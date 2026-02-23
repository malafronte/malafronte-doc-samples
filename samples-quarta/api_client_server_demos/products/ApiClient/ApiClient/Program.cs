using System.Net.Http.Headers;
using System.Net.Http.Json; // Per GetFromJsonAsync, PostAsJsonAsync, etc.
using System.Text.Json;
using ApiClient.Models; // Assumendo che i DTO siano in questo namespace

namespace ApiClient;

public class Program
{
    // --- Configurazione ---
    // Cambia questo URL con l'URL base della tua API (includi https e porta)
    private static readonly string _apiBaseUrl = "http://localhost:3000"; // Esempio di porta comune
    private static HttpClient _httpClient = null!;

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Avvio Client API Prodotti...");

        // Configura HttpClient (gestendo certificati SSL self-signed per localhost)
        ConfigureHttpClient();

        try
        {
            Console.WriteLine($"\n--- TEST API su {_apiBaseUrl} ---");

            // 1. GET Tutti i Prodotti (senza dettagli)
            await TestGetAllProducts(includeRelated: false);

            // 2. GET Tutti i Prodotti (con dettagli)
            await TestGetAllProducts(includeRelated: true);

            // 3. GET Prodotto Specifico (es. ID 1, assumendo esista dal seed)
            int testProductId = 1;
            await TestGetProductById(testProductId);

            // --- Download Media Prodotto Specifico ---
            // Testiamo il download dei media su un prodotto potenzialmente esistente
            await TestDownloadProductMediaById(testProductId);


            // --- Ciclo CRUD ---
            ProductDto? createdProduct = null;
            try
            {
                // 4. POST Nuovo Prodotto
                createdProduct = await TestCreateProduct();
                if (createdProduct == null)
                {
                    Console.WriteLine("\nErrore: Creazione prodotto fallita. Interruzione ciclo CRUD.");
                    return;
                }
                Console.WriteLine($"\nProdotto creato con ID: {createdProduct.Id}");
                // 5. PUT Aggiorna Prodotto Creato
                await TestUpdateProduct(createdProduct);

                // 6. GET Verifica Prodotto Aggiornato
                await TestGetProductById(createdProduct.Id, "Verifica dopo Update");

            }
            finally // Assicura che la DELETE venga tentata anche se l'update fallisce
            {
                // 7. DELETE Prodotto Creato (se esiste)
                if (createdProduct != null)
                {
                    await TestDeleteProduct(createdProduct.Id);

                    // 8. GET Verifica Eliminazione
                    await TestGetProductById(createdProduct.Id, "Verifica dopo Delete");
                }
            }

            // 9. GET Tutti i Prodotti (alla fine, per vedere lo stato finale)
            await TestGetAllProducts(includeRelated: false, "Stato Finale");


        }
        catch (HttpRequestException httpEx)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"\nErrore HTTP: {httpEx.Message}");
            if (httpEx.StatusCode.HasValue)
            {
                Console.WriteLine($"Status Code: {httpEx.StatusCode}");
            }
            Console.WriteLine("Assicurati che l'API sia in esecuzione all'indirizzo specificato e che l'URL sia corretto.");
            Console.ResetColor();
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine($"\nErrore Inaspettato: {ex.Message}");
            Console.ResetColor();
        }
        finally
        {
            Console.WriteLine("\n--- Test API Completato ---");
            _httpClient?.Dispose(); // Rilascia le risorse HttpClient
        }
    }

    // Configura HttpClient per accettare certificati SSL non validi (solo per localhost!)
    //per il trust del certificato di development
    //dotnet dev-certs https --trust

    //per il check del certificato di development
    //dotnet dev-certs https --check

    //per la rimozione del certificato di development
    //dotnet dev-certs https --clean

    private static void ConfigureHttpClient()
    {
        var handler = new HttpClientHandler
        {
            // ATTENZIONE: Questo bypassa la validazione del certificato SSL.
            // Usare SOLO per lo sviluppo locale con certificati autofirmati.
            // NON usare in produzione.
            //ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
            // Alternativa più sicura (ma più complessa) sarebbe installare il certificato dev nel trust store
            // ServerCertificateCustomValidationCallback = (HttpRequestMessage req, X509Certificate2? cert, X509Chain? chain, SslPolicyErrors errors) =>
            // {
            //     // Logica per validare specificamente il certificato di sviluppo
            //     return true; // Se valido per lo sviluppo
            // }
        };

        _httpClient = new HttpClient(handler)
        {
            BaseAddress = new Uri(_apiBaseUrl)
        };
        _httpClient.DefaultRequestHeaders.Accept.Clear();
        _httpClient.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));
    }

    // --- Metodi di Test ---

    private static async Task TestGetAllProducts(bool includeRelated, string context = "")
    {
        string endpoint = includeRelated ? "/products?includeRelated=true" : "/products";
        Console.WriteLine($"\n{context} Eseguendo GET {endpoint}...");

        try
        {
            HttpResponseMessage response = await _httpClient.GetAsync(endpoint);

            if (response.IsSuccessStatusCode)
            {
                var products = await response.Content.ReadFromJsonAsync<List<ProductDto>>();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Ricevuti {products?.Count ?? 0} prodotti.");
                Console.ResetColor();
                // Stampa alcuni dettagli per verifica (opzionale)
                foreach (var p in products?.Take(3) ?? []) // Stampa i primi 3
                {
                    Console.WriteLine($"  - ID: {p.Id}, Titolo: {p.Title}, Prezzo: {p.Price}");
                }
            }
            else
            {
                await LogErrorResponse(response, "GET All Products");
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"GET {endpoint}");
        }
    }

    private static async Task TestGetProductById(int id, string context = "")
    {
        string endpoint = $"/products/{id}";
        Console.WriteLine($"\n{context} Eseguendo GET {endpoint}...");

        try
        {
            HttpResponseMessage response = await _httpClient.GetAsync(endpoint);

            if (response.IsSuccessStatusCode)
            {
                var product = await response.Content.ReadFromJsonAsync<ProductDto>();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Ricevuto Prodotto:");
                Console.WriteLine(JsonSerializer.Serialize(product, new JsonSerializerOptions { WriteIndented = true }));
                Console.ResetColor();
            }
            else
            {
                // Se ci aspettiamo un 404 (es. dopo delete), facciamo il log come informativo
                if (response.StatusCode == System.Net.HttpStatusCode.NotFound && context.Contains("dopo Delete"))
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"Risposta attesa ({response.StatusCode}): Prodotto ID {id} non trovato (corretto dopo DELETE).");
                    Console.ResetColor();
                }
                else
                {
                    await LogErrorResponse(response, $"GET Product By ID ({id})");
                }
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"GET {endpoint}");
        }
    }

    private static async Task<ProductDto?> TestCreateProduct()
    {
        string endpoint = "/products";
        Console.WriteLine($"\nEseguendo POST {endpoint}...");

        // Crea un oggetto DTO per il nuovo prodotto usando CreateProductDto
        var newProduct = new CreateProductDto // <<< MODIFICATO: Usa CreateProductDto
        {
            // L'ID non viene impostato qui
            Title = "Prodotto Console Client",
            Description = "Creato tramite applicazione console C#.",
            Category = "console-test",
            Price = 49.99m,
            DiscountPercentage = 5.5,
            Rating = 4.0,
            Stock = 50,
            Brand = "Client Brand",
            Sku = $"SKU-{Guid.NewGuid().ToString()[..8]}",
            Weight = 0.5,
            WarrantyInformation = "1 anno via console",
            ShippingInformation = "Console Express",
            AvailabilityStatus = "Available via Console",
            ReturnPolicy = "Console Return Policy",
            MinimumOrderQuantity = 1,
            Thumbnail = "http://example.com/consolethumb.png",
            Dimensions = new ProductDimensionsDto { Width = 5, Height = 5, Depth = 5 },
            // Meta non è in CreateProductDto
            Tags = new List<ProductTagDto> { new() { Value = "console" }, new() { Value = "test" } }, // Usa List<T> per inizializzare ICollection<T>?
            Reviews = new List<ProductReviewDto> { new() { Rating = 5, Comment = "Creato da console!", Date = DateTime.UtcNow, ReviewerName = "ConsoleApp", ReviewerEmail = "console@test.com" } },
            Images = new List<ProductImageDto> { new() { Url = "http://example.com/consoleimg1.png" } }
        };

        Console.WriteLine("Dati inviati per la creazione (CreateProductDto):");
        Console.WriteLine(JsonSerializer.Serialize(newProduct, new JsonSerializerOptions { WriteIndented = true }));

        try
        {
            // Invia la richiesta POST con il prodotto nel corpo JSON
            HttpResponseMessage response = await _httpClient.PostAsJsonAsync(endpoint, newProduct);

            if (response.IsSuccessStatusCode && response.StatusCode == System.Net.HttpStatusCode.Created)
            {
                // Leggi il prodotto creato dalla risposta (che include l'ID, quindi è un ProductDto)
                ProductDto? createdProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Prodotto creato:");
                Console.WriteLine($"  Location: {response.Headers.Location}"); // Mostra l'header Location
                Console.WriteLine(JsonSerializer.Serialize(createdProduct, new JsonSerializerOptions { WriteIndented = true }));
                Console.ResetColor();
                return createdProduct; // Restituisce il prodotto creato
            }
            else
            {
                await LogErrorResponse(response, "POST Create Product");
                return null;
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"POST {endpoint}");
            return null;
        }
    }

    private static async Task TestUpdateProduct(ProductDto productToUpdate) // Riceve ancora ProductDto per comodità
    {
        int id = productToUpdate.Id;
        string endpoint = $"/products/{id}";
        Console.WriteLine($"\nEseguendo PUT {endpoint}...");

        // Crea un UpdateProductDto dai dati ricevuti e applica le modifiche
        var updateDto = new UpdateProductDto // <<< MODIFICATO: Crea UpdateProductDto
        {
            Title = productToUpdate.Title + " - Aggiornato", // Applica modifica qui
            Description = "Descrizione aggiornata dalla console.", // Applica modifica qui
            Category = productToUpdate.Category,
            Price = productToUpdate.Price,
            DiscountPercentage = productToUpdate.DiscountPercentage,
            Rating = productToUpdate.Rating,
            Stock = productToUpdate.Stock + 10, // Applica modifica qui
            Brand = productToUpdate.Brand,
            Sku = productToUpdate.Sku,
            Weight = productToUpdate.Weight,
            WarrantyInformation = productToUpdate.WarrantyInformation,
            ShippingInformation = productToUpdate.ShippingInformation,
            AvailabilityStatus = productToUpdate.AvailabilityStatus,
            ReturnPolicy = productToUpdate.ReturnPolicy,
            MinimumOrderQuantity = productToUpdate.MinimumOrderQuantity,
            Thumbnail = productToUpdate.Thumbnail,
            Dimensions = productToUpdate.Dimensions, // Copia l'oggetto esistente
            // Meta non è in UpdateProductDto

            // Ricrea le collezioni per l'aggiornamento (PUT sostituisce)
            Tags = productToUpdate.Tags?.ToList() ?? new List<ProductTagDto>(), // Copia la lista esistente
            Reviews = new List<ProductReviewDto> { new() { Rating = 3, Comment = "Aggiornato da console", Date = DateTime.UtcNow, ReviewerName = "ConsoleAppUpdate", ReviewerEmail = "console@update.com" } }, // Sostituisci con la nuova review
            Images = productToUpdate.Images?.ToList() ?? new List<ProductImageDto>() // Copia la lista esistente
        };

        // Aggiungi un tag alla lista copiata
        updateDto.Tags?.Add(new ProductTagDto { Value = "updated-by-console" });

        Console.WriteLine("Dati inviati per l'aggiornamento (UpdateProductDto):");
        Console.WriteLine(JsonSerializer.Serialize(updateDto, new JsonSerializerOptions { WriteIndented = true }));

        try
        {
            // Invia la richiesta PUT con il DTO di aggiornamento nel corpo JSON
            HttpResponseMessage response = await _httpClient.PutAsJsonAsync(endpoint, updateDto);

            if (response.IsSuccessStatusCode) // PUT può restituire 200 OK o 204 No Content
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Prodotto ID {id} aggiornato.");
                // Se la risposta è 200 OK, potrebbe contenere il prodotto aggiornato (ProductDto)
                if (response.Content.Headers.ContentLength > 0)
                {
                    var updatedProductResponse = await response.Content.ReadFromJsonAsync<ProductDto>(); // La risposta è ancora ProductDto
                    Console.WriteLine("Dati prodotto aggiornati ricevuti nella risposta:");
                    Console.WriteLine(JsonSerializer.Serialize(updatedProductResponse, new JsonSerializerOptions { WriteIndented = true }));
                }
                Console.ResetColor();
            }
            else
            {
                await LogErrorResponse(response, $"PUT Update Product ({id})");
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"PUT {endpoint}");
        }
    }

    private static async Task TestDeleteProduct(int id)
    {
        string endpoint = $"/products/{id}";
        Console.WriteLine($"\nEseguendo DELETE {endpoint}...");

        try
        {
            HttpResponseMessage response = await _httpClient.DeleteAsync(endpoint);

            if (response.IsSuccessStatusCode) // DELETE di solito restituisce 204 No Content
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Prodotto ID {id} eliminato.");
                Console.ResetColor();
            }
            else
            {
                await LogErrorResponse(response, $"DELETE Product ({id})");
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"DELETE {endpoint}");
        }
    }

    // --- Helper per Logging Errori ---
    private static async Task LogErrorResponse(HttpResponseMessage response, string operation)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"Errore durante '{operation}'. Status Code: {response.StatusCode}");
        try
        {
            string errorBody = await response.Content.ReadAsStringAsync();
            if (!string.IsNullOrWhiteSpace(errorBody))
            {
                Console.WriteLine("Corpo della risposta di errore:");
                // Tenta di formattare se è JSON, altrimenti stampa raw
                try
                {
                    using var jsonDoc = JsonDocument.Parse(errorBody);
                    Console.WriteLine(JsonSerializer.Serialize(jsonDoc, new JsonSerializerOptions { WriteIndented = true }));
                }
                catch
                {
                    Console.WriteLine(errorBody);
                }
            }
        }
        catch (Exception ex) { Console.WriteLine($"Impossibile leggere il corpo dell'errore: {ex.Message}"); }
        Console.ResetColor();
    }

    private static void LogError(Exception ex, string operation)
    {
        Console.ForegroundColor = ConsoleColor.DarkRed;
        Console.WriteLine($"Eccezione durante '{operation}': {ex.Message}");
        // Potresti voler loggare anche ex.StackTrace in un vero logger
        Console.ResetColor();
    }

    // --- Metodi di Test ---

    // Metodo che scarica media dato l'ID (recupera prima il prodotto)
    private static async Task TestDownloadProductMediaById(int productId)
    {
        Console.WriteLine($"\nTentativo di download media per Prodotto ID: {productId}...");

        // 1. Recupera i dettagli del prodotto dall'API
        ProductDto? product = null;
        string getEndpoint = $"/products/{productId}";
        try
        {
            HttpResponseMessage response = await _httpClient.GetAsync(getEndpoint);
            if (response.IsSuccessStatusCode)
            {
                product = await response.Content.ReadFromJsonAsync<ProductDto>();
                Console.WriteLine($"Dettagli prodotto ID {productId} recuperati per il download.");
            }
            else
            {
                await LogErrorResponse(response, $"GET Product By ID ({productId}) for Media Download");
                Console.WriteLine("Download media annullato.");
                return; // Esci se non trovi il prodotto
            }
        }
        catch (Exception ex)
        {
            LogError(ex, $"GET {getEndpoint} for Media Download");
            Console.WriteLine("Download media annullato a causa di eccezione nel recupero prodotto.");
            return; // Esci in caso di errore
        }

        // Se il prodotto non è stato recuperato (dovrebbe essere già gestito sopra, ma per sicurezza)
        if (product == null)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Prodotto ID {productId} non trovato o errore nel recupero. Impossibile scaricare media.");
            Console.ResetColor();
            return;
        }

        // 2. Chiama l'overload che prende il DTO
        await TestDownloadProductMedia(product);
    }

    // Metodo che scarica media dato l'oggetto ProductDto (non recupera da API)
    private static async Task TestDownloadProductMedia(ProductDto product)
    {
        if (product == null)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("Tentativo di download media con oggetto ProductDto nullo. Operazione annullata.");
            Console.ResetColor();
            return;
        }
        Console.WriteLine($"\nTentativo di download media per Prodotto ID: {product.Id} (da oggetto DTO)...");

        // Procedi con il download usando i dati del prodotto fornito
        // Calcola la root del progetto risalendo dalla directory di esecuzione
        string projectRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", ".."));
        string baseFolder = Path.Combine(projectRoot, "DownloadedMedia", $"Product_{product.Id}");
        Console.WriteLine($"Download directory: {baseFolder}"); // Aggiunto log per verifica
        Directory.CreateDirectory(baseFolder);
        bool downloadedSomething = false;

        // Scarica Thumbnail
        if (!string.IsNullOrWhiteSpace(product.Thumbnail))
        {
            await DownloadFileAsync(product.Thumbnail, Path.Combine(baseFolder, "thumbnail" + GetFileExtensionFromUrl(product.Thumbnail)));
            downloadedSomething = true;
        }

        // Scarica QR Code
        if (product.Meta != null && !string.IsNullOrWhiteSpace(product.Meta.QrCode))
        {
            await DownloadFileAsync(product.Meta.QrCode, Path.Combine(baseFolder, "qrcode" + GetFileExtensionFromUrl(product.Meta.QrCode)));
            downloadedSomething = true;
        }

        // Scarica Immagini
        if (product.Images != null && product.Images.Count > 0)
        {
            int imgIndex = 1;
            foreach (var img in product.Images)
            {
                if (!string.IsNullOrWhiteSpace(img.Url))
                {
                    string fileName = $"image_{imgIndex}" + GetFileExtensionFromUrl(img.Url);
                    await DownloadFileAsync(img.Url, Path.Combine(baseFolder, fileName));
                    imgIndex++;
                    downloadedSomething = true;
                }
            }
        }

        if (downloadedSomething)
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine($"Media per prodotto ID {product.Id} scaricati in: {baseFolder}");
            Console.ResetColor();
        }
        else
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Nessun media (thumbnail, qrcode, immagini) trovato da scaricare per il prodotto ID {product.Id}.");
            Console.ResetColor();
        }
    }

    // Helper per scaricare un file da URL
    private static async Task DownloadFileAsync(string url, string localPath)
    {
        try
        {
            using var response = await _httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();
            await using var fs = new FileStream(localPath, FileMode.Create, FileAccess.Write, FileShare.None);
            await response.Content.CopyToAsync(fs);
            Console.WriteLine($"Scaricato: {localPath}");
            //in alternativa - ma meno efficiente
            //scarico i byte in memoria e poi salvo su file binario
            // var imageBytes = await _httpClient.GetByteArrayAsync(url);
            // //salvo su file
            // await File.WriteAllBytesAsync(localPath, imageBytes);
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Errore download {url}: {ex.Message}");
            Console.ResetColor();
        }
    }
    // Helper per ottenere l'estensione file da una URL o Percorso Relativo
    private static string GetFileExtensionFromUrl(string urlOrPath) // Rinominato parametro per chiarezza
    {
        if (string.IsNullOrWhiteSpace(urlOrPath)) return ".dat";

        string pathPart = urlOrPath;

        // 1. Rimuovi eventuale query string (es. /path/image.png?v=123)
        //    Path.GetExtension funziona sul percorso, non sull'intera URI con query.
        int queryIndex = pathPart.IndexOf('?');
        if (queryIndex >= 0)
        {
            pathPart = pathPart[..queryIndex];
        }

        // 2. Prova ad estrarre l'estensione usando Path.GetExtension
        //    Questo funziona bene sia per percorsi relativi (come /a/b/c.png)
        //    sia per parti di URL che assomigliano a percorsi (come image.png).
        try
        {
            string ext = Path.GetExtension(pathPart);

            // Controlla se l'estensione è valida (non vuota, non solo '.')
            if (!string.IsNullOrWhiteSpace(ext) && ext != ".")
            {
                return ext; // Es: ".png" - Trovata!
            }
        }
        catch (ArgumentException argEx)
        {
            // Path.GetExtension può lanciare eccezioni se il path contiene caratteri non validi.
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"[GetFileExtensionFromUrl] Errore Path.GetExtension per '{pathPart}': {argEx.Message}");
            Console.ResetColor();
            // Non ritorniamo qui, potremmo ancora provare con Uri se è un URL assoluto valido
        }
        catch (Exception ex) // Catch generico per sicurezza
        {
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine($"[GetFileExtensionFromUrl] Errore inatteso durante Path.GetExtension per '{pathPart}': {ex.Message}");
            Console.ResetColor();
        }


        // 3. Fallback: Se Path.GetExtension non ha funzionato o non ha dato risultati,
        //    e SE sembra un URL assoluto, proviamo ancora con la logica Uri (per compatibilità).
        //    Questo è meno probabile che serva nel tuo caso attuale, ma lo manteniamo.
        if (Uri.IsWellFormedUriString(urlOrPath, UriKind.Absolute))
        {
            try
            {
                if (Uri.TryCreate(urlOrPath, UriKind.Absolute, out Uri? uri))
                {
                    string? fileName = uri.Segments.LastOrDefault();
                    if (!string.IsNullOrEmpty(fileName))
                    {
                        // Applica di nuovo Path.GetExtension sull'ultimo segmento dell'URI
                        string extFromUri = Path.GetExtension(fileName);
                        if (!string.IsNullOrWhiteSpace(extFromUri) && extFromUri != ".")
                        {
                            return extFromUri;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.DarkYellow;
                Console.WriteLine($"[GetFileExtensionFromUrl] Errore durante l'analisi Uri di '{urlOrPath}': {ex.Message}");
                Console.ResetColor();
            }
        }

        // 4. Se NIENTE ha funzionato, ritorna il default ".dat"
        Console.ForegroundColor = ConsoleColor.DarkYellow;
        Console.WriteLine($"[GetFileExtensionFromUrl] Impossibile determinare l'estensione per: '{urlOrPath}'. Defaulting to .dat");
        Console.ResetColor();
        return ".dat";
    }
}

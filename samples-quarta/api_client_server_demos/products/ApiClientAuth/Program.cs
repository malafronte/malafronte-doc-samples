using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json;
using System.Text.Json.Serialization;
using ApiClient.Models;

namespace ApiClientAuth;

// Classe che rappresenta il payload JSON inviato al server per l'autenticazione
public class LoginRequest
{
    [JsonPropertyName("email")]
    public string Email { get; set; } = "";

    [JsonPropertyName("password")]
    public string Password { get; set; } = "";
}

// Classe che rappresenta la risposta JSON del server contenente il token JWT
public class LoginResponse
{
    [JsonPropertyName("access_token")]
    public string AccessToken { get; set; } = "";
}

public class Program
{
    private static readonly string _apiBaseUrl = "http://localhost:3001";
    private static HttpClient _httpClient = null!;
    private static string _token = "";

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Avvio Client API Prodotti con Autenticazione...");

        ConfigureHttpClient();

        try
        {
            Console.WriteLine($"\n--- TEST API su {_apiBaseUrl} ---");

            // 1. GET Tutti i Prodotti (senza dettagli) - Non richiede auth
            await TestGetAllProducts(includeRelated: false);

            // 2. GET Prodotto Specifico - Non richiede auth
            int testProductId = 1;
            await TestGetProductById(testProductId);

            // --- Login ---
            bool isLoggedIn = await TestLogin("admin@example.com", "admin123");
            if (!isLoggedIn)
            {
                Console.WriteLine("\nErrore: Login fallito. Interruzione ciclo CRUD.");
                return;
            }

            // --- Ciclo CRUD (Richiede Auth) ---
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
            finally
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
            _httpClient?.Dispose();
        }
    }

    private static void ConfigureHttpClient()
    {
        var handler = new HttpClientHandler();
        _httpClient = new HttpClient(handler)
        {
            BaseAddress = new Uri(_apiBaseUrl)
        };

        // Pulisce eventuali header Accept preesistenti
        _httpClient.DefaultRequestHeaders.Accept.Clear();

        // Imposta l'header Accept per indicare al server che il client si aspetta risposte in formato JSON
        _httpClient.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));
    }

    private static async Task<bool> TestLogin(string email, string password)
    {
        Console.WriteLine($"\nEseguendo POST /login...");

        // Crea l'oggetto con le credenziali da inviare
        var loginRequest = new LoginRequest { Email = email, Password = password };

        try
        {
            // Invia una richiesta POST all'endpoint /login con le credenziali serializzate in JSON
            HttpResponseMessage response = await _httpClient.PostAsJsonAsync("/login", loginRequest);

            if (response.IsSuccessStatusCode)
            {
                // Deserializza la risposta JSON per estrarre il token JWT
                var loginResponse = await response.Content.ReadFromJsonAsync<LoginResponse>();

                if (loginResponse != null && !string.IsNullOrEmpty(loginResponse.AccessToken))
                {
                    // Salva il token in una variabile statica (opzionale, utile per debug o log)
                    _token = loginResponse.AccessToken;

                    // CONFIGURAZIONE HEADER DI AUTENTICAZIONE:
                    // Aggiunge il token JWT all'header "Authorization" dell'istanza globale di HttpClient.
                    // Lo schema "Bearer" indica che stiamo passando un token di portatore.
                    // Da questo momento in poi, TUTTE le richieste successive effettuate con _httpClient 
                    // includeranno automaticamente questo header, permettendo l'accesso alle rotte protette.
                    _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _token);

                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine($"Successo ({response.StatusCode}). Token ottenuto e configurato.");
                    Console.ResetColor();
                    return true;
                }
            }

            await LogErrorResponse(response, "POST Login");
            return false;
        }
        catch (Exception ex)
        {
            LogError(ex, "POST /login");
            return false;
        }
    }

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
                foreach (var p in products?.Take(3) ?? [])
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

        var newProduct = new CreateProductDto
        {
            Title = "Prodotto Console Client Auth",
            Description = "Creato tramite applicazione console C# con Auth.",
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
            Tags = new List<ProductTagDto> { new() { Value = "console" }, new() { Value = "auth" } },
            Reviews = new List<ProductReviewDto> { new() { Rating = 5, Comment = "Creato da console auth!", Date = DateTime.UtcNow, ReviewerName = "ConsoleApp", ReviewerEmail = "console@test.com" } },
            Images = new List<ProductImageDto> { new() { Url = "http://example.com/consoleimg1.png" } }
        };

        try
        {
            HttpResponseMessage response = await _httpClient.PostAsJsonAsync(endpoint, newProduct);

            if (response.IsSuccessStatusCode && response.StatusCode == System.Net.HttpStatusCode.Created)
            {
                ProductDto? createdProduct = await response.Content.ReadFromJsonAsync<ProductDto>();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Prodotto creato:");
                Console.WriteLine($"  Location: {response.Headers.Location}");
                Console.WriteLine(JsonSerializer.Serialize(createdProduct, new JsonSerializerOptions { WriteIndented = true }));
                Console.ResetColor();
                return createdProduct;
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

    private static async Task TestUpdateProduct(ProductDto productToUpdate)
    {
        int id = productToUpdate.Id;
        string endpoint = $"/products/{id}";
        Console.WriteLine($"\nEseguendo PUT {endpoint}...");

        var updateDto = new UpdateProductDto
        {
            Title = productToUpdate.Title + " - Aggiornato Auth",
            Description = "Descrizione aggiornata dalla console auth.",
            Category = productToUpdate.Category,
            Price = productToUpdate.Price,
            DiscountPercentage = productToUpdate.DiscountPercentage,
            Rating = productToUpdate.Rating,
            Stock = productToUpdate.Stock + 10,
            Brand = productToUpdate.Brand,
            Sku = productToUpdate.Sku,
            Weight = productToUpdate.Weight,
            WarrantyInformation = productToUpdate.WarrantyInformation,
            ShippingInformation = productToUpdate.ShippingInformation,
            AvailabilityStatus = productToUpdate.AvailabilityStatus,
            ReturnPolicy = productToUpdate.ReturnPolicy,
            MinimumOrderQuantity = productToUpdate.MinimumOrderQuantity,
            Thumbnail = productToUpdate.Thumbnail,
            Dimensions = productToUpdate.Dimensions,
            Tags = productToUpdate.Tags?.ToList() ?? new List<ProductTagDto>(),
            Reviews = new List<ProductReviewDto> { new() { Rating = 3, Comment = "Aggiornato da console auth", Date = DateTime.UtcNow, ReviewerName = "ConsoleAppUpdate", ReviewerEmail = "console@update.com" } },
            Images = productToUpdate.Images?.ToList() ?? new List<ProductImageDto>()
        };

        updateDto.Tags?.Add(new ProductTagDto { Value = "updated-by-console-auth" });

        try
        {
            HttpResponseMessage response = await _httpClient.PutAsJsonAsync(endpoint, updateDto);

            if (response.IsSuccessStatusCode)
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"Successo ({response.StatusCode}). Prodotto ID {id} aggiornato.");
                if (response.Content.Headers.ContentLength > 0)
                {
                    var updatedProductResponse = await response.Content.ReadFromJsonAsync<ProductDto>();
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

            if (response.IsSuccessStatusCode)
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
        Console.ResetColor();
    }
}

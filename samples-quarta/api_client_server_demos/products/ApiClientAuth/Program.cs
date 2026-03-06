using System.Text.Json;
using ApiClientAuth.Models;

namespace ApiClientAuth;

public class Program
{
    private const string ApiBaseUrl = "http://localhost:3001";

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Avvio Client API Prodotti con Autenticazione...");

        using var apiClient = new ApiClient(ApiBaseUrl);
        var jsonOptions = new JsonSerializerOptions { WriteIndented = true };

        try
        {
            Console.WriteLine($"\n--- TEST API su {ApiBaseUrl} ---");

            List<Product> allProducts = await apiClient.GetAllProductsAsync();
            Console.WriteLine($"GET /products -> {allProducts.Count} prodotti");
            foreach (Product product in allProducts.Take(3))
            {
                Console.WriteLine($"  - ID: {product.Id}, Titolo: {product.Title}, Prezzo: {product.Price:F2}");
            }

            const int testProductId = 1;
            Product? productById = await apiClient.GetProductByIdAsync(testProductId);
            Console.WriteLine($"\nGET /products/{testProductId}");
            Console.WriteLine(productById == null
                ? "  Prodotto non trovato"
                : JsonSerializer.Serialize(productById, jsonOptions));

            ImageDownloadResult? downloaded = await apiClient.DownloadProductImageAsync(testProductId);
            if (downloaded == null)
            {
                Console.WriteLine("\nDownload immagine (completo): nessuna immagine disponibile.");
            }
            else
            {
                Console.WriteLine($"\nDownload immagine (completo): {downloaded.FilePath} ({downloaded.ByteCount} byte)");
            }

            ImageDownloadResult? downloadedSimple = await apiClient.DownloadProductImageSimpleAsync(testProductId);
            if (downloadedSimple == null)
            {
                Console.WriteLine("Download immagine (semplice): nessuna immagine disponibile.");
            }
            else
            {
                Console.WriteLine($"Download immagine (semplice): {downloadedSimple.FilePath} ({downloadedSimple.ByteCount} byte)");
            }

            const string sampleCategory = "electronics";
            decimal? averageAll = await apiClient.GetAveragePriceAllProductsAsync();
            Console.WriteLine(averageAll.HasValue
                ? $"\nPrezzo medio complessivo: {averageAll.Value:F2}"
                : "\nPrezzo medio complessivo non disponibile (nessun prodotto).");

            CategoryAverageResult? averageByCategory = await apiClient.GetAveragePriceByCategoryAsync(sampleCategory);
            Console.WriteLine(averageByCategory == null
                ? $"Prezzo medio categoria '{sampleCategory}' non disponibile."
                : $"Prezzo medio categoria '{averageByCategory.Category}': {averageByCategory.AveragePrice:F2} (su {averageByCategory.Count} prodotti)");

            IReadOnlyList<CategoryTopProducts> topByCategory = await apiClient.GetTopThreeProductsByRankingPerCategoryAsync();
            Console.WriteLine("\nTop 3 prodotti per rating in ogni categoria:");
            foreach (CategoryTopProducts categoryGroup in topByCategory)
            {
                Console.WriteLine($"Categoria: {categoryGroup.Category}");
                foreach (Product product in categoryGroup.Products)
                {
                    Console.WriteLine($"  - #{product.Id} {product.Title} | Rating: {product.Rating:F2} | Prezzo: {product.Price:F2}");
                }
            }

            PagedProductsResult page1 = await apiClient.ListProductsByCategoryPagedAndSortedAsync(sampleCategory, page: 1, pageSize: 3);
            PagedProductsResult page2 = await apiClient.ListProductsByCategoryPagedAndSortedAsync(sampleCategory, page: 2, pageSize: 3);
            PrintPageResult(page1);
            PrintPageResult(page2);

            bool isLoggedIn = await apiClient.LoginAsync("admin@example.com", "admin123");
            if (!isLoggedIn)
            {
                Console.WriteLine("\nErrore: login fallito. Interruzione ciclo CRUD protetto.");
                return;
            }

            Console.WriteLine("\nLogin eseguito con successo.");

            Product? createdProduct = null;
            try
            {
                CreateProduct createDto = BuildCreateProduct();
                createdProduct = await apiClient.CreateProductAsync(createDto);

                if (createdProduct == null)
                {
                    Console.WriteLine("Creazione prodotto fallita: risposta vuota.");
                    return;
                }

                Console.WriteLine($"Prodotto creato con ID: {createdProduct.Id}");

                UpdateProduct updateDto = BuildUpdateProduct(createdProduct);
                Product? updatedProduct = await apiClient.UpdateProductAsync(createdProduct.Id, updateDto);
                Console.WriteLine(updatedProduct == null
                    ? "Aggiornamento completato senza payload di risposta."
                    : $"Prodotto aggiornato: ID {updatedProduct.Id}, Titolo: {updatedProduct.Title}");

                Product? afterUpdate = await apiClient.GetProductByIdAsync(createdProduct.Id);
                Console.WriteLine("Verifica dopo update:");
                Console.WriteLine(afterUpdate == null
                    ? "  Prodotto non trovato"
                    : JsonSerializer.Serialize(afterUpdate, jsonOptions));
            }
            finally
            {
                if (createdProduct != null)
                {
                    bool deleted = await apiClient.DeleteProductAsync(createdProduct.Id);
                    Console.WriteLine(deleted
                        ? $"Prodotto ID {createdProduct.Id} eliminato."
                        : $"Prodotto ID {createdProduct.Id} non trovato in fase di delete.");

                    Product? afterDelete = await apiClient.GetProductByIdAsync(createdProduct.Id);
                    Console.WriteLine(afterDelete == null
                        ? "Verifica dopo delete: prodotto non più presente (OK)."
                        : "Verifica dopo delete: prodotto ancora presente (da investigare).");
                }
            }

            List<Product> finalProducts = await apiClient.GetAllProductsAsync();
            Console.WriteLine($"\nStato finale: {finalProducts.Count} prodotti disponibili.");
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
            Console.WriteLine($"\nErrore inatteso: {ex.Message}");
            Console.ResetColor();
        }
        finally
        {
            Console.WriteLine("\n--- Test API completato ---");
        }
    }

    private static void PrintPageResult(PagedProductsResult page)
    {
        string total = page.TotalCount.HasValue ? page.TotalCount.Value.ToString() : "n/d";
        Console.WriteLine($"\nPagina {page.Page}, size {page.PageSize}, totale categoria: {total}, elementi ricevuti: {page.Items.Count}");

        foreach (Product product in page.Items)
        {
            Console.WriteLine($"  - #{product.Id} {product.Title} | Prezzo: {product.Price:F2} | Categoria: {product.Category}");
        }
    }

    private static CreateProduct BuildCreateProduct()
    {
        return new CreateProduct
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
            Dimensions = new ProductDimensions { Width = 5, Height = 5, Depth = 5 },
            Tags = [new ProductTag { Value = "console" }, new ProductTag { Value = "auth" }],
            Reviews =
            [
                new ProductReview
                {
                    Rating = 5,
                    Comment = "Creato da console auth!",
                    Date = DateTime.UtcNow,
                    ReviewerName = "ConsoleApp",
                    ReviewerEmail = "console@test.com"
                }
            ],
            Images = [new ProductImage { Url = "http://example.com/consoleimg1.png" }]
        };
    }

    private static UpdateProduct BuildUpdateProduct(Product productToUpdate)
    {
        var updateDto = new UpdateProduct
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
            Tags = productToUpdate.Tags?.ToList() ?? [],
            Reviews =
            [
                new ProductReview
                {
                    Rating = 3,
                    Comment = "Aggiornato da console auth",
                    Date = DateTime.UtcNow,
                    ReviewerName = "ConsoleAppUpdate",
                    ReviewerEmail = "console@update.com"
                }
            ],
            Images = productToUpdate.Images?.ToList() ?? []
        };

        updateDto.Tags?.Add(new ProductTag { Value = "updated-by-console-auth" });
        return updateDto;
    }
}

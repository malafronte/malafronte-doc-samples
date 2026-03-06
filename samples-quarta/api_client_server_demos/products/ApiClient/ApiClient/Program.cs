using ApiClient.Models;
using System.Text.Json;

namespace ApiClient;

public class Program
{
    private static readonly string _apiBaseUrl = "http://localhost:3000";
    private static readonly JsonSerializerOptions _jsonOptions = new()
    {
        WriteIndented = true,
        PropertyNameCaseInsensitive = true
    };

    public static async Task Main(string[] args)
    {
        Console.WriteLine("Avvio Client API Prodotti...");
        using var client = new Client(_apiBaseUrl);

        try
        {
            Console.WriteLine($"\n--- TEST API su {_apiBaseUrl} ---");

            var products = await client.GetAllProductsAsync();
            PrintProductsSummary(products, "GET /products");

            int testProductId = 1;
            var product = await client.GetProductByIdAsync(testProductId);
            PrintProductDetails(product, $"GET /products/{testProductId}");

            string? mediaFolder = await client.DownloadProductMediaByIdAsync(testProductId);
            Console.WriteLine(mediaFolder == null
                ? $"Nessun media scaricato per prodotto {testProductId} (prodotto non trovato)."
                : $"Media scaricati in: {mediaFolder}");

            Product? createdProduct = null;
            try
            {
                var createRequest = BuildSampleCreateProduct();
                Console.WriteLine("\nPayload creazione:");
                Console.WriteLine(JsonSerializer.Serialize(createRequest, _jsonOptions));

                createdProduct = await client.CreateProductAsync(createRequest);
                if (createdProduct == null)
                {
                    Console.WriteLine("\nErrore: Creazione prodotto fallita. Interruzione ciclo CRUD.");
                    return;
                }

                Console.WriteLine($"\nProdotto creato con ID: {createdProduct.Id}");
                var updateRequest = BuildSampleUpdateProduct(createdProduct);
                Console.WriteLine("Payload aggiornamento:");
                Console.WriteLine(JsonSerializer.Serialize(updateRequest, _jsonOptions));

                await client.UpdateProductAsync(createdProduct.Id, updateRequest);
                var updatedProduct = await client.GetProductByIdAsync(createdProduct.Id);
                PrintProductDetails(updatedProduct, "Verifica dopo Update");
            }
            finally
            {
                if (createdProduct != null)
                {
                    await client.DeleteProductAsync(createdProduct.Id);
                    var deletedCheck = await client.GetProductByIdAsync(createdProduct.Id);
                    if (deletedCheck == null)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine($"Verifica dopo Delete: prodotto {createdProduct.Id} non trovato (atteso).");
                        Console.ResetColor();
                    }
                    else
                    {
                        PrintProductDetails(deletedCheck, "Verifica dopo Delete");
                    }
                }
            }

            var finalProducts = await client.GetAllProductsAsync();
            PrintProductsSummary(finalProducts, "Stato Finale");
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
        }
    }

    private static void PrintProductsSummary(List<Product> products, string context)
    {
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"\n{context}: ricevuti {products.Count} prodotti.");
        Console.ResetColor();

        foreach (var p in products.Take(3))
        {
            Console.WriteLine($"  - ID: {p.Id}, Titolo: {p.Title}, Prezzo: {p.Price}");
        }
    }

    private static void PrintProductDetails(Product? product, string context)
    {
        if (product == null)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"\n{context}: prodotto non trovato.");
            Console.ResetColor();
            return;
        }

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"\n{context}:\n{JsonSerializer.Serialize(product, _jsonOptions)}");
        Console.ResetColor();
    }

    private static CreateProduct BuildSampleCreateProduct()
    {
        return new CreateProduct
        {
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
            Dimensions = new ProductDimensions { Width = 5, Height = 5, Depth = 5 },
            Tags = new List<ProductTag> { new() { Value = "console" }, new() { Value = "test" } },
            Reviews = new List<ProductReview>
            {
                new()
                {
                    Rating = 5,
                    Comment = "Creato da console!",
                    Date = DateTime.UtcNow,
                    ReviewerName = "ConsoleApp",
                    ReviewerEmail = "console@test.com"
                }
            },
            Images = new List<ProductImage> { new() { Url = "http://example.com/consoleimg1.png" } }
        };
    }

    private static UpdateProduct BuildSampleUpdateProduct(Product source)
    {
        var dto = new UpdateProduct
        {
            Title = source.Title + " - Aggiornato",
            Description = "Descrizione aggiornata dalla console.",
            Category = source.Category,
            Price = source.Price,
            DiscountPercentage = source.DiscountPercentage,
            Rating = source.Rating,
            Stock = source.Stock + 10,
            Brand = source.Brand,
            Sku = source.Sku,
            Weight = source.Weight,
            WarrantyInformation = source.WarrantyInformation,
            ShippingInformation = source.ShippingInformation,
            AvailabilityStatus = source.AvailabilityStatus,
            ReturnPolicy = source.ReturnPolicy,
            MinimumOrderQuantity = source.MinimumOrderQuantity,
            Thumbnail = source.Thumbnail,
            Dimensions = source.Dimensions,
            Tags = source.Tags?.ToList() ?? new List<ProductTag>(),
            Reviews = new List<ProductReview>
            {
                new()
                {
                    Rating = 3,
                    Comment = "Aggiornato da console",
                    Date = DateTime.UtcNow,
                    ReviewerName = "ConsoleAppUpdate",
                    ReviewerEmail = "console@update.com"
                }
            },
            Images = source.Images?.ToList() ?? new List<ProductImage>()
        };

        dto.Tags?.Add(new ProductTag { Value = "updated-by-console" });
        return dto;
    }
}

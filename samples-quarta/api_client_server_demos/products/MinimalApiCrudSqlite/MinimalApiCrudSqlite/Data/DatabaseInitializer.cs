using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using MinimalApiCrudSqlite.ModelDto;
using MinimalApiCrudSqlite.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

namespace MinimalApiCrudSqlite.Data
{
    /// <summary>
    /// Classe helper per inizializzare e popolare il database.
    /// </summary>
    public static class DatabaseInitializer
    {
        // --- Helper Class per Deserializzazione JSON Seed ---
        // Struttura che corrisponde alla radice del file JSON
        private class ProductSeedDataWrapper
        {
            public List<ProductJsonDto>? Products { get; set; }
        }



        /// <summary>
        /// Applica le migrazioni e popola il database con dati iniziali se è vuoto.
        /// </summary>
        /// <param name="dbContext">Il contesto del database.</param>
        /// <param name="logger">Il logger per registrare informazioni ed errori.</param>
        /// <param name="configuration">L'oggetto di configurazione dell'applicazione.</param> // Aggiunto parametro
        public static async Task InitializeAndSeedAsync(AppDbContext dbContext, ILogger logger, IConfiguration configuration) // Modificata firma
        {
            try
            {
                logger.LogInformation("Applying database migrations...");
                dbContext.Database.Migrate();
                logger.LogInformation("Database migrations applied successfully.");

                if (!await dbContext.Products.AnyAsync())
                {
                    logger.LogInformation("Database is empty after migration. Seeding data from JSON...");

                    // --- Leggi il percorso del file di seed dalla configurazione ---
                    string? seedFilePathRelative = configuration.GetValue<string>("DatabaseSeedSettings:SeedFilePath");

                    if (string.IsNullOrEmpty(seedFilePathRelative))
                    {
                        logger.LogError("Seed file path not found in configuration (DatabaseSeedSettings:SeedFilePath). Skipping seeding.");
                        return; // Esce se la configurazione manca o è vuota
                    }

                    string seedFilePathAbsolute = Path.Combine(AppContext.BaseDirectory, seedFilePathRelative);
                    logger.LogInformation("Attempting to read seed file from: {SeedFilePath}", seedFilePathAbsolute);
                    // --- Fine lettura da configurazione ---

                    if (!File.Exists(seedFilePathAbsolute)) // Usa il percorso assoluto
                    {
                        logger.LogError($"Seed file not found at {seedFilePathAbsolute}. Skipping seeding.");
                        return;
                    }

                    string jsonData = await File.ReadAllTextAsync(seedFilePathAbsolute); // Usa il percorso assoluto

                    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    var seedDataWrapper = JsonSerializer.Deserialize<ProductSeedDataWrapper>(jsonData, options);

                    if (seedDataWrapper?.Products == null || !seedDataWrapper.Products.Any())
                    {
                        logger.LogWarning("Seed file is empty or invalid. Skipping seeding.");
                        return;
                    }

                    var productsToAdd = new List<Product>();
                    foreach (var productDto in seedDataWrapper.Products)
                    {
                        var dimensionsEntity = productDto.Dimensions != null ? new ProductDimensions
                        { Id = 0, Width = productDto.Dimensions.Width, Height = productDto.Dimensions.Height, Depth = productDto.Dimensions.Depth } : null;

                        var metaEntity = productDto.Meta != null ? new ProductMeta
                        { Id = 0, CreatedAt = productDto.Meta.CreatedAt.ToUniversalTime(), UpdatedAt = productDto.Meta.UpdatedAt.ToUniversalTime(), Barcode = productDto.Meta.Barcode, QrCode = productDto.Meta.QrCode }
                        : new ProductMeta { Id = 0, CreatedAt = DateTime.UtcNow, UpdatedAt = DateTime.UtcNow };

                        var productEntity = new Product
                        {
                            Title = productDto.Title,
                            Description = productDto.Description,
                            Category = productDto.Category,
                            Price = productDto.Price,
                            DiscountPercentage = productDto.DiscountPercentage,
                            Rating = productDto.Rating,
                            Stock = productDto.Stock,
                            Brand = productDto.Brand,
                            Sku = productDto.Sku,
                            Weight = productDto.Weight,
                            WarrantyInformation = productDto.WarrantyInformation,
                            ShippingInformation = productDto.ShippingInformation,
                            AvailabilityStatus = productDto.AvailabilityStatus,
                            ReturnPolicy = productDto.ReturnPolicy,
                            MinimumOrderQuantity = productDto.MinimumOrderQuantity,
                            Thumbnail = productDto.Thumbnail,
                            Dimensions = dimensionsEntity,
                            Meta = metaEntity,
                            Tags = new List<ProductTag>(),
                            Reviews = new List<ProductReview>(),
                            Images = new List<ProductImage>()
                        };

                        if (productDto.Tags != null) { foreach (var tagValue in productDto.Tags) { productEntity.Tags.Add(new ProductTag { Id = 0, Value = tagValue }); } }
                        if (productDto.Reviews != null) { foreach (var reviewDto in productDto.Reviews) { productEntity.Reviews.Add(new ProductReview { Id = 0, Rating = reviewDto.Rating, Comment = reviewDto.Comment, Date = reviewDto.Date.ToUniversalTime(), ReviewerName = reviewDto.ReviewerName, ReviewerEmail = reviewDto.ReviewerEmail }); } }
                        if (productDto.Images != null) { foreach (var imageUrl in productDto.Images) { productEntity.Images.Add(new ProductImage { Id = 0, Url = imageUrl }); } }

                        productsToAdd.Add(productEntity);
                    }

                    await dbContext.Products.AddRangeAsync(productsToAdd);
                    await dbContext.SaveChangesAsync();
                    logger.LogInformation("Database seeded successfully with {Count} products.", productsToAdd.Count);
                }
                else
                {
                    logger.LogInformation("Database already contains data. Skipping seeding.");
                }
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "An error occurred during database migration or seeding.");
                // throw; // Considera se rilanciare
            }
        }
    }
}

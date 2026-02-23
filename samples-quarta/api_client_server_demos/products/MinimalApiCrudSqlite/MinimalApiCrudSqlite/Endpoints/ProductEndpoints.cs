using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MinimalApiCrudSqlite.Data;
using MinimalApiCrudSqlite.Models;
using MinimalApiCrudSqlite.ModelDto; // Aggiunto using per i DTO

namespace MinimalApiCrudSqlite.Endpoints;

public static class ProductEndpoints
{
    // Helper method for mapping Product entity to ProductDto
    private static ProductDto MapProductToDto(Product product)
    {
        return new ProductDto
        {
            Id = product.Id,
            Title = product.Title,
            Description = product.Description,
            Category = product.Category,
            Price = product.Price,
            DiscountPercentage = product.DiscountPercentage,
            Rating = product.Rating,
            Stock = product.Stock,
            Brand = product.Brand,
            Sku = product.Sku,
            Weight = product.Weight,
            WarrantyInformation = product.WarrantyInformation,
            ShippingInformation = product.ShippingInformation,
            AvailabilityStatus = product.AvailabilityStatus,
            ReturnPolicy = product.ReturnPolicy,
            MinimumOrderQuantity = product.MinimumOrderQuantity,
            Thumbnail = product.Thumbnail,
            Dimensions = product.Dimensions == null ? null : new ProductDimensionsDto
            {
                Width = product.Dimensions.Width,
                Height = product.Dimensions.Height,
                Depth = product.Dimensions.Depth
            },
            Meta = product.Meta == null ? null : new ProductMetaDto
            {
                CreatedAt = product.Meta.CreatedAt,
                UpdatedAt = product.Meta.UpdatedAt,
                Barcode = product.Meta.Barcode,
                QrCode = product.Meta.QrCode
            },
            Tags = product.Tags?.Select(t => new ProductTagDto { Value = t.Value }).ToList() ?? [],
            Reviews = product.Reviews?.Select(r => new ProductReviewDto
            {
                Rating = r.Rating,
                Comment = r.Comment,
                Date = r.Date,
                ReviewerName = r.ReviewerName,
                ReviewerEmail = r.ReviewerEmail
            }).ToList() ?? new List<ProductReviewDto>(),
            Images = product.Images?.Select(i => new ProductImageDto { Url = i.Url }).ToList() ?? []
        };
    }


    public static RouteGroupBuilder MapProductEndpoints(this RouteGroupBuilder group)
    {
        // GET /products - Recupera tutti i prodotti come DTO
        group.MapGet("/", async (AppDbContext db, [FromQuery] bool includeRelated = false) =>
        {
            IQueryable<Product> query = db.Products.AsNoTracking();
            if (includeRelated)
            {
                query = query.Include(p => p.Dimensions)
                             .Include(p => p.Meta)
                             .Include(p => p.Tags)
                             .Include(p => p.Images)
                             .Include(p => p.Reviews);
            }
            var products = await query.ToListAsync();
            var productDtos = products.Select(MapProductToDto).ToList(); // Mappa a DTO
            return Results.Ok(productDtos);
        })
        .WithName("GetAllProducts")
        .WithSummary("Recupera tutti i prodotti")
        .WithDescription("Recupera la lista di tutti i prodotti come DTO. Usa ?includeRelated=true per caricare Dimensions, Meta, Tags, Images, Reviews.")
        .Produces<List<ProductDto>>(StatusCodes.Status200OK); // Modificato tipo di ritorno

        // GET /products/{id} - Recupera un prodotto specifico per ID come DTO
        group.MapGet("/{id:int}", async (int id, AppDbContext db) =>
        {
            var product = await db.Products
                .AsNoTracking()
                .Include(p => p.Dimensions)
                .Include(p => p.Meta)
                .Include(p => p.Reviews)
                .Include(p => p.Tags)
                .Include(p => p.Images)
                .FirstOrDefaultAsync(p => p.Id == id);

            if (product is null)
            {
                return Results.NotFound($"Prodotto con ID {id} non trovato.");
            }
            var productDto = MapProductToDto(product); // Mappa a DTO
            return Results.Ok(productDto);
        })
        .WithName("GetProductById")
        .WithSummary("Recupera un prodotto per ID")
        .WithDescription("Recupera un prodotto specifico tramite il suo ID come DTO, inclusi tutti i dati correlati (Dimensions, Meta, Reviews, Tags, Images).")
        .Produces<ProductDto>(StatusCodes.Status200OK) // Modificato tipo di ritorno
        .Produces(StatusCodes.Status404NotFound);

        // POST /products - Crea un nuovo prodotto usando CreateProductDto
        group.MapPost("/", async ([FromBody] CreateProductDto createDto, AppDbContext db) =>
        {
            // Mappa CreateProductDto a Product entity
            var product = new Product
            {
                Title = createDto.Title,
                Description = createDto.Description,
                Category = createDto.Category,
                Price = createDto.Price,
                DiscountPercentage = createDto.DiscountPercentage,
                Rating = createDto.Rating,
                Stock = createDto.Stock,
                Brand = createDto.Brand,
                Sku = createDto.Sku,
                Weight = createDto.Weight,
                WarrantyInformation = createDto.WarrantyInformation,
                ShippingInformation = createDto.ShippingInformation,
                AvailabilityStatus = createDto.AvailabilityStatus,
                ReturnPolicy = createDto.ReturnPolicy,
                MinimumOrderQuantity = createDto.MinimumOrderQuantity,
                Thumbnail = createDto.Thumbnail,
                // Crea Meta automaticamente
                Meta = new ProductMeta { CreatedAt = DateTime.UtcNow, UpdatedAt = DateTime.UtcNow },
                // Mappa Dimensions se presente
                Dimensions = createDto.Dimensions == null ? null : new ProductDimensions
                {
                    Width = createDto.Dimensions.Width,
                    Height = createDto.Dimensions.Height,
                    Depth = createDto.Dimensions.Depth
                },
                // Mappa collezioni se presenti
                Tags = createDto.Tags?.Select(t => new ProductTag { Value = t.Value }).ToList() ?? [],
                Reviews = createDto.Reviews?.Select(r => new ProductReview
                {
                    Rating = r.Rating,
                    Comment = r.Comment,
                    Date = r.Date,
                    ReviewerName = r.ReviewerName,
                    ReviewerEmail = r.ReviewerEmail
                }).ToList() ?? [],
                Images = createDto.Images?.Select(i => new ProductImage { Url = i.Url }).ToList() ?? []
            };

            db.Products.Add(product);
            await db.SaveChangesAsync();

            // Ricarica il prodotto creato con le relazioni per mapparlo al DTO di risposta
            var createdProduct = await db.Products
               .AsNoTracking()
               .Include(p => p.Dimensions)
               .Include(p => p.Meta)
               .Include(p => p.Reviews)
               .Include(p => p.Tags)
               .Include(p => p.Images)
               .FirstOrDefaultAsync(p => p.Id == product.Id);

            if (createdProduct == null)
            {
                // Questo non dovrebbe accadere se SaveChangesAsync ha successo, ma è una buona pratica gestirlo
                return Results.Problem("Errore durante il recupero del prodotto appena creato.", statusCode: StatusCodes.Status500InternalServerError);
            }

            var createdProductDto = MapProductToDto(createdProduct); // Mappa a DTO

            return Results.CreatedAtRoute("GetProductById", new { id = product.Id }, createdProductDto);
        })
        .WithName("CreateProduct")
        .WithSummary("Crea un nuovo prodotto")
        .WithDescription("Crea un nuovo prodotto usando un DTO. Includere Dimensions, Tags, Reviews, Images nel corpo della richiesta se necessario. Meta viene generato automaticamente.")
        .Accepts<CreateProductDto>("application/json") // Modificato tipo di input
        .Produces<ProductDto>(StatusCodes.Status201Created) // Modificato tipo di ritorno
        .ProducesValidationProblem();

        // PUT /products/{id} - Aggiorna un prodotto esistente usando UpdateProductDto
        group.MapPut("/{id:int}", async (int id, [FromBody] UpdateProductDto updateDto, AppDbContext db) =>
        {
            var existingProduct = await db.Products
                .Include(p => p.Dimensions)
                .Include(p => p.Meta)
                .Include(p => p.Reviews) // Include collections to modify them
                .Include(p => p.Tags)
                .Include(p => p.Images)
                .FirstOrDefaultAsync(p => p.Id == id);

            if (existingProduct is null)
            {
                return Results.NotFound($"Prodotto con ID {id} non trovato.");
            }

            // Aggiorna le proprietà principali dal DTO
            existingProduct.Title = updateDto.Title;
            existingProduct.Description = updateDto.Description;
            existingProduct.Category = updateDto.Category;
            existingProduct.Price = updateDto.Price;
            existingProduct.DiscountPercentage = updateDto.DiscountPercentage;
            existingProduct.Rating = updateDto.Rating;
            existingProduct.Stock = updateDto.Stock;
            existingProduct.Brand = updateDto.Brand;
            existingProduct.Sku = updateDto.Sku;
            existingProduct.Weight = updateDto.Weight;
            existingProduct.WarrantyInformation = updateDto.WarrantyInformation;
            existingProduct.ShippingInformation = updateDto.ShippingInformation;
            existingProduct.AvailabilityStatus = updateDto.AvailabilityStatus;
            existingProduct.ReturnPolicy = updateDto.ReturnPolicy;
            existingProduct.MinimumOrderQuantity = updateDto.MinimumOrderQuantity;
            existingProduct.Thumbnail = updateDto.Thumbnail;

            // Aggiorna Dimensions (se presente nel DTO)
            if (updateDto.Dimensions != null)
            {
                if (existingProduct.Dimensions != null)
                {
                    // Aggiorna esistente
                    existingProduct.Dimensions.Width = updateDto.Dimensions.Width;
                    existingProduct.Dimensions.Height = updateDto.Dimensions.Height;
                    existingProduct.Dimensions.Depth = updateDto.Dimensions.Depth;
                }
                else
                {
                    // Crea nuovo
                    existingProduct.Dimensions = new ProductDimensions
                    {
                        Width = updateDto.Dimensions.Width,
                        Height = updateDto.Dimensions.Height,
                        Depth = updateDto.Dimensions.Depth
                        // ProductId verrà impostato da EF Core
                    };
                }
            }
            else if (existingProduct.Dimensions != null)
            {
                // Rimuovi se non presente nel DTO ma esistente nel DB
                db.Remove(existingProduct.Dimensions);
                existingProduct.Dimensions = null;
            }

            // Aggiorna Meta (solo UpdatedAt)
            if (existingProduct.Meta != null)
            {
                existingProduct.Meta.UpdatedAt = DateTime.UtcNow;
            }
            else
            {
                // Se per qualche motivo Meta non esiste, crealo (potrebbe indicare un problema)
                existingProduct.Meta = new ProductMeta { CreatedAt = DateTime.UtcNow, UpdatedAt = DateTime.UtcNow };
            }

            // Sostituisci le collezioni (approccio comune per PUT)
            // Rimuovi esistenti dalle collezioni caricate
            existingProduct.Reviews.Clear();
            existingProduct.Tags.Clear();
            existingProduct.Images.Clear();

            // Aggiungi nuovi dal DTO (se presenti)
            if (updateDto.Reviews != null)
            {
                foreach (var reviewDto in updateDto.Reviews)
                {
                    existingProduct.Reviews.Add(new ProductReview
                    {
                        Rating = reviewDto.Rating,
                        Comment = reviewDto.Comment,
                        Date = reviewDto.Date,
                        ReviewerName = reviewDto.ReviewerName,
                        ReviewerEmail = reviewDto.ReviewerEmail
                        // ProductId verrà impostato da EF Core
                    });
                }
            }

            if (updateDto.Tags != null)
            {
                foreach (var tagDto in updateDto.Tags)
                {
                    existingProduct.Tags.Add(new ProductTag
                    {
                        Value = tagDto.Value
                        // ProductId verrà impostato da EF Core
                    });
                }
            }

            if (updateDto.Images != null)
            {
                foreach (var imageDto in updateDto.Images)
                {
                    existingProduct.Images.Add(new ProductImage
                    {
                        Url = imageDto.Url
                        // ProductId verrà impostato da EF Core
                    });
                }
            }

            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException ex)
            {
                Console.Error.WriteLine($"Concurrency error updating product {id}: {ex.Message}");
                return Results.Conflict($"Errore di concorrenza nell'aggiornamento del prodotto {id}. Il record potrebbe essere stato modificato da un altro utente.");
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Database error updating product {id}: {ex.Message}");
                return Results.Problem($"Errore interno del server durante l'aggiornamento del database.", statusCode: StatusCodes.Status500InternalServerError);
            }

            // Ricarica il prodotto aggiornato per mapparlo al DTO di risposta
            var updatedResult = await db.Products
               .AsNoTracking()
               .Include(p => p.Dimensions)
               .Include(p => p.Meta)
               .Include(p => p.Reviews)
               .Include(p => p.Tags)
               .Include(p => p.Images)
               .FirstOrDefaultAsync(p => p.Id == id);

            if (updatedResult == null)
            {
                // Anche questo non dovrebbe accadere
                return Results.Problem("Errore durante il recupero del prodotto dopo l'aggiornamento.", statusCode: StatusCodes.Status500InternalServerError);
            }

            var updatedResultDto = MapProductToDto(updatedResult); // Mappa a DTO

            return Results.Ok(updatedResultDto);
        })
        .WithName("UpdateProduct")
        .WithSummary("Aggiorna un prodotto esistente")
        .WithDescription("Aggiorna completamente un prodotto esistente usando un DTO (incluse relazioni uno-a-uno e uno-a-molti). ATTENZIONE: Le collezioni (Reviews, Tags, Images) vengono sostituite, non unite.")
        .Accepts<UpdateProductDto>("application/json") // Modificato tipo di input
        .Produces<ProductDto>(StatusCodes.Status200OK) // Modificato tipo di ritorno
        .Produces(StatusCodes.Status404NotFound)
        .Produces(StatusCodes.Status400BadRequest)
        .ProducesProblem(StatusCodes.Status500InternalServerError)
        .ProducesProblem(StatusCodes.Status409Conflict)
        .ProducesValidationProblem();

        // DELETE /products/{id} - Elimina un prodotto (invariato, non usa DTO)
        group.MapDelete("/{id:int}", async (int id, AppDbContext db) =>
        {
            // Nota: Potremmo voler caricare le relazioni per logica di business prima di eliminare,
            // ma per la semplice eliminazione basta FindAsync.
            var product = await db.Products.FindAsync(id);
            if (product is null)
            {
                return Results.NotFound($"Prodotto con ID {id} non trovato.");
            }
            db.Products.Remove(product);
            await db.SaveChangesAsync();
            return Results.NoContent();
        })
        .WithName("DeleteProduct")
        .WithSummary("Elimina un prodotto")
        .WithDescription("Elimina un prodotto tramite il suo ID. Il comportamento sulle tabelle correlate (Dimensions, Meta, Reviews, Tags, Images) dipende dalla configurazione OnDelete nel DbContext (Cascade o SetNull).")
        .Produces(StatusCodes.Status204NoContent)
        .Produces(StatusCodes.Status404NotFound);


        return group;

    }

}

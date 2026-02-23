// Data/AppDbContext.cs
using Microsoft.EntityFrameworkCore;
using MinimalApiCrudSqlite.Models;

namespace MinimalApiCrudSqlite.Data
{
    /// <summary>
    /// Contesto del database per l'applicazione (con tabelle separate per Dimensions e Meta).
    /// </summary>
    public class AppDbContext : DbContext
    {
        public DbSet<Product> Products { get; set; }
        public DbSet<ProductReview> Reviews { get; set; }
        public DbSet<ProductTag> Tags { get; set; }
        public DbSet<ProductImage> Images { get; set; }

        // Aggiunti DbSet per le nuove tabelle
        public DbSet<ProductDimensions> Dimensions { get; set; }
        public DbSet<ProductMeta> Metas { get; set; } // Nome plurale per convenzione

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configura l'entità Product
            modelBuilder.Entity<Product>(entity =>
            {
                entity.Property(p => p.Price).HasColumnType("decimal(18,2)");

                // Rimosse le configurazioni .OwnsOne()

                // Configura la relazione uno-a-uno con ProductDimensions
                // Un Product ha un (opzionale) ProductDimensions.
                // La FK 'ProductDimensionsId' è in Product.
                entity.HasOne(p => p.Dimensions)
                      .WithOne() // Non specifichiamo navigation property inversa in Dimensions
                      .HasForeignKey<Product>(p => p.ProductDimensionsId) // Specifica la FK in Product
                      .OnDelete(DeleteBehavior.SetNull); // O Cascade se vuoi cancellare Dimensions quando Product viene cancellato

                // Configura la relazione uno-a-uno con ProductMeta
                // Un Product ha un (opzionale) ProductMeta.
                // La FK 'ProductMetaId' è in Product.
                entity.HasOne(p => p.Meta)
                      .WithOne() // Non specifichiamo navigation property inversa in Meta
                      .HasForeignKey<Product>(p => p.ProductMetaId) // Specifica la FK in Product
                      .OnDelete(DeleteBehavior.SetNull); // O Cascade

                // Configura le relazioni uno-a-molti (invariate)
                entity.HasMany(p => p.Reviews)
                      .WithOne()
                      .HasForeignKey(r => r.ProductId)
                      .OnDelete(DeleteBehavior.Cascade);

                entity.HasMany(p => p.Tags)
                      .WithOne()
                      .HasForeignKey(t => t.ProductId)
                      .OnDelete(DeleteBehavior.Cascade);

                entity.HasMany(p => p.Images)
                      .WithOne()
                      .HasForeignKey(i => i.ProductId)
                      .OnDelete(DeleteBehavior.Cascade);

            });

            modelBuilder.Entity<ProductReview>(entity =>
            {
                entity.Property(r => r.Date).HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            // Potrebbe essere utile aggiungere indici sulle FK in Product
            modelBuilder.Entity<Product>()
                .HasIndex(p => p.ProductDimensionsId)
                .IsUnique(); // Assicura che ogni Dimensions sia collegato a un solo Product

            modelBuilder.Entity<Product>()
                .HasIndex(p => p.ProductMetaId)
                .IsUnique(); // Assicura che ogni Meta sia collegato a un solo Product

        }
    }
}

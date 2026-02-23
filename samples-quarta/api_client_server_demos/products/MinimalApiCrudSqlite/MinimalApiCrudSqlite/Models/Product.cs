// Models/Product.cs
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;

namespace MinimalApiCrudSqlite.Models
{
    /// <summary>
    /// Rappresenta un prodotto nel sistema (con Dimensions/Meta in tabelle separate).
    /// </summary>
    public class Product
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }

        [Required(ErrorMessage = "Il titolo è obbligatorio.")]
        [MaxLength(100)]
        public string? Title { get; set; }

        [MaxLength(500)]
        public string? Description { get; set; }

        [MaxLength(50)]
        public string? Category { get; set; }

        [Range(0, double.MaxValue)]
        [Column(TypeName = "decimal(18,2)")]
        public decimal Price { get; set; }

        [Range(0, 100)]
        public double DiscountPercentage { get; set; }

        [Range(0, 5)]
        public double Rating { get; set; }

        [Range(0, int.MaxValue)]
        public int Stock { get; set; }

        [MaxLength(50)]
        public string? Brand { get; set; }

        [MaxLength(50)]
        public string? Sku { get; set; }

        [Range(0, double.MaxValue)]
        public double Weight { get; set; }

        [MaxLength(100)]
        public string? WarrantyInformation { get; set; }

        [MaxLength(100)]
        public string? ShippingInformation { get; set; }

        [MaxLength(50)]
        public string? AvailabilityStatus { get; set; }

        [MaxLength(100)]
        public string? ReturnPolicy { get; set; }

        [Range(1, int.MaxValue)]
        public int MinimumOrderQuantity { get; set; }

        [Url]
        public string? Thumbnail { get; set; }

        // --- Foreign Keys e Navigation Properties per Relazioni ---

        // Relazione uno-a-uno con ProductDimensions
        public int? ProductDimensionsId { get; set; } // Chiave esterna (nullable se un prodotto può non avere dimensioni)
        public virtual ProductDimensions? Dimensions { get; set; } // Navigation property

        // Relazione uno-a-uno con ProductMeta
        public int? ProductMetaId { get; set; } // Chiave esterna (nullable se un prodotto può non avere meta)
        public virtual ProductMeta? Meta { get; set; } // Navigation property

        // Relazione uno-a-molti con ProductTag (invariata)
        public virtual ICollection<ProductTag> Tags { get; set; } = new List<ProductTag>();

        // Relazione uno-a-molti con ProductReview (invariata)
        public virtual ICollection<ProductReview> Reviews { get; set; } = new List<ProductReview>();

        // Relazione uno-a-molti con ProductImage (invariata)
        public virtual ICollection<ProductImage> Images { get; set; } = new List<ProductImage>();
    }
}

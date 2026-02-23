using System.ComponentModel.DataAnnotations;
using System.Collections.Generic;

namespace MinimalApiCrudSqlite.ModelDto
{
    public class CreateProductDto
    {
        [Required(ErrorMessage = "Il titolo è obbligatorio.")]
        [MaxLength(100)]
        public string? Title { get; set; }

        [MaxLength(500)]
        public string? Description { get; set; }

        [MaxLength(50)]
        public string? Category { get; set; }

        [Range(0, double.MaxValue)]
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
        public int MinimumOrderQuantity { get; set; } = 1;

        [Url]
        public string? Thumbnail { get; set; }

        // Related DTOs (optional on creation)
        public ProductDimensionsDto? Dimensions { get; set; }
        // Meta is usually generated, so not included in Create DTO
        public ICollection<ProductTagDto>? Tags { get; set; }
        public ICollection<ProductReviewDto>? Reviews { get; set; }
        public ICollection<ProductImageDto>? Images { get; set; }
    }
}

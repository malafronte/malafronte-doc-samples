using System.Collections.Generic;

namespace MinimalApiCrudSqlite.ModelDto
{
    public class ProductDto
    {
        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Description { get; set; }
        public string? Category { get; set; }
        public decimal Price { get; set; }
        public double DiscountPercentage { get; set; }
        public double Rating { get; set; }
        public int Stock { get; set; }
        public string? Brand { get; set; }
        public string? Sku { get; set; }
        public double Weight { get; set; }
        public string? WarrantyInformation { get; set; }
        public string? ShippingInformation { get; set; }
        public string? AvailabilityStatus { get; set; }
        public string? ReturnPolicy { get; set; }
        public int MinimumOrderQuantity { get; set; }
        public string? Thumbnail { get; set; }

        // Related DTOs
        public ProductDimensionsDto? Dimensions { get; set; }
        public ProductMetaDto? Meta { get; set; }
        public ICollection<ProductTagDto> Tags { get; set; } = new List<ProductTagDto>();
        public ICollection<ProductReviewDto> Reviews { get; set; } = new List<ProductReviewDto>();
        public ICollection<ProductImageDto> Images { get; set; } = new List<ProductImageDto>();
    }
}

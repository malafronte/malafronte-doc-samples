using System.Text.Json.Serialization;

namespace ApiClient.Models
{
    /// <summary>
    /// Classe per la creazione di un nuovo prodotto.
    /// Basato sulla definizione del server.
    /// </summary>
    public class CreateProduct
    {
        [JsonPropertyName("title")]
        public string? Title { get; set; }

        [JsonPropertyName("description")]
        public string? Description { get; set; }

        [JsonPropertyName("category")]
        public string? Category { get; set; }

        [JsonPropertyName("price")]
        public decimal Price { get; set; }

        [JsonPropertyName("discountPercentage")]
        public double DiscountPercentage { get; set; }

        [JsonPropertyName("rating")]
        public double Rating { get; set; }

        [JsonPropertyName("stock")]
        public int Stock { get; set; }

        [JsonPropertyName("brand")]
        public string? Brand { get; set; }

        [JsonPropertyName("sku")]
        public string? Sku { get; set; }

        [JsonPropertyName("weight")]
        public double Weight { get; set; }

        [JsonPropertyName("warrantyInformation")]
        public string? WarrantyInformation { get; set; }

        [JsonPropertyName("shippingInformation")]
        public string? ShippingInformation { get; set; }

        [JsonPropertyName("availabilityStatus")]
        public string? AvailabilityStatus { get; set; }

        [JsonPropertyName("returnPolicy")]
        public string? ReturnPolicy { get; set; }

        [JsonPropertyName("minimumOrderQuantity")]
        public int MinimumOrderQuantity { get; set; } = 1;

        [JsonPropertyName("thumbnail")]
        public string? Thumbnail { get; set; }

        // Related Classes (optional on creation)
        // Nota: Usiamo le classi del namespace ApiClient.Models
        [JsonPropertyName("dimensions")]
        public ProductDimensions? Dimensions { get; set; }
        // Meta is usually generated, so not included in Create DTO
        [JsonPropertyName("tags")]
        public ICollection<ProductTag>? Tags { get; set; }
        [JsonPropertyName("reviews")]
        public ICollection<ProductReview>? Reviews { get; set; }
        [JsonPropertyName("images")]
        public ICollection<ProductImage>? Images { get; set; }
    }
}


using System.Text.Json.Serialization;

namespace ApiClientAuth.Models
{
    /// <summary>
    /// Classe per l'aggiornamento di un prodotto esistente.
    /// Basato sulla definizione del server.
    /// </summary>
    public class UpdateProduct
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
        public int MinimumOrderQuantity { get; set; }

        [JsonPropertyName("thumbnail")]
        public string? Thumbnail { get; set; }

        // Related Classes
        // Nota: Usiamo le classi del namespace ApiClient.Models
        [JsonPropertyName("dimensions")]
        public ProductDimensions? Dimensions { get; set; }
        // Meta is usually managed internally (e.g., UpdatedAt), so not included in Update DTO
        [JsonPropertyName("tags")]
        public ICollection<ProductTag>? Tags { get; set; }
        [JsonPropertyName("reviews")]
        public ICollection<ProductReview>? Reviews { get; set; }
        [JsonPropertyName("images")]
        public ICollection<ProductImage>? Images { get; set; }
    }
}

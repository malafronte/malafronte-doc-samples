using System.Text.Json.Serialization;

namespace ApiClient.Models;

/// <summary>
/// Classe per rappresentare un prodotto ricevuto dall'API.
/// </summary>
public class Product
{
    // L'ID è importante per GET, PUT, DELETE e nella risposta di POST
    [JsonPropertyName("id")]
    public int Id { get; set; }
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

    // Relazioni
    [JsonPropertyName("dimensions")]
    public ProductDimensions? Dimensions { get; set; }
    [JsonPropertyName("meta")]
    public ProductMeta? Meta { get; set; }
    [JsonPropertyName("tags")]
    public ICollection<ProductTag>? Tags { get; set; } = new List<ProductTag>(); // Cambiato in ICollection e inizializzato
    [JsonPropertyName("reviews")]
    public ICollection<ProductReview>? Reviews { get; set; } = new List<ProductReview>(); // Cambiato in ICollection e inizializzato
    [JsonPropertyName("images")]
    public ICollection<ProductImage>? Images { get; set; } = new List<ProductImage>(); // Cambiato in ICollection e inizializzato
}

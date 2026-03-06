using System.Text.Json.Serialization;

namespace ApiClientAuth.Models;

public class ProductImage
{
    [JsonPropertyName("url")]
    public string? Url { get; set; }
    [JsonPropertyName("productId")]
    public int ProductId { get; set; }
}

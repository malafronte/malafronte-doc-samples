using System.Text.Json.Serialization;

namespace ApiClientAuth.Models;

public class ProductMeta
{
    [JsonPropertyName("id")]
    public int Id { get; set; }
    [JsonPropertyName("createdAt")]
    public DateTime CreatedAt { get; set; }
    [JsonPropertyName("updatedAt")]
    public DateTime UpdatedAt { get; set; }
    [JsonPropertyName("barcode")]
    public string? Barcode { get; set; }
    [JsonPropertyName("qrCode")]
    public string? QrCode { get; set; }
}

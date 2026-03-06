using System.Text.Json.Serialization;

namespace ApiClientAuth.Models;

public class ProductTag
{
    [JsonPropertyName("value")]
    public string? Value { get; set; }
    // public int ProductId { get; set; }
}

using System.Text.Json.Serialization;

namespace ApiClient.Models;

public class ProductTag
{
    [JsonPropertyName("value")]
    public string? Value { get; set; }
    // public int ProductId { get; set; }
}

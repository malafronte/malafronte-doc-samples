using System.Text.Json.Serialization;

namespace ApiClientAuth.Models;

public class ProductDimensions
{
    [JsonPropertyName("id")]
    public int Id { get; set; }
    [JsonPropertyName("width")]
    public double Width { get; set; }
    [JsonPropertyName("height")]
    public double Height { get; set; }
    [JsonPropertyName("depth")]
    public double Depth { get; set; }
}

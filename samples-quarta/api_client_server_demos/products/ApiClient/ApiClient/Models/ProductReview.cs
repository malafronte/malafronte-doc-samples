using System.Text.Json.Serialization;

namespace ApiClient.Models;

public class ProductReview
{
    [JsonPropertyName("rating")]
    public int Rating { get; set; }
    [JsonPropertyName("comment")]
    public string? Comment { get; set; }
    [JsonPropertyName("date")]
    public DateTime Date { get; set; }
    [JsonPropertyName("reviewerName")]
    public string? ReviewerName { get; set; }
    [JsonPropertyName("reviewerEmail")]
    public string? ReviewerEmail { get; set; }
    // public int ProductId { get; set; } // Solitamente non necessario nel DTO di risposta annidato
}

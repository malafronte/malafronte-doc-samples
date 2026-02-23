using System;

namespace ApiClient.Models;

public class ProductReviewDto
{
    public int Rating { get; set; }
    public string? Comment { get; set; }
    public DateTime Date { get; set; }
    public string? ReviewerName { get; set; }
    public string? ReviewerEmail { get; set; }
    // public int ProductId { get; set; } // Solitamente non necessario nel DTO di risposta annidato
}

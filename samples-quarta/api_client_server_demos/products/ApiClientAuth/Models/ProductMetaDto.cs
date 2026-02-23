using System;

namespace ApiClient.Models;

public class ProductMetaDto
{
    // public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    public string? Barcode { get; set; }
    public string? QrCode { get; set; }
}

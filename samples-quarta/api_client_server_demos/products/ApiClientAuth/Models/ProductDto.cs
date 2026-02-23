using System;
using System.Text.Json.Serialization;
using System.Collections.Generic; // Aggiunto per ICollection

namespace ApiClient.Models;

/// <summary>
/// DTO per rappresentare un prodotto ricevuto dall'API.
/// </summary>
public class ProductDto
{
    // L'ID è importante per GET, PUT, DELETE e nella risposta di POST
    public int Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? Category { get; set; }
    public decimal Price { get; set; }
    public double DiscountPercentage { get; set; }
    public double Rating { get; set; }
    public int Stock { get; set; }
    public string? Brand { get; set; }
    public string? Sku { get; set; }
    public double Weight { get; set; }
    public string? WarrantyInformation { get; set; }
    public string? ShippingInformation { get; set; }
    public string? AvailabilityStatus { get; set; }
    public string? ReturnPolicy { get; set; }
    public int MinimumOrderQuantity { get; set; }
    public string? Thumbnail { get; set; }

    // Relazioni
    public ProductDimensionsDto? Dimensions { get; set; }
    public ProductMetaDto? Meta { get; set; }
    public ICollection<ProductTagDto>? Tags { get; set; } = new List<ProductTagDto>(); // Cambiato in ICollection e inizializzato
    public ICollection<ProductReviewDto>? Reviews { get; set; } = new List<ProductReviewDto>(); // Cambiato in ICollection e inizializzato
    public ICollection<ProductImageDto>? Images { get; set; } = new List<ProductImageDto>(); // Cambiato in ICollection e inizializzato
}

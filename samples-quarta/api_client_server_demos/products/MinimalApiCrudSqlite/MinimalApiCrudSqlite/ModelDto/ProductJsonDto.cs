using System;
using MinimalApiCrudSqlite.Models;

namespace MinimalApiCrudSqlite.ModelDto;

// DTO per mappare il prodotto JSON durante la deserializzazione
public class ProductJsonDto
{
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? Category { get; set; }
    public decimal Price { get; set; }
    public double DiscountPercentage { get; set; }
    public double Rating { get; set; }
    public int Stock { get; set; }
    public List<string>? Tags { get; set; }
    public string? Brand { get; set; }
    public string? Sku { get; set; }
    public double Weight { get; set; }
    public ProductDimensions? Dimensions { get; set; }
    public string? WarrantyInformation { get; set; }
    public string? ShippingInformation { get; set; }
    public string? AvailabilityStatus { get; set; }
    public List<ProductReview>? Reviews { get; set; }
    public string? ReturnPolicy { get; set; }
    public int MinimumOrderQuantity { get; set; }
    public ProductMeta? Meta { get; set; }
    public List<string>? Images { get; set; }
    public string? Thumbnail { get; set; }
}
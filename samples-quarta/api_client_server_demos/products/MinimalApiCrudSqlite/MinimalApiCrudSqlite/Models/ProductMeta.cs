using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalApiCrudSqlite.Models;

/// <summary>
/// Metadati associati a un prodotto (Tabella Separata).
/// </summary>
public class ProductMeta
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } // Chiave primaria per la tabella ProductMeta

    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    [MaxLength(50)]
    public string? Barcode { get; set; }

    [Url]
    public string? QrCode { get; set; }

    // Foreign key inversa verso Product (per relazione uno-a-uno)
    // public int ProductId { get; set; }
    // public Product Product { get; set; } = null!;
    // Nota: La FK può stare su uno dei due lati della relazione 1-1.
    // La metteremo su Product per semplicità.
}

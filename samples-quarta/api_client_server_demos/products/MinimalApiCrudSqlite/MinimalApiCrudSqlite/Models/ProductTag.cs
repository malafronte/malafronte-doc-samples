using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalApiCrudSqlite.Models;

/// <summary>
/// Rappresenta un tag associato a un prodotto.
/// </summary>
public class ProductTag
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } // Chiave primaria per il tag specifico del prodotto

    [Required]
    [MaxLength(50)]
    public string? Value { get; set; } // Il valore del tag (es. "beauty")

    // Foreign Key per il Prodotto a cui il tag è associato
    public int ProductId { get; set; }
    // Navigation property (opzionale, ma utile)
    // public Product Product { get; set; } = null!;
}
using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalApiCrudSqlite.Models;

/// <summary>
/// Rappresenta l'URL di un'immagine associata a un prodotto.
/// </summary>
public class ProductImage
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } // Chiave primaria per l'immagine specifica del prodotto

    [Required]
    [Url]
    public string? Url { get; set; } // L'URL dell'immagine

    // Foreign Key per il Prodotto a cui l'immagine è associata
    public int ProductId { get; set; }
    // Navigation property (opzionale, ma utile)
    // public Product Product { get; set; } = null!;
}

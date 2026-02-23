using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalApiCrudSqlite.Models;

/// <summary>
/// Rappresenta una recensione lasciata per un prodotto.
/// </summary>
public class ProductReview
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } // Chiave primaria per la recensione

    [Range(1, 5)]
    public int Rating { get; set; }

    [MaxLength(500)]
    public string? Comment { get; set; }

    public DateTime Date { get; set; }

    [MaxLength(100)]
    public string? ReviewerName { get; set; }

    [EmailAddress]
    [MaxLength(100)]
    public string? ReviewerEmail { get; set; }

    // Foreign Key per il Prodotto a cui la recensione è associata
    public int ProductId { get; set; }
    // Navigation property (opzionale, ma utile)
    // public Product Product { get; set; } = null!;
}
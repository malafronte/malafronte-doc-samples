using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MinimalApiCrudSqlite.Models;

/// <summary>
/// Rappresenta le dimensioni di un prodotto (Tabella Separata).
/// </summary>
public class ProductDimensions
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int Id { get; set; } // Chiave primaria per la tabella ProductDimensions

    public double Width { get; set; }
    public double Height { get; set; }
    public double Depth { get; set; }

    // Foreign key inversa verso Product (per relazione uno-a-uno)
    // public int ProductId { get; set; }
    // public Product Product { get; set; } = null!;
    // Nota: La FK può stare su uno dei due lati della relazione 1-1.
    // La metteremo su Product per semplicità.
}
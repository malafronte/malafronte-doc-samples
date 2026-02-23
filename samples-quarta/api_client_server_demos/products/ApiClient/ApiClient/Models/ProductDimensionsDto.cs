using System;

namespace ApiClient.Models;

public class ProductDimensionsDto
{
    // Nota: L'ID non è solitamente necessario nel DTO per l'input/output di Dimensions
    // public int Id { get; set; }
    public double Width { get; set; }
    public double Height { get; set; }
    public double Depth { get; set; }
}

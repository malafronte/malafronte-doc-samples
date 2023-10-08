namespace Romanzi.Model;
public class Personaggio
{
    public int PersonaggioId { get; set; }
    public string Nome { get; set; } = null!;
    public int RomanzoId { get; set; }
    public Romanzo Romanzo { get; set; } = null!;
    public string? Sesso { get; set; }
    public string? Ruolo { get; set; }

}

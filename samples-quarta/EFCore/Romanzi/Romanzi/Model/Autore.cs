namespace Romanzi.Model;
public class Autore
{
    public int AutoreId { get; set; }
    public string Nome { get; set; } = null!;
    public string Cognome { get; set; } = null!;
    public string? Nazionalità { get; set; }
    public List<Romanzo> Romanzi { get; set; } = null!;

}


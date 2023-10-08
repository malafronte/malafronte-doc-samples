namespace Romanzi.Model;
public class Romanzo
{
    public int RomanzoId { get; set; }
    public string Titolo { get; set; } = null!;
    public int AutoreId { get; set; }
    public Autore Autore { get; set; } = null!;
    public int? AnnoPubblicazione { get; set; }
    public List<Personaggio> Personaggi { get; set; } = null!;

}

namespace LinqAlMuseo;

public class Artista
{
    public int Id { get; set; }
    public string Nome { get; set; } = null!;
    public string Cognome { get; set; } = null!;
    public string? Nazionalita { get; set; }

    public override string ToString()
    {
        return string.Format($"[ID = {Id}, Nome = {Nome},  Cognome = {Cognome}, Nazionalità = {Nazionalita}]"); ;
    }

}

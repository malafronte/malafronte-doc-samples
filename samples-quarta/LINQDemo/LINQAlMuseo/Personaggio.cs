namespace LinqAlMuseo;

public class Personaggio
{
    public int Id { get; set; }
    public string Nome { get; set; } = null!;
    public int FkOperaId { get; set; }
    public override string ToString()
    {
        return string.Format($"[ID = {Id}, Nome = {Nome}, FkOperaId = {FkOperaId}]"); ;
    }
}


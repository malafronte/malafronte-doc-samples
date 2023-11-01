namespace DbUtilizziPC.Model;

public class Computer
{
    public int Id { get; set; }
    public string Modello { get; set; } = null!;
    public string Collocazione { get; set; } = null!;
    public List<Utilizza> Utilizzi { get; } = null!;
    //Skip Navigation Property
    public List<Studente> Studenti { get; } = null!;
    public override string ToString()
    {
        return $"{{{nameof(Id)} = {Id}, {nameof(Modello)} = {Modello}, {nameof(Collocazione)} = {Collocazione}}}";
    }
}

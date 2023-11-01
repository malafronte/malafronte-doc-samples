namespace DbUtilizziPC.Model;

public class Studente
{
    public int Id { get; set; }
    public string Nome { get; set; } = null!;
    public string Cognome { get; set; } = null!;
    //Foreign Key su Classe
    public int ClasseId { get; set; }
    //Navigation Property su Classe
    public Classe Classe { get; set; } = null !;
    //navigation property per Molti a Molti
    public List<Utilizza> Utilizzi { get; } = null!;
    //Skip Navigation Property
    public List<Computer> Computers { get; } = null!;
    public override string ToString()
    {
        return $"{{{nameof(Id)} = {Id}, {nameof(Nome)} = {Nome}, {nameof(Cognome)} = {Cognome}, {nameof(Classe)} = {Classe}}}";
    }
}

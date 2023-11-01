using Microsoft.EntityFrameworkCore;

namespace DbUtilizziPC.Model;
//https://learn.microsoft.com/en-us/ef/core/modeling/indexes?tabs=data-annotations#index-uniqueness
[Index(nameof(Nome), IsUnique = true)]
public class Classe
{
    public int Id { get; set; }
    public string Nome { get; set; } = null!;
    public string Aula { get; set; } = null!;
    //navigation property
    public ICollection<Studente> Studenti { get; set; } = null!;
    public override string ToString()
    {
        return $"{{{nameof(Id)} = {Id}, {nameof(Nome)} = {Nome}, {nameof(Aula)} = {Aula}}}";
    }
}

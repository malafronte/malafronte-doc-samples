using System.ComponentModel.DataAnnotations;

namespace Università.Model;
public class Docente
{
    //qui l'annotation è resa necessaria perché non si segue la convenzione sul nome della chiave
    [Key]
    public int CodDocente { get; set; }
    public string Nome { get; set; } = null!;
    public string Cognome { get; set; } = null!;
    public Dipartimento Dipartimento { get; set; }
    //NAVIGATION PROPERTY
    public ICollection<Corso> Corsi { get; set; } = null!;
}


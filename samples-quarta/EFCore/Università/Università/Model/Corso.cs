using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Università.Model;
public class Corso
{
    //qui l'annotation è resa necessaria perché non si segue la convenzione sul nome della chiave
    [Key]
    public int CodiceCorso { get; set; }
    public string Nome { get; set; } = null!;
    //qui l'annotation è resa necessaria perché non si segue la convenzione sul nome della chiave
    public int? CodDocente { get; set; }
    //NAVIGATION PROPERTY
    [ForeignKey("CodDocente")]
    public Docente? Docente { get; set; }

    //NAVIGATION PROPERTY PER MOLTI A MOLTI STUDENTI - CORSI
    //https://learn.microsoft.com/en-us/ef/core/modeling/relationships/navigations
    public ICollection<Frequenta> Frequenze { get; set; } = null!;
    //skip navigation - https://learn.microsoft.com/en-us/ef/core/modeling/relationships/many-to-many
    public ICollection<Studente> Studenti { get; set; } =null!;

}


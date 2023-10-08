using System.ComponentModel.DataAnnotations;

namespace Università.Model;

public class Studente
{
    //qui l'annotation è resa necessaria perché non si segue la convenzione sul nome della chiave
    [Key]
    public int Matricola { get; set; }
    public string Nome { get; set; } = null!;
    public string Cognome { get; set; } = null!;
    public int AnnoNascita { get; set; }

    //Chiave esterna
    public int CorsoLaureaId { get; set; }
    //NAVIGATION PROPERTY PER CHIAVE ESTERNA
    public CorsoLaurea CorsoLaurea { get; set; } = null!;

    //NAVIGATION PROPERTY PER MOLTI A MOLTI STUDENTI - CORSI
    public ICollection<Frequenta> Frequenze { get; set; } = null!;
    //skip navigation - https://learn.microsoft.com/en-us/ef/core/modeling/relationships/many-to-many
    public ICollection<Corso> Corsi { get; set; } = null!;

}


namespace Università.Model;
public class CorsoLaurea
{
    //Chiave primaria
    public int CorsoLaureaId { get; set; }

    public TipoLaurea TipoLaurea { get; set; }

    public Facoltà Facoltà { get; set; }

    //NAVIGATION PROPERTY
    public ICollection<Studente> Studenti { get; set; } = null!;
}


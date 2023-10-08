namespace Università.Model;

public class Frequenta
{
    //la chiave primaria è composta da Matricola e CodCorso tramite Fluent API
    //le chiavi esterne vanno configurate mediante Fluent API
    public int Matricola { get; set; }
    //NAVIGATION PROPERTY
    public Studente Studente { get; set; } = null!;
    public int CodCorso { get; set; }
    //NAVIGATION PROPERTY
    public Corso Corso { get; set; } = null!;


}

using GestioneFattureClienti.Model;
using Microsoft.EntityFrameworkCore;
namespace GestioneFattureClienti.Data;
public class FattureClientiContext : DbContext
{
    public DbSet<Fattura> Fatture { get; set; } = null!;
    public DbSet<Cliente> Clienti { get; set; } = null!;
    public string DbPath { get; }

    public FattureClientiContext()
    {
        //https://www.hanselman.com/blog/how-do-i-find-which-directory-my-net-core-console-application-was-started-in-or-is-running-from
        var folder = AppContext.BaseDirectory;
        //La BaseDirectory restituisce la cartella dove si trova l'assembly (.dll e .exe del programma compilato)
        //il database, per comodità, è inserito nella cartella di progetto, dove si trova anche il file Program.cs 
        var path = Path.Combine(folder, "../../../FattureClienti.db");
        DbPath = path;
    }
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        => optionsBuilder.UseSqlite($"Data Source={DbPath}");
}

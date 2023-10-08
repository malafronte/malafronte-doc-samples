using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Università.Model;

namespace Università.Data;

public class UniversitàContext : DbContext
{
    //creazione delle tabelle
    public DbSet<Studente> Studenti { get; set; } = null!;
    public DbSet<CorsoLaurea> CorsiLaurea { get; set; } = null!;
    public DbSet<Frequenta> Frequenze { get; set; } = null!;
    public DbSet<Corso> Corsi { get; set; } = null!;
    public DbSet<Docente> Docenti { get; set; } = null!;
    public string DbPath { get; }

    public UniversitàContext()
    {
        var dir = AppContext.BaseDirectory;
        var path = Path.Combine(dir, "../../../universita.db");
        DbPath = path;
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    => options.UseSqlite($"Data Source={DbPath}");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        //per gestire la conversione da Enumerativo a string:
        //https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions
        var converterTipoLaurea = new EnumToStringConverter<TipoLaurea>();
        var converterFacolta = new EnumToStringConverter<Facoltà>();
        var converterDipartimento = new EnumToStringConverter<Dipartimento>();
        modelBuilder
            .Entity<CorsoLaurea>()
            .Property(cl => cl.TipoLaurea)
            .HasConversion(converterTipoLaurea);
        modelBuilder
           .Entity<CorsoLaurea>()
           .Property(cl => cl.Facoltà)
           .HasConversion(converterFacolta);
        modelBuilder
           .Entity<Docente>()
           .Property(d => d.Dipartimento)
           .HasConversion(converterDipartimento);

        //https://learn.microsoft.com/en-us/ef/core/modeling/relationships/many-to-many
        modelBuilder.Entity<Corso>()
            .HasMany(c => c.Studenti)
            .WithMany(s => s.Corsi)
            .UsingEntity<Frequenta>
            (
            //chiave esterna su Studente
            left => left
            .HasOne(fr => fr.Studente)
            .WithMany(s => s.Frequenze)
            .HasForeignKey(fr => fr.Matricola),
            //chiave esterna su Corso
            right => right
            .HasOne(fr => fr.Corso)
            .WithMany(c => c.Frequenze)
            .HasForeignKey(fr => fr.CodCorso));
    }

}


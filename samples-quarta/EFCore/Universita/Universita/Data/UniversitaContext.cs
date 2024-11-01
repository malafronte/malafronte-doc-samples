﻿using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Universita.Model;

namespace Universita.Data;
public class UniversitaContext : DbContext
{
    //creazione delle tabelle
    public DbSet<Studente> Studenti { get; set; } = null!;
    public DbSet<CorsoLaurea> CorsiLaurea { get; set; } = null!;
    public DbSet<Frequenta> Frequenze { get; set; } = null!;
    public DbSet<Corso> Corsi { get; set; } = null!;
    public DbSet<Docente> Docenti { get; set; } = null!;
    public string DbPath { get; }
    public UniversitaContext()
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
            .HasForeignKey(fr => fr.CodCorso),
            //primary key - in realtà, avendo associato le chiavi esterne, EF Core sarebbe in grado di creare 
            //la primary key a partire dalla combinazione delle due foreigh key. In questo caso particolare
            //questa terza fluent API è ridondante, ma è riportata per mostrare come si potrebbe configurare manualmente
            //la chiave primaria
            k => k.HasKey(fr => new { fr.Matricola, fr.CodCorso }));

    }

}


using DbUtilizziPC.Model;
using Microsoft.EntityFrameworkCore;

namespace DbUtilizziPC.Data;
public class UtilizziPCContext:DbContext
{
    public DbSet<Classe> Classi { get; set; } = null!;
    public DbSet<Studente> Studenti { get; set; } = null!;
    public DbSet<Computer> Computers { get; set; } = null!;
    public DbSet<Utilizza> Utilizzi { get; set; } = null!;
    public string DbPath { get; }
    public UtilizziPCContext()
    {
        var cartellaApp = AppContext.BaseDirectory;
        DbPath = Path.Combine(cartellaApp, "../../../DbUtilizziPC.db");
    }
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite($"Data Source = {DbPath}");
    }
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Studente>()
            .HasMany(s => s.Computers)
            .WithMany(c => c.Studenti)
            .UsingEntity<Utilizza>(
            //left => left.HasOne(u => u.Computer).WithMany(c => c.Utilizzi).HasForeignKey(u => u.ComputerId),
            //right => right.HasOne(u => u.Studente).WithMany(s => s.Utilizzi).HasForeignKey(u => u.StudenteId),
            //k =>k.HasKey( u => new {u.ComputerId, u.StudenteId, u.DataOraInizioUtilizzo })
            );
    }
}

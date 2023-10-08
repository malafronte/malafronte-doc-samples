using Microsoft.EntityFrameworkCore;
using Romanzi.Model;

namespace Romanzi.Data;

public class RomanziContext : DbContext
{
    public DbSet<Personaggio> Personaggi { get; set; } = null!;
    public DbSet<Autore> Autori { get; set; } = null!;
    public DbSet<Romanzo> Romanzi { get; set; } = null!;
    public string DbPath { get; }

    public RomanziContext()
    {
        var appDir = AppContext.BaseDirectory;
        var path = Path.Combine(appDir, "../../../Romanzi.db");
        DbPath = path;
    }
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite($"Data Source = {DbPath}");
    }
}


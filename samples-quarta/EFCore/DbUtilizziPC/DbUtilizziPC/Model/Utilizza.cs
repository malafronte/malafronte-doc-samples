using Microsoft.EntityFrameworkCore;

namespace DbUtilizziPC.Model;

[PrimaryKey(nameof(StudenteId), nameof(ComputerId), nameof(DataOraInizioUtilizzo))]
public class Utilizza
{
    public int StudenteId { get; set; }
    public Studente Studente { get; set; } = null!;
    public int ComputerId { get; set; }
    public Computer Computer { get; set; } = null!;
    public DateTime DataOraInizioUtilizzo { get; set; }
    public DateTime? DataOraFineUtilizzo { get; set; }
    
    public override string ToString()
    {
        return $"{{{nameof(StudenteId)} = {StudenteId}, {nameof(ComputerId)} = {ComputerId}," +
            $" {nameof(DataOraInizioUtilizzo)} = {DataOraInizioUtilizzo}," +
            $" {nameof(DataOraFineUtilizzo)} = {DataOraFineUtilizzo}}}";
    }
}

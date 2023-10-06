namespace GestioneFattureClienti.Model;
public class Cliente
{
    public int ClienteId { get; set; }
    public string RagioneSociale { get; set; } = null!;
    public string PartitaIVA { get; set; } = null!;
    public string? Citta { get; set; }
    public string? Via { get; set; }
    public string? Civico { get; set; }
    public string? CAP { get; set; }
    public List<Fattura> Fatture { get; } = new List<Fattura>();

    public override string ToString()
    {
        return string.Format($"[{nameof(ClienteId)}= {ClienteId}, " +
            $"{nameof(RagioneSociale)} = {RagioneSociale}, " +
            $"{nameof(PartitaIVA)} = {PartitaIVA}, " +
            $"{nameof(Citta)} = {Citta}, " +
            $"{nameof(Via)} = {Via}, " +
            $"{nameof(Civico)} = {Civico}, " +
            $"{nameof(CAP)} = {CAP}]");
    }
}
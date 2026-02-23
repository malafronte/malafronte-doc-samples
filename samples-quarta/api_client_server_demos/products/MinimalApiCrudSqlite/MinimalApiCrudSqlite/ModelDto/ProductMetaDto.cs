namespace MinimalApiCrudSqlite.ModelDto
{
    public class ProductMetaDto
    {
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
        public string? Barcode { get; set; }
        public string? QrCode { get; set; }
    }
}

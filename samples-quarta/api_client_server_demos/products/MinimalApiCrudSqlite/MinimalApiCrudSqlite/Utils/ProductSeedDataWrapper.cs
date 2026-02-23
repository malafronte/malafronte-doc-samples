using System;
using MinimalApiCrudSqlite.ModelDto;

namespace MinimalApiCrudSqlite.Utils;

// --- Helper Class per Deserializzazione JSON Seed ---
public class ProductSeedDataWrapper
{
    public List<ProductJsonDto>? Products { get; set; }
}

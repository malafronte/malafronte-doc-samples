using Microsoft.EntityFrameworkCore;
using MinimalApiCrudSqlite.Data;
using MinimalApiCrudSqlite.Endpoints;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

// Il database verrà creato nel file 'products.db' nella directory dell'applicazione
var connectionString = builder.Configuration.GetConnectionString("SqliteConnection") ?? "Data Source=products.db";
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(connectionString));

// Aggiunta dei servizi per la documentazione API (Swagger/NSwag)
// NSwag fornisce generazione del documento OpenAPI e UI Swagger/ReDoc
builder.Services.AddEndpointsApiExplorer(); // Necessario per analizzare gli endpoint
builder.Services.AddOpenApiDocument(settings =>
{
    settings.Title = "Product API - Minimal API CRUD Sqlite";
    settings.Version = "v1";
    settings.Description = "API per la gestione di prodotti con persistenza su SQLite.";
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    // Middleware per servire il documento OpenAPI generato (swagger.json)
    app.UseOpenApi();
    // Middleware per servire la UI di Swagger (accessibile a /swagger)
    app.UseSwaggerUi(config =>
    {
        config.DocumentTitle = "Minimal API CRUD Sqlite v1";
        config.Path = "/swagger";
        config.DocumentPath = "/openapi/v1.json"; // Usa il documento generato da Microsoft.AspNetCore.OpenApi
        config.DocExpansion = "list";
    });
    // Middleware per servire la UI di ReDoc (alternativa a Swagger UI, accessibile a /redoc)
    app.UseReDoc(settings =>
    {
        settings.Path = "/redoc";
        settings.DocumentPath = "/openapi/v1.json";
    });
}

app.UseHttpsRedirection();

using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var dbContext = services.GetRequiredService<AppDbContext>();
        var logger = services.GetRequiredService<ILogger<Program>>();
        // Ottieni l'oggetto IConfiguration dai servizi
        var configuration = services.GetRequiredService<IConfiguration>();

        // Chiama il metodo statico passando anche la configurazione
        await DatabaseInitializer.InitializeAndSeedAsync(dbContext, logger, configuration);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "An error occurred during database initialization.");
        // throw;
    }
}

app.UseStaticFiles(); // Abilita la gestione dei file statici (es. immagini, CSS, JS)
app.UseDefaultFiles(); // Abilita la gestione dei file predefiniti (es. index.html)

app.MapGroup("/products") // Gruppo di endpoint per i prodotti
   .WithTags("Products") // Tag per Swagger
   .MapProductEndpoints(); // Mappa gli endpoint per i prodotti
app.Run();


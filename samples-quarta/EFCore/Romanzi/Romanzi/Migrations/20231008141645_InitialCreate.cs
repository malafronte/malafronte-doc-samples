using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Romanzi.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Autori",
                columns: table => new
                {
                    AutoreId = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", nullable: false),
                    Cognome = table.Column<string>(type: "TEXT", nullable: false),
                    Nazionalità = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Autori", x => x.AutoreId);
                });

            migrationBuilder.CreateTable(
                name: "Romanzi",
                columns: table => new
                {
                    RomanzoId = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Titolo = table.Column<string>(type: "TEXT", nullable: false),
                    AutoreId = table.Column<int>(type: "INTEGER", nullable: false),
                    AnnoPubblicazione = table.Column<int>(type: "INTEGER", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Romanzi", x => x.RomanzoId);
                    table.ForeignKey(
                        name: "FK_Romanzi_Autori_AutoreId",
                        column: x => x.AutoreId,
                        principalTable: "Autori",
                        principalColumn: "AutoreId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Personaggi",
                columns: table => new
                {
                    PersonaggioId = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", nullable: false),
                    RomanzoId = table.Column<int>(type: "INTEGER", nullable: false),
                    Sesso = table.Column<string>(type: "TEXT", nullable: true),
                    Ruolo = table.Column<string>(type: "TEXT", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Personaggi", x => x.PersonaggioId);
                    table.ForeignKey(
                        name: "FK_Personaggi_Romanzi_RomanzoId",
                        column: x => x.RomanzoId,
                        principalTable: "Romanzi",
                        principalColumn: "RomanzoId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Personaggi_RomanzoId",
                table: "Personaggi",
                column: "RomanzoId");

            migrationBuilder.CreateIndex(
                name: "IX_Romanzi_AutoreId",
                table: "Romanzi",
                column: "AutoreId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Personaggi");

            migrationBuilder.DropTable(
                name: "Romanzi");

            migrationBuilder.DropTable(
                name: "Autori");
        }
    }
}

using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Università.Migrations
{
    /// <inheritdoc />
    public partial class InitialMigrate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "CorsiLaurea",
                columns: table => new
                {
                    CorsoLaureaId = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    TipoLaurea = table.Column<string>(type: "TEXT", nullable: false),
                    Facoltà = table.Column<string>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_CorsiLaurea", x => x.CorsoLaureaId);
                });

            migrationBuilder.CreateTable(
                name: "Docenti",
                columns: table => new
                {
                    CodDocente = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", nullable: false),
                    Cognome = table.Column<string>(type: "TEXT", nullable: false),
                    Dipartimento = table.Column<string>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Docenti", x => x.CodDocente);
                });

            migrationBuilder.CreateTable(
                name: "Studenti",
                columns: table => new
                {
                    Matricola = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", nullable: false),
                    Cognome = table.Column<string>(type: "TEXT", nullable: false),
                    AnnoNascita = table.Column<int>(type: "INTEGER", nullable: false),
                    CorsoLaureaId = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Studenti", x => x.Matricola);
                    table.ForeignKey(
                        name: "FK_Studenti_CorsiLaurea_CorsoLaureaId",
                        column: x => x.CorsoLaureaId,
                        principalTable: "CorsiLaurea",
                        principalColumn: "CorsoLaureaId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "Corsi",
                columns: table => new
                {
                    CodiceCorso = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    Nome = table.Column<string>(type: "TEXT", nullable: false),
                    CodDocente = table.Column<int>(type: "INTEGER", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Corsi", x => x.CodiceCorso);
                    table.ForeignKey(
                        name: "FK_Corsi_Docenti_CodDocente",
                        column: x => x.CodDocente,
                        principalTable: "Docenti",
                        principalColumn: "CodDocente");
                });

            migrationBuilder.CreateTable(
                name: "Frequenze",
                columns: table => new
                {
                    Matricola = table.Column<int>(type: "INTEGER", nullable: false),
                    CodCorso = table.Column<int>(type: "INTEGER", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Frequenze", x => new { x.CodCorso, x.Matricola });
                    table.ForeignKey(
                        name: "FK_Frequenze_Corsi_CodCorso",
                        column: x => x.CodCorso,
                        principalTable: "Corsi",
                        principalColumn: "CodiceCorso",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Frequenze_Studenti_Matricola",
                        column: x => x.Matricola,
                        principalTable: "Studenti",
                        principalColumn: "Matricola",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Corsi_CodDocente",
                table: "Corsi",
                column: "CodDocente");

            migrationBuilder.CreateIndex(
                name: "IX_Frequenze_Matricola",
                table: "Frequenze",
                column: "Matricola");

            migrationBuilder.CreateIndex(
                name: "IX_Studenti_CorsoLaureaId",
                table: "Studenti",
                column: "CorsoLaureaId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Frequenze");

            migrationBuilder.DropTable(
                name: "Corsi");

            migrationBuilder.DropTable(
                name: "Studenti");

            migrationBuilder.DropTable(
                name: "Docenti");

            migrationBuilder.DropTable(
                name: "CorsiLaurea");
        }
    }
}

using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Persistence.Migrations
{
    /// <inheritdoc />
    public partial class updateDatabase : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.Sql(
                @"CREATE TABLE IF NOT EXISTS ""new_angajati"" (
        ""Username"" TEXT NOT NULL CONSTRAINT ""PK_angajati"" PRIMARY KEY,
        ""Nume"" TEXT NOT NULL,
        ""Parola"" TEXT NOT NULL,
        ""Id"" TEXT NULL
    );"
            );

            migrationBuilder.Sql(
                @"INSERT INTO ""new_angajati"" (""Username"", ""Nume"", ""Parola"") SELECT ""Username"", ""Nume"", ""Parola"" FROM ""angajati"";"
            );

            migrationBuilder.Sql(
                @"DROP TABLE ""angajati"";"
            );

            migrationBuilder.Sql(
                @"ALTER TABLE ""new_angajati"" RENAME TO ""angajati"";"
            );
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "angajati");
        }
    }
}

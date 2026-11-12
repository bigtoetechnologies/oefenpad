using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Oefenpad.DB.Migrations
{
    /// <inheritdoc />
    public partial class GameProgress : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "GameLevelProgress",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    ApplicationUserId = table.Column<string>(type: "TEXT", maxLength: 450, nullable: false),
                    Game = table.Column<string>(type: "TEXT", maxLength: 40, nullable: false),
                    LevelId = table.Column<string>(type: "TEXT", maxLength: 80, nullable: false),
                    Correct = table.Column<int>(type: "INTEGER", nullable: false),
                    Total = table.Column<int>(type: "INTEGER", nullable: false),
                    CompletedAt = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GameLevelProgress", x => x.Id);
                    table.ForeignKey(
                        name: "FK_GameLevelProgress_AspNetUsers_ApplicationUserId",
                        column: x => x.ApplicationUserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "GameSaves",
                columns: table => new
                {
                    Id = table.Column<int>(type: "INTEGER", nullable: false)
                        .Annotation("Sqlite:Autoincrement", true),
                    ApplicationUserId = table.Column<string>(type: "TEXT", maxLength: 450, nullable: false),
                    Game = table.Column<string>(type: "TEXT", maxLength: 40, nullable: false),
                    RoundId = table.Column<string>(type: "TEXT", maxLength: 32, nullable: false),
                    StateJson = table.Column<string>(type: "TEXT", nullable: false),
                    UpdatedAt = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GameSaves", x => x.Id);
                    table.ForeignKey(
                        name: "FK_GameSaves_AspNetUsers_ApplicationUserId",
                        column: x => x.ApplicationUserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_GameLevelProgress_ApplicationUserId_Game_LevelId",
                table: "GameLevelProgress",
                columns: new[] { "ApplicationUserId", "Game", "LevelId" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_GameSaves_ApplicationUserId_Game",
                table: "GameSaves",
                columns: new[] { "ApplicationUserId", "Game" },
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "GameLevelProgress");

            migrationBuilder.DropTable(
                name: "GameSaves");
        }
    }
}

using Oefenpad.DTOs;

namespace Oefenpad.DB.Models;

/// <summary>
/// A finished level of a game that has named levels, such as the preposition
/// paths. One row per player, game and level; the best score is kept.
/// </summary>
public class GameLevelProgress
{
    public int Id { get; set; }

    public required string ApplicationUserId { get; set; }

    public ApplicationUser? ApplicationUser { get; set; }

    public required string Game { get; set; }

    public required string LevelId { get; set; }

    public int Correct { get; set; }

    public int Total { get; set; }

    public DateTime CompletedAt { get; set; }
}

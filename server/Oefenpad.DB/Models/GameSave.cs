using Oefenpad.DTOs;

namespace Oefenpad.DB.Models;

/// <summary>
/// A signed-in player's active round for one game. The state is the game's
/// private JSON, the same blob that would otherwise live only in
/// <c>RoundStore</c>; storing it lets a player leave and pick the puzzle up
/// later, even after a restart.
/// </summary>
public class GameSave
{
    public int Id { get; set; }

    public required string ApplicationUserId { get; set; }

    public ApplicationUser? ApplicationUser { get; set; }

    /// <summary>API segment, e.g. <c>wordsearch</c>.</summary>
    public required string Game { get; set; }

    /// <summary>The round this state belongs to, so a move can find it again.</summary>
    public required string RoundId { get; set; }

    public required string StateJson { get; set; }

    public DateTime UpdatedAt { get; set; }
}

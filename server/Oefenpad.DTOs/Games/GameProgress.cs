namespace Oefenpad.DTOs.Games;

/// <summary>A saved, resumable round: its id and the game's private state JSON.</summary>
public sealed record SavedGame(string RoundId, string StateJson);

/// <summary>A finished level and the best score the player reached on it.</summary>
public sealed record LevelProgress(int Correct, int Total);

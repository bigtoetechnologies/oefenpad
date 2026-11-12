using Oefenpad.DTOs.Games;

namespace Oefenpad.Contracts.Interfaces.Services;

/// <summary>
/// The account's copy of game progress. Every method answers the anonymous
/// player with nothing: progress is only written and read for a signed-in
/// learner, and the games themselves keep working without an account.
/// </summary>
public interface IGameProgressService
{
    /// <summary>Whether there is an account to save progress for.</summary>
    bool IsSignedIn { get; }

    /// <summary>The player's live round for a game, or null when there is none.</summary>
    Task<SavedGame?> LoadSavedAsync(string game, CancellationToken cancellationToken = default);

    /// <summary>Stores the live round, replacing any earlier save for the same game.</summary>
    Task SaveStateAsync(
        string game,
        string roundId,
        string stateJson,
        CancellationToken cancellationToken = default);

    /// <summary>Forgets the live round, e.g. when the game is finished.</summary>
    Task ClearStateAsync(string game, CancellationToken cancellationToken = default);

    /// <summary>Records a finished level, keeping the best score seen so far.</summary>
    Task RecordLevelAsync(
        string game,
        string levelId,
        int correct,
        int total,
        CancellationToken cancellationToken = default);

    /// <summary>Finished levels keyed by level id, best score per level.</summary>
    Task<IReadOnlyDictionary<string, LevelProgress>> LoadLevelsAsync(
        string game,
        CancellationToken cancellationToken = default);
}

using Microsoft.EntityFrameworkCore;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB;
using Oefenpad.DB.Models;
using Oefenpad.DTOs.Games;

namespace Oefenpad.Services.Games;

/// <summary>
/// Writes and reads the signed-in player's game saves and level results. The
/// games call this through the API; an anonymous player is quietly ignored so
/// the same code path serves accounts and guests.
/// </summary>
public sealed class GameProgressService(
    IOefenpadContextFactory contextFactory,
    ICurrentUserService currentUser) : IGameProgressService
{
    public bool IsSignedIn => currentUser.IsAuthenticated && currentUser.UserId is not null;

    public async Task<SavedGame?> LoadSavedAsync(string game, CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || currentUser.UserId is not { } userId)
            return null;

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        return await context.GameSaves
            .AsNoTracking()
            .Where(save => save.ApplicationUserId == userId && save.Game == game)
            .Select(save => new SavedGame(save.RoundId, save.StateJson))
            .FirstOrDefaultAsync(cancellationToken);
    }

    public async Task SaveStateAsync(
        string game,
        string roundId,
        string stateJson,
        CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || currentUser.UserId is not { } userId)
            return;

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        var save = await context.GameSaves
            .FirstOrDefaultAsync(
                row => row.ApplicationUserId == userId && row.Game == game,
                cancellationToken);

        if (save is null)
        {
            context.GameSaves.Add(new GameSave
            {
                ApplicationUserId = userId,
                Game = game,
                RoundId = roundId,
                StateJson = stateJson,
                UpdatedAt = DateTime.UtcNow
            });
        }
        else
        {
            save.RoundId = roundId;
            save.StateJson = stateJson;
            save.UpdatedAt = DateTime.UtcNow;
        }

        // Two tabs, or a double-submitted move, can both find no row and both
        // insert. The unique index then fails the loser, which would surface as a
        // 500 on an ordinary move, so retry that as the update it meant to be.
        try
        {
            await context.SaveChangesAsync(cancellationToken);
        }
        catch (DbUpdateException) when (save is null)
        {
            await using var retry = await contextFactory.CreateContextAsync(cancellationToken);
            await retry.GameSaves
                .Where(row => row.ApplicationUserId == userId && row.Game == game)
                .ExecuteUpdateAsync(
                    row => row
                        .SetProperty(x => x.RoundId, roundId)
                        .SetProperty(x => x.StateJson, stateJson)
                        .SetProperty(x => x.UpdatedAt, DateTime.UtcNow),
                    cancellationToken);
        }
    }

    public async Task ClearStateAsync(string game, CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || currentUser.UserId is not { } userId)
            return;

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        await context.GameSaves
            .Where(save => save.ApplicationUserId == userId && save.Game == game)
            .ExecuteDeleteAsync(cancellationToken);
    }

    public async Task RecordLevelAsync(
        string game,
        string levelId,
        int correct,
        int total,
        CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || currentUser.UserId is not { } userId)
            return;

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        var progress = await context.GameLevelProgress
            .FirstOrDefaultAsync(
                row => row.ApplicationUserId == userId && row.Game == game && row.LevelId == levelId,
                cancellationToken);

        if (progress is null)
        {
            context.GameLevelProgress.Add(new GameLevelProgress
            {
                ApplicationUserId = userId,
                Game = game,
                LevelId = levelId,
                Correct = correct,
                Total = total,
                CompletedAt = DateTime.UtcNow
            });
        }
        else if (correct >= progress.Correct)
        {
            // Keep the best run; replaying a level must never lower the record.
            progress.Correct = correct;
            progress.Total = total;
            progress.CompletedAt = DateTime.UtcNow;
        }

        // Same race as SaveStateAsync: a concurrent insert wins the unique index
        // and this one must become an update rather than a 500.
        try
        {
            await context.SaveChangesAsync(cancellationToken);
        }
        catch (DbUpdateException) when (progress is null)
        {
            await using var retry = await contextFactory.CreateContextAsync(cancellationToken);
            await retry.GameLevelProgress
                .Where(row => row.ApplicationUserId == userId
                              && row.Game == game
                              && row.LevelId == levelId
                              && correct >= row.Correct)
                .ExecuteUpdateAsync(
                    row => row
                        .SetProperty(x => x.Correct, correct)
                        .SetProperty(x => x.Total, total)
                        .SetProperty(x => x.CompletedAt, DateTime.UtcNow),
                    cancellationToken);
        }
    }

    public async Task<IReadOnlyDictionary<string, LevelProgress>> LoadLevelsAsync(
        string game,
        CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || currentUser.UserId is not { } userId)
            return new Dictionary<string, LevelProgress>();

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        var rows = await context.GameLevelProgress
            .AsNoTracking()
            .Where(progress => progress.ApplicationUserId == userId && progress.Game == game)
            .Select(progress => new
            {
                progress.LevelId,
                progress.Correct,
                progress.Total
            })
            .ToListAsync(cancellationToken);

        return rows.ToDictionary(
            row => row.LevelId,
            row => new LevelProgress(row.Correct, row.Total),
            StringComparer.Ordinal);
    }
}

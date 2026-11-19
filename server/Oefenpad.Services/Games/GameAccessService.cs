using Oefenpad.Contracts.Interfaces.Services;

namespace Oefenpad.Services.Games;

/// <summary>
/// Why a level is closed to the current visitor. The client renders the two
/// differently: one offers sign-up, the other asks for the previous level.
/// </summary>
public static class GameLock
{
    public const string Account = "account";
    public const string Progress = "progress";
    public const string Premium = "premium";

    public static string Message(string reason) => reason switch
    {
        Progress => "Haal eerst het vorige niveau.",
        Premium => "Hiervoor komt een abonnement.",
        _ => "Maak een account om dit niveau te openen."
    };
}

/// <summary>
/// What the current visitor may start. Gating is a brake on scripted scraping,
/// not a paywall engine: a guest reaches the free slice of a game, and a
/// signed-in learner reaches the next level once the previous one is finished.
/// </summary>
public sealed class GameAccess
{
    private readonly IReadOnlyDictionary<string, string> _locks;

    private GameAccess(bool isSignedIn, IReadOnlyDictionary<string, string>? locks)
    {
        IsSignedIn = isSignedIn;
        _locks = locks ?? new Dictionary<string, string>();
    }

    public bool IsSignedIn { get; }

    public static GameAccess Open(bool isSignedIn) => new(isSignedIn, null);

    public static GameAccess WithLocks(bool isSignedIn, IReadOnlyDictionary<string, string> locks) =>
        new(isSignedIn, locks);

    /// <summary>The lock reason for a level, or null when it can be started.</summary>
    public string? ReasonFor(string? levelId) =>
        levelId is not null && _locks.TryGetValue(levelId, out var reason) ? reason : null;

    /// <summary>
    /// The same options, with the closed levels marked. Every other field is
    /// passed through untouched, so a game with no policy is unaffected.
    /// </summary>
    public GameOptions Annotate(GameOptions options) =>
        new(
            options.Categories,
            options.Levels
                .Select(level => ReasonFor(level.Id) is { } reason
                    ? level with { Locked = true, LockReason = reason }
                    : level)
                .ToList());
}

/// <summary>
/// The visitor tiers for Voorzetselpaden. The tiers follow the CEFR bands the
/// content is written in: A0 is open to everyone, A1, A2 and the A2 pairs need
/// an account, and B1 and up will need a paid plan. A band is the unit because the game grows a
/// band at a time — an index-based cut would move every time a band lands.
/// Within a tier a level also waits for the one before it, and the first level
/// of a band opens the band. Finishing counts as passing: the point of the gate
/// is to make a crawler play, not to grade the player.
/// </summary>
public static class PrepositionAccess
{
    /// <summary>The band every visitor may practise.</summary>
    public const string FreeBand = "a0";

    /// <summary>The bands that need an account. Anything above them needs a plan.</summary>
    public static readonly string[] AccountBands = ["a1", "a2", "a2-pairs"];

    public enum Tier { Free, Account, Premium }

    /// <summary>
    /// Which tier a level belongs to. A level without a band is left free, so a
    /// new or unlabelled band never arrives locked by accident.
    /// </summary>
    public static Tier TierOf(Level level) => level.Band?.Trim().ToLowerInvariant() switch
    {
        null or "" or FreeBand => Tier.Free,
        var band when AccountBands.Contains(band) => Tier.Account,
        _ => Tier.Premium
    };

    /// <summary>
    /// Per-level lock reason, keyed by level id. A null <paramref name="passed"/>
    /// means the account has finished nothing.
    /// </summary>
    public static IReadOnlyDictionary<string, string> Evaluate(
        IReadOnlyList<Level> levels,
        IReadOnlySet<string>? passed,
        bool isSignedIn,
        bool isPremium = false)
    {
        var locks = new Dictionary<string, string>(StringComparer.Ordinal);

        for (var i = 0; i < levels.Count; i++)
        {
            var level = levels[i];
            var tier = TierOf(level);

            if (tier == Tier.Free) continue;

            // A paid level is closed without a plan even when it was finished
            // before: progress survives, access does not.
            if (tier == Tier.Premium && !isPremium)
            {
                locks[level.Id] = GameLock.Premium;
                continue;
            }

            if (!isSignedIn)
            {
                locks[level.Id] = GameLock.Account;
                continue;
            }

            if (passed is null) { locks[level.Id] = GameLock.Progress; continue; }

            // A level that was finished stays playable, finishing the one
            // before opens this one, and the first level of a band is where
            // that band starts. Anything else waits.
            var opensBand = i == 0
                || !string.Equals(levels[i - 1].Band, level.Band, StringComparison.OrdinalIgnoreCase);

            if (opensBand || passed.Contains(level.Id) || passed.Contains(levels[i - 1].Id)) continue;

            locks[level.Id] = GameLock.Progress;
        }

        return locks;
    }
}

/// <summary>
/// Reads the current visitor's progress and turns it into a <see cref="GameAccess"/>.
/// Kept out of the game services so they stay singleton and free of accounts.
/// </summary>
public sealed class GameAccessService(GameContent content, IGameProgressService progress)
{
    public async Task<GameAccess> ForAsync(string game, CancellationToken cancellationToken = default)
    {
        if (!string.Equals(game, PrepositionsService.Id, StringComparison.OrdinalIgnoreCase))
            return GameAccess.Open(progress.IsSignedIn);

        var passed = await progress.LoadLevelsAsync(game, cancellationToken);

        // No payment system yet, so nobody holds a plan and the paid slice is
        // shut. When subscriptions ship, read the entitlement here; the tier
        // boundary and the client rendering already exist.
        const bool isPremium = false;

        var locks = PrepositionAccess.Evaluate(
            content.Prepositions.Levels,
            passed.Keys.ToHashSet(StringComparer.Ordinal),
            progress.IsSignedIn,
            isPremium);

        return GameAccess.WithLocks(progress.IsSignedIn, locks);
    }
}

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
/// The visitor tiers for Voorzetselpaden. The first levels are open to
/// everyone, the next six need an account, and everything after that needs a
/// paid plan. Within a tier a level also waits for the one before it. Finishing
/// counts as passing: the point of the gate is to make a crawler play, not to
/// grade the player.
/// </summary>
public static class PrepositionAccess
{
    public const int FreeLevels = 3;

    /// <summary>
    /// The index of the first level that needs a paid plan. Levels 0–2 are free,
    /// 3–8 need an account (six levels), 9 and up need a subscription. There is
    /// no payment system yet, so no visitor is premium and that slice stays shut.
    /// </summary>
    public const int PremiumFrom = 9;

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
            if (i < FreeLevels) continue;

            var id = levels[i].Id;

            // A paid level is closed without a plan even when it was finished
            // before: progress survives, access does not.
            if (i >= PremiumFrom && !isPremium)
            {
                locks[id] = GameLock.Premium;
                continue;
            }

            if (!isSignedIn)
            {
                locks[id] = GameLock.Account;
                continue;
            }

            if (passed is null) { locks[id] = GameLock.Progress; continue; }

            // A level that was finished stays playable, and finishing the one
            // before opens this one. Anything else waits.
            if (passed.Contains(id) || passed.Contains(levels[i - 1].Id)) continue;

            locks[id] = GameLock.Progress;
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

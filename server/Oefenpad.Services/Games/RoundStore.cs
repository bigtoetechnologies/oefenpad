using System.Collections.Concurrent;

namespace Oefenpad.Services.Games;

/// <summary>
/// Where a round's private state lives between requests. Deliberately in memory:
/// the answer is never in the browser, and a restart simply ends open rounds.
/// </summary>
public sealed class RoundStore
{
    private static readonly TimeSpan DefaultLifetime = TimeSpan.FromHours(3);
    private const int MaxRounds = 4_000;

    private readonly ConcurrentDictionary<string, Round> _rounds = new(StringComparer.Ordinal);

    public string Save(string game, object state, TimeSpan? lifetime = null)
    {
        if (_rounds.Count > MaxRounds) CleanUp();

        var id = Guid.NewGuid().ToString("N");
        _rounds[id] = new Round(game, state, DateTimeOffset.UtcNow + (lifetime ?? DefaultLifetime));
        return id;
    }

    public object? Get(string id, string game)
    {
        if (!_rounds.TryGetValue(id, out var round)) return null;

        if (round.Expires < DateTimeOffset.UtcNow)
        {
            _rounds.TryRemove(id, out _);
            return null;
        }

        return string.Equals(round.Game, game, StringComparison.OrdinalIgnoreCase)
            ? round.State
            : null;
    }

    public void Remove(string id) => _rounds.TryRemove(id, out _);

    /// <summary>
    /// The gate that serialises moves on one round. A round's state is a shared
    /// mutable object and every game's Move is check-then-act on it, so two
    /// requests for the same round — a double tap, a retried POST — would
    /// otherwise interleave and corrupt it. Null when the round is unknown;
    /// the caller then falls through to its own expiry handling.
    /// </summary>
    public SemaphoreSlim? Gate(string id) =>
        _rounds.TryGetValue(id, out var round) ? round.Gate : null;

    private void CleanUp()
    {
        var now = DateTimeOffset.UtcNow;
        foreach (var (id, round) in _rounds)
        {
            if (round.Expires < now) _rounds.TryRemove(id, out _);
        }

        // Still full after expiry? Drop the oldest half rather than grow without bound.
        if (_rounds.Count <= MaxRounds) return;

        foreach (var id in _rounds
                     .OrderBy(x => x.Value.Expires)
                     .Take(_rounds.Count - MaxRounds / 2)
                     .Select(x => x.Key))
        {
            _rounds.TryRemove(id, out _);
        }
    }

    private sealed record Round(string Game, object State, DateTimeOffset Expires)
    {
        public SemaphoreSlim Gate { get; } = new(1, 1);
    }
}

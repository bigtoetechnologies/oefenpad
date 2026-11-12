using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// One game, server-authoritative. The client asks for a round, gets only what
/// it must render, and reports what the player did. It never receives the
/// answer bank, the full grid solution or the translation column.
/// </summary>
public interface IGameService
{
    /// <summary>API segment, e.g. <c>hangman</c>.</summary>
    string Game { get; }

    /// <summary>Categories and levels the player may choose, without any words.</summary>
    GameOptions Options();

    /// <summary>Dutch interface strings for this game.</summary>
    IReadOnlyDictionary<string, string> Texts();

    /// <summary>Starts a round and returns its opaque id plus the first view.</summary>
    RoundStart Start(JsonElement input);

    /// <summary>Applies one player action to a round and returns the new view.</summary>
    RoundMove Move(string roundId, JsonElement move);

    /// <summary>
    /// The private state of a live round as JSON, or null when the game cannot
    /// save it. Only the account store ever sees this; it never leaves the server.
    /// </summary>
    string? Export(string roundId);

    /// <summary>
    /// Rebuilds a live round from saved JSON and returns its new id and view.
    /// Throws <see cref="RoundExpiredException"/> when the blob cannot be used.
    /// </summary>
    RoundStart Resume(string stateJson);

    /// <summary>
    /// The named level a round belongs to, or null for games whose rounds are
    /// not levels. Used to record progress when a round is finished.
    /// </summary>
    string? LevelOf(string roundId);
}

/// <param name="Resume">Extra data only a resumed round needs, such as the
/// cells of words the player had already found.</param>
public sealed record RoundStart(string RoundId, object View, object? Resume = null);

/// <param name="Done">The round is finished.</param>
/// <param name="Correct">Whether the last action was correct, when it is judged.</param>
/// <param name="Explanation">Dutch feedback for the player, when there is any.</param>
/// <param name="Rejection">A non-scoring refusal, e.g. a card from the same panel.</param>
public sealed record RoundMove(
    object View,
    bool Done = false,
    bool? Correct = null,
    string? Explanation = null,
    int? CorrectCount = null,
    int? Total = null,
    string? Rejection = null);

public sealed record GameOptions(
    IReadOnlyList<GameCategory> Categories,
    IReadOnlyList<GameLevel> Levels);

public sealed record GameCategory(string Id, string Name, string Icon, int Count);

/// <param name="Size">Grid size or pair count, where the level has one.</param>
/// <param name="Locked">The current visitor may not start this level yet.</param>
/// <param name="LockReason">Why it is locked, when it is; see <see cref="GameLock"/>.</param>
public sealed record GameLevel(
    string Id,
    string Name,
    int? Size = null,
    string? Subtitle = null,
    bool Locked = false,
    string? LockReason = null);

public sealed class RoundExpiredException : Exception
{
    public RoundExpiredException()
        : base("Deze ronde bestaat niet meer. Start een nieuw spel.") { }
}

public sealed class InvalidMoveException : Exception
{
    public InvalidMoveException(string message) : base(message) { }
}

/// <summary>Shared plumbing for the per-game services.</summary>
public abstract class GameService : IGameService
{
    /// <summary>
    /// One options object for every round that is written to an account. Private
    /// state is still stored by the game itself, so the shape never reaches the browser.
    /// </summary>
    protected static readonly JsonSerializerOptions StorageJson = new(JsonSerializerDefaults.Web);

    protected GameService(GameContent content, RoundStore rounds)
    {
        Content = content;
        Rounds = rounds;
    }

    protected GameContent Content { get; }

    protected RoundStore Rounds { get; }

    public abstract string Game { get; }

    public virtual IReadOnlyDictionary<string, string> Texts() => Content.Texts(Game);

    public abstract GameOptions Options();

    public abstract RoundStart Start(JsonElement input);

    public abstract RoundMove Move(string roundId, JsonElement move);

    public abstract string? Export(string roundId);

    public abstract RoundStart Resume(string stateJson);

    protected RoundStart Store(
        object state,
        object view,
        object? resume = null,
        TimeSpan? lifetime = null) =>
        new(Rounds.Save(Game, state, lifetime), view, resume);

    protected T State<T>(string roundId) where T : class =>
        Rounds.Get(roundId, Game) as T
        ?? throw new RoundExpiredException();

    /// <summary>Serializes a round's state without losing its concrete type.</summary>
    protected static string ToJson(object state) =>
        JsonSerializer.Serialize(state, state.GetType(), StorageJson);

    public virtual string? LevelOf(string roundId) => null;

    /* ---------- interface strings ---------- */

    /// <summary>
    /// A Dutch interface string from the game's text bank, with placeholders
    /// replaced. Content stays in JSON; only the keys appear in code.
    /// </summary>
    protected string Text(string key, params (string Name, object? Value)[] values)
    {
        var bank = Texts();
        if (!bank.TryGetValue(key, out var text)) return key;

        foreach (var (name, value) in values)
            text = text.Replace("{" + name + "}", value?.ToString() ?? "");

        return text;
    }

    /* ---------- defensive JSON reading ---------- */

    protected static string? String(JsonElement body, string name)
    {
        if (body.ValueKind != JsonValueKind.Object) return null;
        return body.TryGetProperty(name, out var p) && p.ValueKind == JsonValueKind.String
            ? p.GetString()
            : null;
    }

    protected static int? Int(JsonElement body, string name)
    {
        if (body.ValueKind != JsonValueKind.Object) return null;
        return body.TryGetProperty(name, out var p) && p.ValueKind == JsonValueKind.Number
            ? p.GetInt32()
            : null;
    }

    protected static bool? Bool(JsonElement body, string name)
    {
        if (body.ValueKind != JsonValueKind.Object) return null;
        return body.TryGetProperty(name, out var p) &&
               (p.ValueKind == JsonValueKind.True || p.ValueKind == JsonValueKind.False)
            ? p.GetBoolean()
            : null;
    }

    protected static IReadOnlyList<JsonElement> Array(JsonElement body, string name)
    {
        if (body.ValueKind != JsonValueKind.Object) return System.Array.Empty<JsonElement>();
        return body.TryGetProperty(name, out var p) && p.ValueKind == JsonValueKind.Array
            ? p.EnumerateArray().ToList()
            : System.Array.Empty<JsonElement>();
    }

    /* ---------- shared helpers ---------- */

    protected static List<T> Shuffle<T>(IEnumerable<T> source)
    {
        var list = source.ToList();
        for (var i = list.Count - 1; i > 0; i--)
        {
            var j = Random.Shared.Next(i + 1);
            (list[i], list[j]) = (list[j], list[i]);
        }
        return list;
    }

    protected static T Pick<T>(IReadOnlyList<T> list) =>
        list[Random.Shared.Next(list.Count)];

    /// <summary>
    /// Name and icon are looked up by key, with a fallback, so a key that has no
    /// word-bank category still yields a usable entry instead of throwing. Image
    /// categories come from the image path, which need not match a word key.
    /// </summary>
    protected GameCategory Category(string key, int count) =>
        new(key, Content.CategoryName(key), Content.CategoryIcon(key), count);
}

/// <summary>Resolves an API segment to its game.</summary>
public sealed class GameRegistry
{
    private readonly Dictionary<string, IGameService> _services;

    public GameRegistry(IEnumerable<IGameService> services)
    {
        _services = services.ToDictionary(x => x.Game, StringComparer.OrdinalIgnoreCase);
    }

    public IGameService? For(string game) =>
        _services.TryGetValue(game, out var service) ? service : null;

    public IEnumerable<string> Games => _services.Keys.OrderBy(x => x, StringComparer.Ordinal);
}

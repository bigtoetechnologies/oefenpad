using System.Text.Json;

namespace Oefenpad.Resources.Games;

/// <summary>
/// Reads the game content banks that are embedded in this assembly.
/// Nothing here is published as a static file; a caller must go through the
/// game API, which only hands back the words belonging to one round.
/// </summary>
public static class GameData
{
    private const string Prefix = "Oefenpad.Resources.Games.Data.";

    private static readonly Lazy<IReadOnlyDictionary<string, string>> Files = new(LoadAll);

    /// <summary>Raw JSON for a bank, e.g. <c>words</c> or <c>texts.hangman</c>.</summary>
    public static string Json(string name) =>
        Files.Value.TryGetValue(name, out var json)
            ? json
            : throw new KeyNotFoundException($"Game data bank '{name}' is not embedded.");

    public static bool Exists(string name) => Files.Value.ContainsKey(name);

    public static IReadOnlyList<string> Names =>
        Files.Value.Keys.OrderBy(x => x, StringComparer.Ordinal).ToList();

    /// <summary>Deserialises a bank with the camelCase names used by the JSON files.</summary>
    public static T Load<T>(string name) =>
        JsonSerializer.Deserialize<T>(Json(name), Options)
        ?? throw new InvalidOperationException($"Game data bank '{name}' deserialised to null.");

    public static readonly JsonSerializerOptions Options = new()
    {
        PropertyNameCaseInsensitive = true
    };

    private static IReadOnlyDictionary<string, string> LoadAll()
    {
        var assembly = typeof(GameData).Assembly;
        var result = new Dictionary<string, string>(StringComparer.Ordinal);

        foreach (var resource in assembly.GetManifestResourceNames())
        {
            if (!resource.StartsWith(Prefix, StringComparison.Ordinal)) continue;
            if (!resource.EndsWith(".json", StringComparison.Ordinal)) continue;

            var name = resource[Prefix.Length..^".json".Length];
            using var stream = assembly.GetManifestResourceStream(resource)
                ?? throw new InvalidOperationException($"Cannot open '{resource}'.");
            using var reader = new StreamReader(stream);
            result[name] = reader.ReadToEnd();
        }

        return result;
    }
}

using Oefenpad.Resources.Games;

namespace Oefenpad.Services.Games;

/// <summary>
/// The content banks, loaded once from the embedded JSON. Only the services in
/// this folder see these objects; the API projects a round-sized view of them.
/// </summary>
public sealed class GameContent
{
    private readonly Dictionary<string, IReadOnlyDictionary<string, string>> _texts;

    public GameContent()
    {
        Categories = GameData.Load<Dictionary<string, WordCategory>>("words");
        WordImages = GameData.Load<Dictionary<string, string>>("wordimages");
        Prepositions = GameData.Load<PrepositionsData>("prepositions");
        Reels = GameData.Load<List<Reel>>("reels");
        Meta = GameData.Load<MetaData>("meta");

        _texts = new Dictionary<string, IReadOnlyDictionary<string, string>>(StringComparer.OrdinalIgnoreCase);
        foreach (var game in new[] { "hangman", "memory", "matching", "wordsearch", "prepositions", "storymachine" })
        {
            if (GameData.Exists($"texts.{game}"))
                _texts[game] = GameData.Load<Dictionary<string, string>>($"texts.{game}");
        }

        ImageItems = BuildImageItems();
        ImageByFile = ImageItems.ToDictionary(x => x.File, StringComparer.OrdinalIgnoreCase);
    }

    public IReadOnlyDictionary<string, WordCategory> Categories { get; }

    public IReadOnlyDictionary<string, string> WordImages { get; }

    public PrepositionsData Prepositions { get; }

    public IReadOnlyList<Reel> Reels { get; }

    public MetaData Meta { get; }

    /// <summary>Every word image that also has a Dutch word, once per file.</summary>
    public IReadOnlyList<ImageItem> ImageItems { get; }

    public IReadOnlyDictionary<string, ImageItem> ImageByFile { get; }

    /// <summary>Dutch interface strings for a game, or an empty table.</summary>
    public IReadOnlyDictionary<string, string> Texts(string game) =>
        _texts.TryGetValue(game, out var t)
            ? t
            : new Dictionary<string, string>();

    /// <summary>The Dutch label of a word category, falling back to its key.</summary>
    public string CategoryName(string key) =>
        Categories.TryGetValue(key, out var category) &&
        category.Label.TryGetValue("nl", out var name)
            ? name
            : key;

    public string CategoryIcon(string key) =>
        Categories.TryGetValue(key, out var category) && !string.IsNullOrWhiteSpace(category.Icon)
            ? category.Icon!
            : "🖼️";

    /// <summary>
    /// Categories that can be offered for an image-based game: at least one word
    /// with both an English key and a Dutch word that has a picture.
    /// </summary>
    public IEnumerable<(string Key, WordCategory Category, int Playable)> PlayableCategories(bool requireImage)
    {
        foreach (var (key, category) in Categories)
        {
            var playable = category.Words.Count(w =>
                !string.IsNullOrWhiteSpace(w.Nl) &&
                (!requireImage || (!string.IsNullOrWhiteSpace(w.En) && WordImages.ContainsKey(w.En!))));

            if (playable > 0) yield return (key, category, playable);
        }
    }

    /// <summary>Unique image items belonging to one category, or all of them.</summary>
    public IEnumerable<ImageItem> ImagesFor(string? category) =>
        string.IsNullOrEmpty(category) || category == "all"
            ? ImageItems
            : ImageItems.Where(x => x.Category == category);

    public string? ImageFor(WordEntry entry) =>
        entry.Img is not null
            ? entry.Img
            : entry.En is not null && WordImages.TryGetValue(entry.En, out var file)
                ? file
                : null;

    private List<ImageItem> BuildImageItems()
    {
        var byEnglish = new Dictionary<string, WordEntry>(StringComparer.Ordinal);
        foreach (var category in Categories.Values)
        {
            foreach (var entry in category.Words)
            {
                if (entry.En is null || string.IsNullOrWhiteSpace(entry.Nl)) continue;
                byEnglish.TryAdd(entry.En, entry);
            }
        }

        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var items = new List<ImageItem>();

        foreach (var (english, file) in WordImages)
        {
            if (!seen.Add(file)) continue;
            if (!byEnglish.TryGetValue(english, out var entry)) continue;

            var slash = file.IndexOf('/');
            var category = slash > 0 ? file[..slash] : "";
            items.Add(new ImageItem(file, english, entry.Nl!, category));
        }

        return items;
    }
}

public sealed record ImageItem(string File, string English, string Dutch, string Category);

/* ---------- word banks ---------- */

public sealed class WordCategory
{
    public string? Icon { get; set; }
    public Dictionary<string, string> Label { get; set; } = new();
    public List<WordEntry> Words { get; set; } = new();
}

public sealed class WordEntry
{
    public string? En { get; set; }
    public string? Nl { get; set; }
    public string? Img { get; set; }
}

/* ---------- prepositions ---------- */

public sealed class PrepositionsData
{
    public Dictionary<string, Scene> Scenes { get; set; } = new();
    public List<PrepositionFrame> Frames { get; set; } = new();
    public List<Level> Levels { get; set; } = new();
}

public sealed class Scene
{
    public string File { get; set; } = "";
    public string Alt { get; set; } = "";
}

public sealed class PrepositionFrame
{
    public string Id { get; set; } = "";
    public string Frame { get; set; } = "";
    public string En { get; set; } = "";
    public string Scene { get; set; } = "";
    public string? Contrast { get; set; }
    public bool Separable { get; set; }
    public bool DiscoverOnly { get; set; }
    public string? Prefix { get; set; }
    public List<string> Focus { get; set; } = new();
    public Example Example { get; set; } = new();
    public List<List<string>> Build { get; set; } = new();
    public List<Concept> Concept { get; set; } = new();
    public Pronominal? Pronominal { get; set; }
    public string? PronominalScene { get; set; }
}

public sealed class Example
{
    public string Nl { get; set; } = "";
    public string En { get; set; } = "";
}

public sealed class Pronominal
{
    public string Nl { get; set; } = "";
    public string En { get; set; } = "";
}

public sealed class Concept
{
    public string Question { get; set; } = "";
    public bool Answer { get; set; }
}

public sealed class Level
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";

    /// <summary>The CEFR band the level comes from, e.g. <c>a0</c>.</summary>
    public string? Band { get; set; }

    public List<string> Frames { get; set; } = new();
    public List<string>? Extra { get; set; }
}

/* ---------- story machine ---------- */

public sealed class Reel
{
    public string Id { get; set; } = "";
    public Dictionary<string, string> Label { get; set; } = new();
    public List<Tile> Tiles { get; set; } = new();
    public Join? Join { get; set; }
    public bool Wildcard { get; set; }
}

public sealed class Tile
{
    public string Id { get; set; } = "";
    public string Art { get; set; } = "";
    public string En { get; set; } = "";
    public string Nl { get; set; } = "";
}

public sealed class Join
{
    public string En { get; set; } = "";
    public string Nl { get; set; } = "";
    public bool Comma { get; set; }
}

/* ---------- provenance ---------- */

public sealed class MetaData
{
    public string GeneratedFrom { get; set; } = "";
    public int Categories { get; set; }
    public int Words { get; set; }
    public int WordImages { get; set; }
    public int Scenes { get; set; }
    public int Frames { get; set; }
    public int Levels { get; set; }
    public int Reels { get; set; }
}

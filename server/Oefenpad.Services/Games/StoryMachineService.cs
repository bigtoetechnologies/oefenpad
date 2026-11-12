using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// The story machine. Reels are positional, so the reel order is load-bearing.
/// Only the tiles currently on the drums leave the server; the word bank stays
/// embedded, and a spin sends just the strip of pictures the animation shows.
/// </summary>
public sealed class StoryMachineService : GameService
{
    private const int MinimumReels = 2;
    private const int MaximumReels = 6;
    private const int StripLength = 14;

    public StoryMachineService(GameContent content, RoundStore rounds) : base(content, rounds) { }

    public override string Game => "storymachine";

    public override GameOptions Options() => new(
        System.Array.Empty<GameCategory>(),
        Enumerable.Range(MinimumReels, MaximumReels - MinimumReels + 1)
            .Select(n => new GameLevel(n.ToString(), n.ToString(), n))
            .ToList());

    public override RoundStart Start(JsonElement input)
    {
        var count = Math.Clamp(Int(input, "count") ?? 3, MinimumReels, MaximumReels);
        var language = NormaliseLanguage(String(input, "language"));

        var state = new RoundState { Count = count, Language = language };
        for (var i = 0; i < count; i++)
            state.Tiles.Add(Draw(i, state));

        return Store(state, View(state));
    }

    public override RoundMove Move(string roundId, JsonElement move)
    {
        var state = State<RoundState>(roundId);

        switch (String(move, "action"))
        {
            case "hold":
            {
                var index = Int(move, "index") ?? throw new InvalidMoveException("Geen rol.");
                if (index < 0 || index >= state.Count)
                    throw new InvalidMoveException("Onbekende rol.");

                var held = Bool(move, "held") ?? false;
                if (held) state.Held.Add(index);
                else state.Held.Remove(index);

                return new RoundMove(View(state));
            }

            case "language":
            {
                state.Language = NormaliseLanguage(String(move, "language"));
                return new RoundMove(View(state));
            }

            case "spin":
            {
                var strips = new List<object>();

                for (var i = 0; i < state.Count; i++)
                {
                    if (state.Held.Contains(i)) continue;

                    state.Tiles[i] = Draw(i, state);

                    var art = new List<string>();
                    for (var n = 0; n < StripLength - 1; n++)
                        art.Add(Pick(Content.Reels[i].Tiles).Art);
                    art.Add(state.Tiles[i].Art);

                    strips.Add(new { index = i, art });
                }

                var view = View(state);
                return new RoundMove(new { view, strips });
            }

            default:
                throw new InvalidMoveException("Onbekende actie.");
        }
    }

    public override string? Export(string roundId) => ToJson(State<RoundState>(roundId));

    public override RoundStart Resume(string stateJson)
    {
        var state = JsonSerializer.Deserialize<RoundState>(stateJson, StorageJson)
            ?? throw new RoundExpiredException();

        return Store(state, View(state));
    }

    /* ---------- drawing ---------- */

    private Tile Draw(int reelIndex, RoundState state)
    {
        var reel = Content.Reels[reelIndex];
        var avoid = state.Tiles
            .Select((tile, i) => (tile, i))
            .Where(x => x.i != reelIndex && x.tile is not null)
            .Select(x => x.tile!.Id)
            .ToHashSet(StringComparer.Ordinal);

        Tile? tile = null;
        for (var attempt = 0; attempt < 12; attempt++)
        {
            tile = reel.Wildcard && Random.Shared.NextDouble() > 0.6
                ? Pick(Pick(Content.Reels).Tiles)
                : Pick(reel.Tiles);

            if (!avoid.Contains(tile.Id)) return tile;
        }

        return tile!;
    }

    private object View(RoundState state) => new
    {
        count = state.Count,
        language = state.Language,
        reels = state.Tiles.Select((tile, i) => new
        {
            index = i,
            label = new
            {
                nl = Content.Reels[i].Label.GetValueOrDefault("nl", ""),
                en = Content.Reels[i].Label.GetValueOrDefault("en", "")
            },
            held = state.Held.Contains(i),
            tile = new
            {
                id = tile.Id,
                art = tile.Art,
                nl = tile.Nl,
                en = tile.En
            }
        }).ToList()
    };

    private static string NormaliseLanguage(string? language) => language == "en" ? "en" : "nl";

    private sealed class RoundState
    {
        public int Count { get; set; } = 3;
        public string Language { get; set; } = "nl";
        public List<Tile> Tiles { get; set; } = new();
        public HashSet<int> Held { get; set; } = new();
    }
}

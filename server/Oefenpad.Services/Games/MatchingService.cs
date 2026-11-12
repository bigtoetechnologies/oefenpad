using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// Matching: one card from each panel, word against picture. The pairing table
/// and the deck order live on the server; a card face is revealed only when
/// the player asks for it.
/// </summary>
public sealed class MatchingService : GameService
{
    private const int MinimumPairs = 4;
    private const int MaximumWordLength = 12;

    private static readonly int[] PairOptions = { 4, 6, 8, 10, 12 };

    public MatchingService(GameContent content, RoundStore rounds) : base(content, rounds) { }

    public override string Game => "matching";

    public override GameOptions Options()
    {
        var categories = PairPoolAll()
            .Where(x => x.Value.Count >= MinimumPairs)
            .Select(x => Category(x.Key, x.Value.Count))
            .ToList();

        var levels = PairOptions
            .Select(n => new GameLevel(n.ToString(), Text($"pairs-{n}"), n))
            .ToList();

        return new GameOptions(categories, levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var category = String(input, "category") ?? "animals";
        var requested = Int(input, "pairs") ?? 6;

        var pool = PairPool(category);
        if (pool.Count < MinimumPairs)
            throw new InvalidMoveException("Deze categorie heeft te weinig paren.");

        var count = Math.Min(requested, pool.Count);
        if (count < MinimumPairs) count = MinimumPairs;

        var chosen = Shuffle(pool).Take(count).ToList();
        var cards = Shuffle(
            chosen.Select(p => new Card(p.Id, "word", p.Word, p.Image))
                .Concat(chosen.Select(p => new Card(p.Id, "image", p.Word, p.Image))));

        var state = new RoundState
        {
            Category = category,
            TotalPairs = count,
            Cards = cards
        };

        return Store(state, View(state));
    }

    public override RoundMove Move(string roundId, JsonElement move)
    {
        var state = State<RoundState>(roundId);
        if (String(move, "action") != "flip")
            throw new InvalidMoveException("Onbekende actie.");

        var index = Int(move, "index") ?? throw new InvalidMoveException("Geen kaart.");
        if (index < 0 || index >= state.Cards.Count)
            throw new InvalidMoveException("Onbekende kaart.");

        // A resolved miss is still face up; the next tap closes it. That has to
        // happen before the already-open check, or tapping one of the two missed
        // cards — the obvious next move — is refused and the turn cannot start.
        if (state.FaceUp.Count == 2) state.FaceUp.Clear();

        var card = state.Cards[index];
        if (card.Matched || state.FaceUp.Contains(index))
            return new RoundMove(View(state), Rejection: "alreadyOpen");

        // The two picks must come from opposite panels; a same-panel second
        // pick is refused and does not count as a move.
        if (state.FaceUp.Count == 1 && state.Cards[state.FaceUp[0]].Side == card.Side)
            return new RoundMove(View(state), Rejection: "sameSide");

        state.FaceUp.Add(index);

        bool? correct = null;
        var done = false;

        if (state.FaceUp.Count == 2)
        {
            var first = state.Cards[state.FaceUp[0]];
            var second = state.Cards[state.FaceUp[1]];
            state.Moves++;

            var matched = first.PairId == second.PairId && first.Side != second.Side;
            correct = matched;

            if (matched)
            {
                first.Matched = true;
                second.Matched = true;
                state.FaceUp.Clear();
                state.PairsFound++;
                done = state.PairsFound >= state.TotalPairs;
            }
        }

        return new RoundMove(View(state), Done: done, Correct: correct);
    }

    public override string? Export(string roundId) => ToJson(State<RoundState>(roundId));

    public override RoundStart Resume(string stateJson)
    {
        var state = JsonSerializer.Deserialize<RoundState>(stateJson, StorageJson)
            ?? throw new RoundExpiredException();

        return Store(state, View(state));
    }

    /* ---------- pair pools ---------- */

    private Dictionary<string, List<Pair>> PairPoolAll()
    {
        var result = new Dictionary<string, List<Pair>>(StringComparer.Ordinal);
        foreach (var (key, _) in Content.Categories)
            result[key] = PairPool(key);
        return result;
    }

    private List<Pair> PairPool(string category)
    {
        if (!Content.Categories.TryGetValue(category, out var cat)) return new List<Pair>();

        var seenImages = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var seenWords = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var pairs = new List<Pair>();

        foreach (var entry in cat.Words)
        {
            if (string.IsNullOrWhiteSpace(entry.En) || string.IsNullOrWhiteSpace(entry.Nl)) continue;
            if (entry.Nl.Length > MaximumWordLength) continue;
            if (!Content.WordImages.TryGetValue(entry.En!, out var image)) continue;
            if (!seenImages.Add(image)) continue;
            if (!seenWords.Add(entry.Nl!)) continue;

            pairs.Add(new Pair(pairs.Count, entry.Nl!, image));
        }

        return pairs;
    }

    private object View(RoundState state) => new
    {
        category = new
        {
            id = state.Category,
            name = Content.CategoryName(state.Category),
            icon = Content.CategoryIcon(state.Category)
        },
        pairs = state.TotalPairs,
        moves = state.Moves,
        pairsLeft = state.TotalPairs - state.PairsFound,
        cards = state.Cards.Select((card, i) => new
        {
            index = i,
            side = card.Side,
            matched = card.Matched,
            faceUp = state.FaceUp.Contains(i),
            face = card.Matched || state.FaceUp.Contains(i)
                ? new
                {
                    kind = card.Side == "image" ? "image" : "word",
                    word = card.Word,
                    imageUrl = card.Side == "image" ? "/assets/wordimages/" + card.Image : null
                }
                : null
        }).ToList()
    };

    private sealed record Pair(int Id, string Word, string Image);

    private sealed class RoundState
    {
        public string Category { get; set; } = "animals";
        public int TotalPairs { get; set; }
        public int PairsFound { get; set; }
        public int Moves { get; set; }
        public List<Card> Cards { get; set; } = new();
        public List<int> FaceUp { get; set; } = new();
    }

    private sealed record Card(int PairId, string Side, string Word, string Image)
    {
        public bool Matched { get; set; }
    }
}

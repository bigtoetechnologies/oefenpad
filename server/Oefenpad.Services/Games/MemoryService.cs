using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// Memory: pair a Dutch word with its picture, or, in a text-only category,
/// with its English meaning. The deck, including which item
/// sits behind each card, stays on this side; a card's face is only revealed
/// when the player turns it.
/// </summary>
public sealed class MemoryService : GameService
{
    private static readonly (string Id, int Size, int Pairs)[] Levels =
    {
        ("4", 4, 8),
        ("6", 6, 18),
        ("8", 8, 32),
        ("10", 10, 50)
    };

    public MemoryService(GameContent content, RoundStore rounds) : base(content, rounds) { }

    public override string Game => "memory";

    public override GameOptions Options()
    {
        var categories = new List<GameCategory>
        {
            new("all", Text("cat-all"), "🖼️", Content.ImageItems.Count)
        };

        foreach (var group in Content.ImageItems.GroupBy(x => x.Category).OrderBy(x => x.Key))
            categories.Add(Category(group.Key, group.Count()));

        // Text-only categories count pairs, not pictures. One too small for the
        // smallest board is left out, so no listed category is unplayable; the
        // client already greys out the boards a category has too few pairs for.
        var smallest = Levels.Min(l => l.Pairs);
        foreach (var (key, category) in Content.Categories.Where(x => x.Value.TextOnly))
        {
            var pairs = Content.TextPairs(key).Count;
            if (pairs >= smallest) categories.Add(Category(key, pairs));
        }

        var levels = Levels
            .Select(l => new GameLevel(l.Id, Text($"diff-{l.Id}x{l.Id}"), l.Pairs))
            .ToList();

        return new GameOptions(categories, levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var category = String(input, "category") ?? "all";
        var levelId = String(input, "level") ?? "6";

        var level = Levels.FirstOrDefault(l => l.Id == levelId);
        if (level.Id is null) throw new InvalidMoveException("Onbekend niveau.");

        if (category != "all" && !Content.Categories.ContainsKey(category))
            throw new InvalidMoveException("Onbekende categorie.");

        var text = Content.IsTextOnly(category);
        List<Card> deck;

        if (text)
        {
            var pairs = Content.TextPairs(category);
            if (pairs.Count < level.Pairs)
                throw new InvalidMoveException("Deze categorie heeft te weinig paren voor dit niveau.");

            // The pair id is the Dutch word, which TextPairs keeps unique.
            var chosen = Shuffle(pairs).Take(level.Pairs).ToList();
            deck = Shuffle(
                chosen.Select(p => new Card(p.Dutch, "word", p.Dutch, null))
                    .Concat(chosen.Select(p => new Card(p.Dutch, "meaning", p.English, null))));
        }
        else
        {
            var pool = Content.ImagesFor(category).ToList();
            if (pool.Count < level.Pairs)
                throw new InvalidMoveException("Deze categorie heeft te weinig plaatjes voor dit niveau.");

            var items = Shuffle(pool).Take(level.Pairs).ToList();
            deck = Shuffle(
                items.Select(item => new Card(item.File, "image", item.Dutch, item.File))
                    .Concat(items.Select(item => new Card(item.File, "word", item.Dutch, item.File))));
        }

        var state = new RoundState
        {
            Category = category,
            LevelId = level.Id,
            GridSize = level.Size,
            TotalPairs = level.Pairs,
            Text = text,
            Cards = deck
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

        // Two wrong cards stay face up until the player turns the next one. Close
        // them before the already-open check: in a memory game the next card is
        // very often one of those two, and refusing it strands the player.
        if (state.FaceUp.Count == 2) state.FaceUp.Clear();

        var card = state.Cards[index];
        if (card.Matched || state.FaceUp.Contains(index))
            return new RoundMove(View(state), Rejection: "alreadyOpen");

        state.FaceUp.Add(index);

        bool? correct = null;
        var done = false;

        if (state.FaceUp.Count == 2)
        {
            var first = state.Cards[state.FaceUp[0]];
            var second = state.Cards[state.FaceUp[1]];
            state.Moves++;

            var matched = first.ItemId == second.ItemId && first.Kind != second.Kind;
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

    private object View(RoundState state) => new
    {
        category = new
        {
            id = state.Category,
            name = state.Category == "all" ? Text("cat-all") : Content.CategoryName(state.Category),
            icon = state.Category == "all" ? "🖼️" : Content.CategoryIcon(state.Category)
        },
        level = state.LevelId,
        text = state.Text,
        gridSize = state.GridSize,
        pairs = state.TotalPairs,
        moves = state.Moves,
        pairsFound = state.PairsFound,
        cards = state.Cards.Select((card, i) => new
        {
            index = i,
            matched = card.Matched,
            faceUp = state.FaceUp.Contains(i),
            face = card.Matched || state.FaceUp.Contains(i)
                ? new
                {
                    kind = card.Kind,
                    word = card.Word,
                    imageUrl = card.Kind == "image" ? "/assets/wordimages/" + card.Image : null
                }
                : null
        }).ToList()
    };

    private sealed class RoundState
    {
        public string Category { get; set; } = "all";
        public string LevelId { get; set; } = "6";
        public int GridSize { get; set; }
        public int TotalPairs { get; set; }
        /// <summary>A text-only round: Dutch word against English meaning.</summary>
        public bool Text { get; set; }
        public int PairsFound { get; set; }
        public int Moves { get; set; }
        public List<Card> Cards { get; set; } = new();
        public List<int> FaceUp { get; set; } = new();
    }

    private sealed record Card(string ItemId, string Kind, string Word, string? Image)
    {
        public bool Matched { get; set; }
    }
}

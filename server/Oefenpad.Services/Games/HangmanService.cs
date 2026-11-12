using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// Hangman. The hidden word, the picture clue and the answer stay on the
/// server; the view carries only the pattern of known and unknown letters.
/// </summary>
public sealed class HangmanService : GameService
{
    private const int MaximumWrong = 10;
    private const int StartingHints = 2;
    private const string Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    private static readonly (string Id, int MaxLength)[] Difficulties =
    {
        ("easy", 5),
        ("medium", 8),
        ("hard", 99)
    };

    public HangmanService(GameContent content, RoundStore rounds) : base(content, rounds) { }

    public override string Game => "hangman";

    public override GameOptions Options()
    {
        var categories = Content.Categories
            .Where(x => x.Value.Words.Any(w => !string.IsNullOrWhiteSpace(w.Nl)))
            .Select(x => Category(x.Key,
                x.Value.Words.Count(w => !string.IsNullOrWhiteSpace(w.Nl))))
            .ToList();

        var levels = Difficulties
            .Select(d => new GameLevel(d.Id, Text($"diff-{d.Id}")))
            .ToList();

        return new GameOptions(categories, levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var category = String(input, "category") ?? "animals";
        var difficultyId = String(input, "difficulty") ?? "medium";
        var translateTo = String(input, "translateTo") ?? "";

        if (!Content.Categories.ContainsKey(category))
            throw new InvalidMoveException("Onbekende categorie.");

        var difficulty = Difficulties.FirstOrDefault(d => d.Id == difficultyId);
        if (difficulty.Id is null) throw new InvalidMoveException("Onbekend niveau.");

        var word = PickWord(category, difficulty.MaxLength, translateTo);
        if (word is null) throw new InvalidMoveException("Geen woord gevonden voor deze keuze.");

        var state = new RoundState
        {
            Category = category,
            Difficulty = difficulty.Id,
            Word = word,
            TranslateTo = translateTo
        };

        return Store(state, View(state));
    }

    public override RoundMove Move(string roundId, JsonElement move)
    {
        var state = State<RoundState>(roundId);
        var action = String(move, "action");

        return action switch
        {
            "guess" => Guess(state, move),
            "hint" => Hint(state),
            _ => throw new InvalidMoveException("Onbekende actie.")
        };
    }

    public override string? Export(string roundId) => ToJson(State<RoundState>(roundId));

    public override RoundStart Resume(string stateJson)
    {
        var state = JsonSerializer.Deserialize<RoundState>(stateJson, StorageJson)
            ?? throw new RoundExpiredException();

        return Store(state, View(state));
    }

    private RoundMove Guess(RoundState state, JsonElement move)
    {
        if (state.Status != "playing")
            throw new InvalidMoveException("Het spel is al klaar.");

        var raw = String(move, "letter");
        if (string.IsNullOrWhiteSpace(raw) || raw.Trim().Length != 1)
            throw new InvalidMoveException("Geen letter.");

        var letter = char.ToUpperInvariant(raw.Trim()[0]);
        if (!Alphabet.Contains(letter))
            throw new InvalidMoveException("Onbekende letter.");
        if (!state.Guessed.Add(letter))
            throw new InvalidMoveException("Deze letter is al geraden.");

        var hit = state.Word.Contains(letter);
        if (!hit) state.Wrong++;

        FinishIfOver(state);
        return new RoundMove(View(state), Done: state.Status != "playing", Correct: hit);
    }

    private RoundMove Hint(RoundState state)
    {
        if (state.Status != "playing")
            throw new InvalidMoveException("Het spel is al klaar.");
        if (state.HintsLeft <= 0)
            throw new InvalidMoveException("Geen hints meer.");

        var remaining = state.Word
            .Where(char.IsLetter)
            .Where(ch => !state.Guessed.Contains(ch))
            .Distinct()
            .ToList();

        if (remaining.Count == 0)
            throw new InvalidMoveException("Alle letters zijn al bekend.");

        state.Guessed.Add(Pick(remaining));
        state.HintsLeft--;
        FinishIfOver(state);

        return new RoundMove(View(state), Done: state.Status != "playing", Correct: true);
    }

    private static void FinishIfOver(RoundState state)
    {
        var allFound = state.Word
            .Where(char.IsLetter)
            .All(state.Guessed.Contains);

        if (allFound) state.Status = "won";
        else if (state.Wrong >= MaximumWrong) state.Status = "lost";
    }

    /* ---------- content ---------- */

    private WordEntry? EntryFor(RoundState state) =>
        Content.Categories.TryGetValue(state.Category, out var cat)
            ? cat.Words.FirstOrDefault(w =>
                string.Equals(w.Nl, state.Word, StringComparison.OrdinalIgnoreCase))
            : null;

    private (string? Clue, string? Translation) HelpersFor(RoundState state)
    {
        var entry = EntryFor(state);
        if (entry is null) return (null, null);

        var clue = Content.ImageFor(entry);
        var translation = state.TranslateTo == "en" ? entry.En : null;
        return (clue, translation);
    }

    private string? PickWord(string category, int maxLength, string translateTo)
    {
        if (!Content.Categories.TryGetValue(category, out var cat)) return null;

        var eligible = cat.Words
            .Where(w => !string.IsNullOrWhiteSpace(w.Nl))
            .Where(w => translateTo != "en" || !string.IsNullOrWhiteSpace(w.En))
            .Where(w =>
            {
                var letters = w.Nl!.Count(char.IsLetter);
                return letters >= 3 && letters <= maxLength;
            })
            .ToList();

        // Prefer words with a picture clue; the point of the clue is that the
        // meaning is visible while the spelling is not.
        var withImage = eligible.Where(w => Content.ImageFor(w) is not null).ToList();
        if (withImage.Count > 0) eligible = withImage;

        return eligible.Count == 0
            ? cat.Words.FirstOrDefault(w => !string.IsNullOrWhiteSpace(w.Nl))?.Nl
            : Pick(eligible).Nl;
    }

    private object View(RoundState state)
    {
        var (clue, translation) = HelpersFor(state);
        var over = state.Status != "playing";

        return new
        {
            category = new
            {
                id = state.Category,
                name = Content.CategoryName(state.Category),
                icon = Content.CategoryIcon(state.Category)
            },
            difficulty = state.Difficulty,
            maxWrong = MaximumWrong,
            wrong = state.Wrong,
            guessed = state.Guessed.OrderBy(x => x).ToList(),
            pattern = state.Word.Select(ch => new
            {
                gap = ch == ' ',
                text = !char.IsLetter(ch) || state.Guessed.Contains(ch) ? ch.ToString() : null,
                revealed = !char.IsLetter(ch) || state.Guessed.Contains(ch)
            }).ToList(),
            wordLength = state.Word.Length,
            hintsLeft = state.HintsLeft,
            status = state.Status,
            clueImageUrl = clue is null ? null : "/assets/wordimages/" + clue,
            translation = state.TranslateTo == "en" ? translation : null,
            answer = over ? state.Word : null,
            imageUrl = over && clue is not null ? "/assets/wordimages/" + clue : null
        };
    }

    private sealed class RoundState
    {
        public string Category { get; set; } = "animals";
        public string Difficulty { get; set; } = "medium";
        public string Word { get; set; } = "";
        public string TranslateTo { get; set; } = "";
        public HashSet<char> Guessed { get; set; } = new();
        public int Wrong { get; set; }
        public int HintsLeft { get; set; } = StartingHints;
        public string Status { get; set; } = "playing";
    }
}

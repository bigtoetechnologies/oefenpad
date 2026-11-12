using System.Text.Json;

namespace Oefenpad.Services.Games;

/// <summary>
/// Word search. The grid, the placement of every word and the profanity filter
/// are generated here; the browser receives the letters and the word list, but
/// never where a word sits. A selection is judged against the hidden placement
/// table, so the answer can not be read out of the page.
/// </summary>
public sealed class WordSearchService : GameService
{
    private const string DefaultCategory = "animals";

    private static readonly (int Dr, int Dc)[] AllDirections =
    {
        (0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (1, -1), (-1, -1)
    };

    private static readonly DifficultySpec[] Difficulties =
    {
        // Beginner places words in one direction only, and AvoidAdjacent rejects
        // any placement whose cells touch another word, so two words can never
        // share a cell: the overlap is structurally always 0. A target above it
        // was unreachable and simply spent 25 futile regenerations per round.
        //
        // Easy keeps AvoidAdjacent and only adds the perpendicular direction. A
        // crossing still fails the adjacency check: the shared cell's neighbours
        // along the other word are not part of this word, so they read as touches.
        // Twenty generated boards overlapped by exactly 0 percent, so a 25 percent
        // target burned the whole budget every round (152 ms measured against
        // beginner's 5.8 ms).
        new("beginner", 10, 6, new[] { (0, 1) }, 3, 5, 0, true),
        new("easy", 12, 8, new[] { (0, 1), (1, 0) }, 3, 6, 0, true),
        new("medium", 16, 10, new[] { (0, 1), (0, -1), (1, 0), (-1, 0) }, 4, 7, 25, false),
        new("hard", 20, 16, AllDirections, 4, 10, 25, false),
        new("master", 20, 20, AllDirections, 4, 13, 25, false),
        new("insane", 20, 65, AllDirections, 4, 13, 0, false)
        {
            MinDensity = 0.75,
            StrictOverlap = true,
            MaxRegenerations = 5
        }
    };

    private static readonly HashSet<string> BlockedWords = new(StringComparer.Ordinal)
    {
        "ANAL", "ANUS", "ARSE", "ASS", "BASTARD", "BITCH", "BLOODY", "BOLLOCKS", "BONER", "BUM",
        "BUTT", "CLIT", "COCK", "COON", "CRAP", "CUM", "CUNT", "DAMN", "DICK", "DIKE",
        "DYKE", "FAG", "FART", "FELCH", "FUCK", "GAY", "GOOK", "HELL", "HOE", "HOMO",
        "HORE", "JAP", "JERK", "JIZZ", "KNOB", "KUNT", "LICK", "MUFF", "NIG", "NOB",
        "PEDO", "PENIS", "PISS", "POOP", "PORN", "PRICK", "PUBE", "PUSSY", "QUEER", "RAPE",
        "RIM", "SCHLONG", "SCREW", "SCUM", "SEMEN", "SEX", "SHAG", "SHIT", "SKANK", "SLUT",
        "SMEG", "SPAZ", "SPERM", "SPIC", "TIT", "TURD", "TWAT", "VAG", "VULVA", "WANG",
        "WANK", "WHORE", "WOG", "WOP", "KUT", "LUL", "PIK", "NEUK", "NEUKEN", "HOER",
        "SLOERIE", "TYFUS", "TERING", "KOLERE", "KLOTE", "KLOTEN", "GODVER", "VERDOMME", "STRONT", "SCHIJT",
        "PIS", "ZEIK", "KONT", "REET", "SUKKEL", "EIKEL", "NEGER", "MOF", "PLEE", "KAK",
        "FLIKKER", "KLOOTZAK", "HUFFER", "SMEERLAP", "MIETJE", "PLEURIS", "TIEFUS", "POKKEN", "KANKER", "TRUT"
    };

    private const string FillerAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private const int MaxPlacementAttempts = 500;

    public WordSearchService(GameContent content, RoundStore rounds) : base(content, rounds) { }

    public override string Game => "wordsearch";

    public override GameOptions Options()
    {
        var categories = Content.PlayableCategories(requireImage: false)
            .Where(x => x.Category.Words.Any(IsSingleWord))
            .Select(x => Category(x.Key,
                x.Category.Words.Count(w => IsSingleWord(w) && !string.IsNullOrWhiteSpace(w.Nl))))
            .ToList();

        var levels = Difficulties
            .Select(d => new GameLevel(d.Id, Text($"diff-{d.Id}"), d.GridSize))
            .ToList();

        return new GameOptions(categories, levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var category = String(input, "category") ?? DefaultCategory;
        var difficultyId = String(input, "difficulty") ?? "beginner";
        var translateTo = String(input, "translateTo") ?? "";

        var spec = Difficulties.FirstOrDefault(d => d.Id == difficultyId);
        if (spec is null) throw new InvalidMoveException("Onbekend niveau.");

        var puzzle = Generate(spec, category, translateTo);
        return Store(puzzle, View(puzzle));
    }

    public override RoundMove Move(string roundId, JsonElement move)
    {
        var puzzle = State<Puzzle>(roundId);

        return String(move, "action") switch
        {
            "select" => Select(puzzle, move),
            "hint" => Hint(puzzle),
            _ => throw new InvalidMoveException("Onbekende actie.")
        };
    }

    public override string? Export(string roundId) => ToJson(Snapshot(State<Puzzle>(roundId)));

    public override RoundStart Resume(string stateJson)
    {
        var saved = JsonSerializer.Deserialize<PuzzleState>(stateJson, StorageJson)
            ?? throw new RoundExpiredException();
        var puzzle = Restore(saved);

        // Only the cells of words already found travel: the outlines the
        // player has earned, never the placements still hidden.
        return Store(puzzle, View(puzzle), new { placements = Placements(puzzle) });
    }

    /* =============================================================
       Player actions
       ============================================================= */

    private RoundMove Select(Puzzle puzzle, JsonElement move)
    {
        var r1 = Int(move, "r1") ?? throw new InvalidMoveException("Geen selectie.");
        var c1 = Int(move, "c1") ?? throw new InvalidMoveException("Geen selectie.");
        var r2 = Int(move, "r2") ?? throw new InvalidMoveException("Geen selectie.");
        var c2 = Int(move, "c2") ?? throw new InvalidMoveException("Geen selectie.");

        if (!Inside(puzzle, r1, c1) || !Inside(puzzle, r2, c2))
            throw new InvalidMoveException("Selectie valt buiten het rooster.");

        var (stepR, stepC) = Step(r1, c1, r2, c2);
        if (stepR == 0 && stepC == 0)
            throw new InvalidMoveException("Selecteer een lijn.");

        var selected = new System.Text.StringBuilder();
        var r = r1;
        var c = c1;
        while (true)
        {
            selected.Append(puzzle.Grid[r, c]);
            if (r == r2 && c == c2) break;
            r += stepR;
            c += stepC;
            if (!Inside(puzzle, r, c)) break;
        }

        var text = selected.ToString();
        var reversed = new string(text.Reverse().ToArray());

        for (var i = 0; i < puzzle.Words.Count; i++)
        {
            if (puzzle.Found[i]) continue;
            var word = puzzle.Words[i].Text;
            if (text != word && reversed != word) continue;

            puzzle.Found[i] = true;
            var done = puzzle.Found.All(x => x);
            return new RoundMove(new { view = View(puzzle), foundIndex = i },
                Done: done, Correct: true);
        }

        return new RoundMove(View(puzzle), Correct: false);
    }

    private RoundMove Hint(Puzzle puzzle)
    {
        if (puzzle.HintsLeft <= 0)
            throw new InvalidMoveException("Geen hints meer.");

        var unfound = Enumerable.Range(0, puzzle.Words.Count)
            .Where(i => !puzzle.Found[i])
            .ToList();
        if (unfound.Count == 0)
            throw new InvalidMoveException("Alle woorden zijn al gevonden.");

        var index = Pick(unfound);
        puzzle.HintsLeft--;

        var word = puzzle.Words[index];
        var cells = Enumerable.Range(0, word.Text.Length)
            .Select(i => new { r = word.Row + word.Dr * i, c = word.Col + word.Dc * i })
            .ToList();

        return new RoundMove(new { view = View(puzzle), hint = new { index, cells } });
    }

    /* =============================================================
       Views
       ============================================================= */

    private object View(Puzzle puzzle) => new
    {
        difficulty = puzzle.DifficultyId,
        category = new
        {
            id = puzzle.CategoryId,
            name = Content.CategoryName(puzzle.CategoryId),
            icon = Content.CategoryIcon(puzzle.CategoryId)
        },
        size = puzzle.Size,
        grid = Enumerable.Range(0, puzzle.Size)
            .Select(r => Enumerable.Range(0, puzzle.Size)
                .Select(c => puzzle.Grid[r, c].ToString())
                .ToList())
            .ToList(),
        words = puzzle.Words.Select((w, i) => new
        {
            index = i,
            text = w.Text,
            translation = w.Translation,
            imageUrl = w.Image is null ? null : "/assets/wordimages/" + w.Image
        }).ToList(),
        found = puzzle.Found,
        hintsLeft = puzzle.HintsLeft,
        done = puzzle.Found.All(x => x)
    };

    /* =============================================================
       Generation
       ============================================================= */

    private Puzzle Generate(DifficultySpec spec, string category, string translateTo)
    {
        var puzzle = TryGenerate(spec, category, translateTo)
            ?? (category != DefaultCategory
                ? TryGenerate(spec, DefaultCategory, translateTo)
                : null);

        return puzzle ?? throw new InvalidMoveException("Geen woorden gevonden voor deze keuze.");
    }

    private Puzzle? TryGenerate(DifficultySpec spec, string category, string translateTo)
    {
        if (!Content.Categories.TryGetValue(category, out var cat)) return null;

        var candidates = CandidateWords(cat, spec, translateTo);
        if (candidates.Count == 0) return null;

        var best = (Puzzle?)null;
        var bestDensity = -1.0;
        var maxRegenerations = spec.MaxRegenerations > 0 ? spec.MaxRegenerations : 25;

        for (var regeneration = 0; regeneration < maxRegenerations; regeneration++)
        {
            var attempt = Build(spec, category, candidates);
            var density = (double)attempt.UniqueCells / (spec.GridSize * spec.GridSize);

            if (spec.MinDensity > 0)
            {
                if (density > bestDensity)
                {
                    bestDensity = density;
                    best = attempt;
                }
                if (density >= spec.MinDensity) break;
                continue;
            }

            if (attempt.OverlapPercent >= spec.MinOverlapPercent) return attempt;
        }

        if (best is not null) return best;

        // No attempt cleared the overlap target; keep the last one rather than
        // throwing away a playable board.
        return Build(spec, category, candidates);
    }

    private Puzzle Build(
        DifficultySpec spec,
        string category,
        List<Candidate> candidates)
    {
        var grid = new char[spec.GridSize, spec.GridSize];
        var solution = new int[spec.GridSize, spec.GridSize];
        for (var r = 0; r < spec.GridSize; r++)
        for (var c = 0; c < spec.GridSize; c++)
            solution[r, c] = -1;

        var words = new List<PlacedWord>();

        var selected = SelectWords(candidates, spec.WordCount);
        var totalLetters = 0;

        foreach (var word in selected)
        {
            var choices = new List<(int Row, int Col, int Dr, int Dc, int Overlaps)>();

            for (var attempt = 0; attempt < MaxPlacementAttempts; attempt++)
            {
                var (dr, dc) = Pick(spec.Directions);
                var row = Random.Shared.Next(spec.GridSize);
                var col = Random.Shared.Next(spec.GridSize);

                if (!CanPlace(grid, solution, words, spec, word.Text, row, col, dr, dc)) continue;

                choices.Add((row, col, dr, dc,
                    CountOverlaps(grid, solution, word.Text, row, col, dr, dc)));
            }

            if (choices.Count == 0) continue;

            choices.Sort((a, b) => b.Overlaps.CompareTo(a.Overlaps));
            var maxOverlap = choices[0].Overlaps;

            (int Row, int Col, int Dr, int Dc, int Overlaps) choice;
            if (spec.StrictOverlap)
            {
                var top = choices.Where(x => x.Overlaps == maxOverlap).ToList();
                choice = Pick(top);
            }
            else
            {
                var poolSize = Math.Max(1, (int)Math.Ceiling(choices.Count * 0.3));
                while (poolSize < choices.Count && choices[poolSize].Overlaps == maxOverlap)
                    poolSize++;

                choice = choices[Random.Shared.Next(poolSize)];
            }

            PlaceWord(grid, solution, words, word, choice.Row, choice.Col, choice.Dr, choice.Dc);
            totalLetters += word.Text.Length;
        }

        var puzzle = new Puzzle
        {
            DifficultyId = spec.Id,
            CategoryId = category,
            Size = spec.GridSize,
            Grid = grid,
            Solution = solution,
            Words = words,
            Found = new bool[words.Count],
            HintsLeft = spec.Id == "insane" ? 0 : 3
        };

        ShuffleWordOrder(puzzle);

        var uniqueCells = 0;
        for (var r = 0; r < spec.GridSize; r++)
        for (var c = 0; c < spec.GridSize; c++)
            if (puzzle.Solution[r, c] >= 0) uniqueCells++;

        puzzle.UniqueCells = uniqueCells;
        puzzle.OverlapPercent = totalLetters > 0
            ? (totalLetters - uniqueCells) * 100.0 / totalLetters
            : 0;

        Fill(puzzle);
        Sanitize(puzzle);

        return puzzle;
    }

    private List<Candidate> CandidateWords(
        WordCategory cat,
        DifficultySpec spec,
        string translateTo)
    {
        var result = new List<Candidate>();
        var seen = new HashSet<string>(StringComparer.Ordinal);

        foreach (var entry in cat.Words)
        {
            if (string.IsNullOrWhiteSpace(entry.Nl) || !IsSingleWord(entry)) continue;
            if (entry.Nl.Length < spec.MinWordLen || entry.Nl.Length > spec.MaxWordLen) continue;
            if (translateTo == "en" && string.IsNullOrWhiteSpace(entry.En)) continue;
            if (!seen.Add(entry.Nl)) continue;

            result.Add(new Candidate(
                entry.Nl,
                translateTo == "en" ? entry.En : null,
                Content.ImageFor(entry)));
        }

        return result;
    }

    private static List<Candidate> SelectWords(List<Candidate> candidates, int wordCount)
    {
        var shuffled = Shuffle(candidates);
        var selected = new List<Candidate>();

        foreach (var candidate in shuffled)
        {
            if (selected.Count >= wordCount) break;
            if (selected.Any(x =>
                    x.Text.Contains(candidate.Text, StringComparison.Ordinal) ||
                    candidate.Text.Contains(x.Text, StringComparison.Ordinal)))
                continue;

            selected.Add(candidate);
        }

        if (selected.Count < 2)
        {
            selected.Clear();
            selected.AddRange(shuffled.Take(wordCount));
        }

        var unique = new List<Candidate>();
        var words = new HashSet<string>(StringComparer.Ordinal);
        foreach (var candidate in selected)
            if (words.Add(candidate.Text)) unique.Add(candidate);

        unique.Sort((a, b) => b.Text.Length.CompareTo(a.Text.Length));
        return unique;
    }

    /* ---------- placement ---------- */

    private static bool CanPlace(
        char[,] grid,
        int[,] solution,
        List<PlacedWord> words,
        DifficultySpec spec,
        string word,
        int row,
        int col,
        int dr,
        int dc)
    {
        for (var i = 0; i < word.Length; i++)
        {
            var r = row + dr * i;
            var c = col + dc * i;
            if (!Inside(spec.GridSize, r, c)) return false;

            var existing = solution[r, c];
            if (existing >= 0)
            {
                if (grid[r, c] != word[i]) return false;
                // A word in the same direction would merge, not intersect.
                var other = words[existing];
                if (other.Dr * dc == other.Dc * dr) return false;
            }
        }

        var beforeR = row - dr;
        var beforeC = col - dc;
        if (Inside(spec.GridSize, beforeR, beforeC))
        {
            var previous = solution[beforeR, beforeC];
            if (previous >= 0)
            {
                var other = words[previous];
                if (other.Dr * dc == other.Dc * dr) return false;
            }
        }

        var afterR = row + dr * word.Length;
        var afterC = col + dc * word.Length;
        if (Inside(spec.GridSize, afterR, afterC))
        {
            var next = solution[afterR, afterC];
            if (next >= 0)
            {
                var other = words[next];
                if (other.Dr * dc == other.Dc * dr) return false;
            }
        }

        return !spec.AvoidAdjacent || !HasTouchingWord(solution, spec.GridSize, word, row, col, dr, dc);
    }

    private static bool HasTouchingWord(
        int[,] solution,
        int size,
        string word,
        int row,
        int col,
        int dr,
        int dc)
    {
        var orthogonal = new[] { (-1, 0), (1, 0), (0, -1), (0, 1) };

        for (var i = 0; i < word.Length; i++)
        {
            var r = row + dr * i;
            var c = col + dc * i;

            foreach (var (odr, odc) in orthogonal)
            {
                var nr = r + odr;
                var nc = c + odc;
                if (!Inside(size, nr, nc)) continue;
                if (solution[nr, nc] < 0) continue;

                var isSelf = false;
                for (var j = 0; j < word.Length; j++)
                {
                    if (row + dr * j == nr && col + dc * j == nc)
                    {
                        isSelf = true;
                        break;
                    }
                }

                if (isSelf) continue;
                return true;
            }
        }

        return false;
    }

    private static int CountOverlaps(
        char[,] grid,
        int[,] solution,
        string word,
        int row,
        int col,
        int dr,
        int dc)
    {
        var overlaps = 0;
        for (var i = 0; i < word.Length; i++)
        {
            var r = row + dr * i;
            var c = col + dc * i;
            if (solution[r, c] >= 0 && grid[r, c] == word[i]) overlaps++;
        }

        return overlaps;
    }

    private static void PlaceWord(
        char[,] grid,
        int[,] solution,
        List<PlacedWord> words,
        Candidate candidate,
        int row,
        int col,
        int dr,
        int dc)
    {
        var index = words.Count;
        words.Add(new PlacedWord
        {
            Text = candidate.Text,
            Translation = candidate.Translation,
            Image = candidate.Image,
            Row = row,
            Col = col,
            Dr = dr,
            Dc = dc
        });

        for (var i = 0; i < candidate.Text.Length; i++)
        {
            var r = row + dr * i;
            var c = col + dc * i;
            grid[r, c] = candidate.Text[i];
            solution[r, c] = index;
        }
    }

    private static void ShuffleWordOrder(Puzzle puzzle)
    {
        var order = Shuffle(Enumerable.Range(0, puzzle.Words.Count));
        var remap = new int[puzzle.Words.Count];
        for (var newIndex = 0; newIndex < order.Count; newIndex++)
            remap[order[newIndex]] = newIndex;

        puzzle.Words = order.Select(i => puzzle.Words[i]).ToList();

        for (var r = 0; r < puzzle.Size; r++)
        for (var c = 0; c < puzzle.Size; c++)
        {
            var old = puzzle.Solution[r, c];
            if (old >= 0) puzzle.Solution[r, c] = remap[old];
        }

        puzzle.Found = new bool[puzzle.Words.Count];
    }

    private static void Fill(Puzzle puzzle)
    {
        for (var r = 0; r < puzzle.Size; r++)
        for (var c = 0; c < puzzle.Size; c++)
        {
            if (puzzle.Grid[r, c] == '\0')
                puzzle.Grid[r, c] = FillerAlphabet[Random.Shared.Next(FillerAlphabet.Length)];
        }
    }

    /* ---------- profanity filter ---------- */

    private static void Sanitize(Puzzle puzzle)
    {
        var size = puzzle.Size;
        var directions = new[] { (0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (1, -1), (-1, -1) };
        var changed = true;
        var passes = 0;

        while (changed && passes < 20)
        {
            changed = false;
            passes++;

            for (var r = 0; r < size; r++)
            for (var c = 0; c < size; c++)
            foreach (var (dr, dc) in directions)
            {
                var text = new System.Text.StringBuilder();
                var cells = new List<(int R, int C)>();
                var rr = r;
                var cc = c;

                while (Inside(size, rr, cc) && text.Length < 8)
                {
                    text.Append(puzzle.Grid[rr, cc]);
                    cells.Add((rr, cc));
                    rr += dr;
                    cc += dc;
                }

                var str = text.ToString();

                for (var length = 3; length <= str.Length; length++)
                {
                    for (var start = 0; start + length <= str.Length; start++)
                    {
                        var sub = str.Substring(start, length);
                        if (!BlockedWords.Contains(sub)) continue;

                        for (var k = start; k < start + length; k++)
                        {
                            var (cr, cc2) = cells[k];
                            if (puzzle.Solution[cr, cc2] >= 0) continue;

                            puzzle.Grid[cr, cc2] =
                                FillerAlphabet[Random.Shared.Next(FillerAlphabet.Length)];
                            changed = true;
                            break;
                        }

                        if (changed) break;
                    }

                    if (changed) break;
                }

                if (changed) break;
            }
        }
    }

    /* ---------- geometry ---------- */

    private static bool Inside(int size, int r, int c) =>
        r >= 0 && r < size && c >= 0 && c < size;

    private static bool Inside(Puzzle puzzle, int r, int c) =>
        r >= 0 && r < puzzle.Size && c >= 0 && c < puzzle.Size;

    private static (int Dr, int Dc) Step(int r1, int c1, int r2, int c2)
    {
        var dr = r2 - r1;
        var dc = c2 - c1;

        if (dr == 0 && dc != 0) return (0, Math.Sign(dc));
        if (dc == 0 && dr != 0) return (Math.Sign(dr), 0);
        if (Math.Abs(dr) == Math.Abs(dc) && dr != 0) return (Math.Sign(dr), Math.Sign(dc));
        return (0, 0);
    }

    private static bool IsSingleWord(WordEntry entry) =>
        !string.IsNullOrWhiteSpace(entry.Nl) && entry.Nl.All(char.IsLetter);

    /* ---------- state ---------- */

    /// <summary>
    /// The stored shape. A <c>char[,]</c> and an <c>int[,]</c> do not serialize,
    /// so the grid travels as rows and the solution is rebuilt from the words
    /// (which is also the only copy worth trusting after a restart).
    /// </summary>
    private static PuzzleState Snapshot(Puzzle puzzle) => new()
    {
        DifficultyId = puzzle.DifficultyId,
        CategoryId = puzzle.CategoryId,
        Size = puzzle.Size,
        Rows = Enumerable.Range(0, puzzle.Size)
            .Select(r => new string(Enumerable.Range(0, puzzle.Size)
                .Select(c => puzzle.Grid[r, c])
                .ToArray()))
            .ToList(),
        Words = puzzle.Words,
        Found = puzzle.Found,
        HintsLeft = puzzle.HintsLeft,
        UniqueCells = puzzle.UniqueCells,
        OverlapPercent = puzzle.OverlapPercent
    };

    private static Puzzle Restore(PuzzleState saved)
    {
        var size = saved.Size;
        if (size <= 0 || saved.Rows.Count != size || saved.Rows.Any(row => row.Length != size))
            throw new RoundExpiredException();
        if (saved.Words.Count == 0)
            throw new RoundExpiredException();

        var grid = new char[size, size];
        for (var r = 0; r < size; r++)
        for (var c = 0; c < size; c++)
            grid[r, c] = saved.Rows[r][c];

        var solution = new int[size, size];
        for (var r = 0; r < size; r++)
        for (var c = 0; c < size; c++)
            solution[r, c] = -1;

        for (var i = 0; i < saved.Words.Count; i++)
        {
            var word = saved.Words[i];
            for (var k = 0; k < word.Text.Length; k++)
            {
                var r = word.Row + word.Dr * k;
                var c = word.Col + word.Dc * k;
                if (Inside(size, r, c)) solution[r, c] = i;
            }
        }

        var found = saved.Found.Length == saved.Words.Count
            ? saved.Found
            : new bool[saved.Words.Count];

        return new Puzzle
        {
            DifficultyId = saved.DifficultyId,
            CategoryId = saved.CategoryId,
            Size = size,
            Grid = grid,
            Solution = solution,
            Words = saved.Words,
            Found = found,
            HintsLeft = saved.HintsLeft,
            UniqueCells = saved.UniqueCells,
            OverlapPercent = saved.OverlapPercent
        };
    }

    private static Dictionary<int, List<Dictionary<string, int>>> Placements(Puzzle puzzle)
    {
        var map = new Dictionary<int, List<Dictionary<string, int>>>();
        for (var i = 0; i < puzzle.Words.Count; i++)
        {
            if (!puzzle.Found[i]) continue;
            var word = puzzle.Words[i];
            map[i] = Enumerable.Range(0, word.Text.Length)
                .Select(k => new Dictionary<string, int>
                {
                    ["r"] = word.Row + word.Dr * k,
                    ["c"] = word.Col + word.Dc * k
                })
                .ToList();
        }

        return map;
    }

    private sealed class PuzzleState
    {
        public string DifficultyId { get; set; } = "";
        public string CategoryId { get; set; } = "";
        public int Size { get; set; }
        public List<string> Rows { get; set; } = new();
        public List<PlacedWord> Words { get; set; } = new();
        public bool[] Found { get; set; } = System.Array.Empty<bool>();
        public int HintsLeft { get; set; }
        public int UniqueCells { get; set; }
        public double OverlapPercent { get; set; }
    }

    private sealed record DifficultySpec(
        string Id,
        int GridSize,
        int WordCount,
        (int Dr, int Dc)[] Directions,
        int MinWordLen,
        int MaxWordLen,
        int MinOverlapPercent,
        bool AvoidAdjacent)
    {
        public double MinDensity { get; init; }
        public bool StrictOverlap { get; init; }
        public int MaxRegenerations { get; init; }
    }

    private sealed record Candidate(string Text, string? Translation, string? Image);

    private sealed class PlacedWord
    {
        public string Text { get; set; } = "";
        public string? Translation { get; set; }
        public string? Image { get; set; }
        public int Row { get; set; }
        public int Col { get; set; }
        public int Dr { get; set; }
        public int Dc { get; set; }
    }

    private sealed class Puzzle
    {
        public string DifficultyId { get; set; } = "";
        public string CategoryId { get; set; } = "";
        public int Size { get; set; }
        public char[,] Grid { get; set; } = new char[0, 0];
        public int[,] Solution { get; set; } = new int[0, 0];
        public List<PlacedWord> Words { get; set; } = new();
        public bool[] Found { get; set; } = System.Array.Empty<bool>();
        public int HintsLeft { get; set; }
        public int UniqueCells { get; set; }
        public double OverlapPercent { get; set; }
    }
}

using System.Text.Json;
using System.Text.Json.Serialization;

namespace Oefenpad.Services.Games;

/// <summary>
/// Scheidbare werkwoorden, server-side. The same two steps as the Verb game,
/// text-first: the player first reads each verb with its split form, perfect
/// and an example, then picks the English meaning of the verb from four.
///
/// This is a sibling of <see cref="VerbService"/> rather than a generalisation
/// of it: the verbs round state is stored in accounts as JSON, so its shape
/// stays untouched, and here the options are glosses, not pictures.
/// </summary>
public sealed class SeparableService : GameService
{
    /// <summary>API segment and progress key.</summary>
    public const string Id = "separable";

    /// <summary>The answer plus at most this many distractors.</summary>
    private const int Distractors = 3;

    private readonly Dictionary<string, SeparableFrame> _byId;

    public SeparableService(GameContent content, RoundStore rounds)
        : base(content, rounds)
    {
        _byId = content.Separable.Frames.ToDictionary(f => f.Id, StringComparer.Ordinal);
    }

    public override string Game => Id;

    public override GameOptions Options()
    {
        var levels = Content.Separable.Levels.Select(level =>
        {
            var count = level.Frames.Count(_byId.ContainsKey);
            return new GameLevel(
                level.Id,
                level.Name,
                Subtitle: count == 1 ? "1 werkwoord" : $"{count} werkwoorden",
                Band: level.Band);
        }).ToList();

        return new GameOptions(System.Array.Empty<GameCategory>(), levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var levelId = String(input, "level");
        var level = Content.Separable.Levels.FirstOrDefault(l => l.Id == levelId)
            ?? throw new InvalidMoveException("Onbekend niveau.");

        var state = new RoundState
        {
            LevelId = level.Id,
            Steps = BuildSteps(level)
        };

        return Store(state, View(state));
    }

    public override RoundMove Move(string roundId, JsonElement move)
    {
        var state = State<RoundState>(roundId);
        var action = String(move, "action") ?? throw new InvalidMoveException("Geen actie.");

        return action switch
        {
            "next" => Next(state),
            "choose" => Choose(state, move),
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

    public override string? LevelOf(string roundId) => State<RoundState>(roundId).LevelId;

    /* =============================================================
       Steps
       ============================================================= */

    private List<Step> BuildSteps(Level level)
    {
        var frames = level.Frames.Where(_byId.ContainsKey).Select(id => _byId[id]).ToList();

        return new List<Step>
        {
            /* 1. Discover — input, no score. One card at a time. */
            new DiscoverStep { Cards = frames },

            /* 2. Choose the meaning. */
            new ChooseStep
            {
                Items = frames.Select(f => new ChooseItem
                {
                    Frame = f,
                    Options = Shuffle(OptionFrames(f, frames, Content.Separable.Frames))
                }).ToList()
            }
        };
    }

    /// <summary>
    /// The answer plus up to three distractors, unshuffled: first the other
    /// verbs of the level, then other verbs of the same band when the level
    /// is too small. No two options share a gloss, so there is always exactly
    /// one right answer. The caller shuffles once and stores the order in the
    /// round, so a resume shows the same board.
    /// </summary>
    public static List<SeparableFrame> OptionFrames(
        SeparableFrame frame,
        IReadOnlyList<SeparableFrame> level,
        IEnumerable<SeparableFrame> all)
    {
        var options = new List<SeparableFrame> { frame };
        var glosses = new HashSet<string>(StringComparer.OrdinalIgnoreCase) { Norm(frame.Gloss) };

        void Take(IEnumerable<SeparableFrame> pool)
        {
            foreach (var candidate in Shuffle(pool))
            {
                if (options.Count > Distractors) return;
                if (options.Any(o => o.Id == candidate.Id)) continue;
                if (string.IsNullOrWhiteSpace(candidate.Gloss)) continue;
                if (!glosses.Add(Norm(candidate.Gloss))) continue;
                options.Add(candidate);
            }
        }

        Take(level.Where(f => f.Id != frame.Id));
        Take(all.Where(f => f.Band == frame.Band && f.Id != frame.Id && !level.Any(l => l.Id == f.Id)));

        return options;
    }

    private static string Norm(string gloss) => gloss.Trim();

    private RoundMove Next(RoundState state)
    {
        var step = CurrentStep(state);

        // Discovery has no answer to give; every other step must be answered.
        if (step is ChooseStep && !state.Feedback)
            throw new InvalidMoveException("Beantwoord eerst de vraag.");

        state.Item++;
        ClearFeedback(state);

        if (state.Item >= ItemCount(step))
        {
            state.Item = 0;

            // Skip a step with no items, so a view never indexes item 0 of an
            // empty list.
            do
            {
                state.StepIndex++;
            }
            while (state.StepIndex < state.Steps.Count
                   && ItemCount(state.Steps[state.StepIndex]) == 0);

            if (state.StepIndex >= state.Steps.Count)
                return new RoundMove(FinishedView(state), Done: true,
                    CorrectCount: state.Correct, Total: state.Total);

            ClearFeedback(state);
        }

        return new RoundMove(View(state));
    }

    /// <summary>
    /// The player sends the position of the option, never a verb id: the ids
    /// are the infinitives, so sending them to the browser would give the
    /// answer away.
    /// </summary>
    private RoundMove Choose(RoundState state, JsonElement move)
    {
        var step = CurrentStep(state) as ChooseStep
            ?? throw new InvalidMoveException("Nu kies je geen betekenis.");
        if (state.Feedback) throw new InvalidMoveException("Dit item is al beantwoord.");

        var item = step.Items[state.Item];
        var chosen = Int(move, "option") ?? throw new InvalidMoveException("Geen betekenis gekozen.");
        if (chosen < 0 || chosen >= item.Options.Count)
            throw new InvalidMoveException("Onbekende betekenis.");

        var answer = item.Options.FindIndex(o => o.Id == item.Frame.Id);
        var correct = chosen == answer;
        state.Total++;
        if (correct) state.Correct++;

        state.Feedback = true;
        state.LastCorrect = correct;
        state.CorrectOption = answer;
        state.ChosenOption = chosen;

        state.LastExplanation = correct
            ? Text("gloss-correct", ("verb", item.Frame.Verb), ("en", item.Frame.Gloss))
            : Text("gloss-wrong", ("verb", item.Frame.Verb), ("en", item.Frame.Gloss),
                ("other", item.Options[chosen].Gloss));

        return new RoundMove(View(state), Correct: state.LastCorrect,
            Explanation: state.LastExplanation,
            CorrectCount: state.Correct, Total: state.Total);
    }

    /* =============================================================
       Views
       ============================================================= */

    private object View(RoundState state)
    {
        var step = CurrentStep(state);

        object content = step switch
        {
            DiscoverStep discover => DiscoverView(discover, state),
            ChooseStep choose => ChooseView(choose, state),
            _ => throw new InvalidOperationException("Onbekende stap.")
        };

        var view = new Dictionary<string, object?>
        {
            ["kind"] = step.Kind,
            ["level"] = state.LevelId,
            ["stepIndex"] = state.StepIndex,
            ["item"] = state.Item,
            ["count"] = ItemCount(step),
            ["steps"] = state.Steps.Select(s => s.Kind).ToList(),
            ["correct"] = state.Correct,
            ["total"] = state.Total,
            ["phase"] = state.Feedback ? "feedback" : "question",
            ["content"] = content
        };

        if (state.Feedback)
        {
            view["feedback"] = new Dictionary<string, object?>
            {
                ["correct"] = state.LastCorrect,
                ["explanation"] = state.LastExplanation,
                ["correctOption"] = state.CorrectOption,
                ["chosenOption"] = state.ChosenOption
            };
        }

        return view;
    }

    private object DiscoverView(DiscoverStep step, RoundState state)
    {
        var frame = step.Cards[state.Item];

        return new Dictionary<string, object?>
        {
            ["card"] = new Dictionary<string, object?>
            {
                ["image"] = Image(frame.Scene),
                ["verb"] = frame.Verb,
                ["gloss"] = frame.Gloss,
                ["split"] = frame.Split,
                ["perfect"] = frame.Perfect,
                ["example"] = frame.Example,
                ["exampleEn"] = frame.ExampleEn
            }
        };
    }

    private static object ChooseView(ChooseStep step, RoundState state)
    {
        var item = step.Items[state.Item];
        return new Dictionary<string, object?>
        {
            ["verb"] = item.Frame.Verb,
            ["example"] = item.Frame.Example,
            ["options"] = item.Options.Select(o => o.Gloss).ToList()
        };
    }

    private static object FinishedView(RoundState state) => new
    {
        done = true,
        correct = state.Correct,
        total = state.Total,
        level = state.LevelId
    };

    /// <summary>The drawing for a card, or null when it has none.</summary>
    private object? Image(string? sceneId)
    {
        if (string.IsNullOrWhiteSpace(sceneId)
            || !Content.Separable.Scenes.TryGetValue(sceneId, out var scene)
            || string.IsNullOrWhiteSpace(scene.File))
            return null;

        return new
        {
            id = sceneId,
            url = "/assets/" + scene.File,
            alt = scene.Alt
        };
    }

    /* =============================================================
       Housekeeping
       ============================================================= */

    private static Step CurrentStep(RoundState state)
    {
        if (state.StepIndex < 0 || state.StepIndex >= state.Steps.Count)
            throw new RoundExpiredException();

        return state.Steps[state.StepIndex];
    }

    private static int ItemCount(Step step) => step switch
    {
        DiscoverStep d => d.Cards.Count,
        ChooseStep c => c.Items.Count,
        _ => 0
    };

    private static void ClearFeedback(RoundState state)
    {
        state.Feedback = false;
        state.LastCorrect = null;
        state.LastExplanation = null;
        state.CorrectOption = null;
        state.ChosenOption = null;
    }

    /* ---------- state ---------- */

    private sealed class RoundState
    {
        public string LevelId { get; set; } = "";
        public List<Step> Steps { get; set; } = new();
        public int StepIndex { get; set; }
        public int Item { get; set; }
        public int Correct { get; set; }
        public int Total { get; set; }
        public bool Feedback { get; set; }
        public bool? LastCorrect { get; set; }
        public string? LastExplanation { get; set; }
        public int? CorrectOption { get; set; }
        public int? ChosenOption { get; set; }
    }

    [JsonPolymorphic]
    [JsonDerivedType(typeof(DiscoverStep), "discover")]
    [JsonDerivedType(typeof(ChooseStep), "choose")]
    private abstract class Step
    {
        public abstract string Kind { get; }
    }

    private sealed class DiscoverStep : Step
    {
        public override string Kind => "discover";
        public List<SeparableFrame> Cards { get; set; } = new();
    }

    private sealed class ChooseStep : Step
    {
        public override string Kind => "choose";
        public List<ChooseItem> Items { get; set; } = new();
    }

    private sealed class ChooseItem
    {
        public SeparableFrame Frame { get; set; } = new();
        public List<SeparableFrame> Options { get; set; } = new();
    }
}

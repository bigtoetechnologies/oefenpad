using System.Text.Json;
using System.Text.Json.Serialization;

namespace Oefenpad.Services.Games;

/// <summary>
/// The Verb game, server-side. A level is four or five drawn verbs; the player
/// first sees each picture with its infinitive and gloss, then chooses the
/// picture that belongs to a verb. The browser never receives the answer: the
/// scene ids and the option order stay in the round.
///
/// There is no example sentence and no conjugation drill. An irregular verb
/// shows the past singular and the perfect as forms to recognise, not as a
/// grammar lesson; see Docs/werkwoorden/AGENTS.html.
/// </summary>
public sealed class VerbService : GameService
{
    /// <summary>API segment and progress key.</summary>
    public const string Id = "verbs";

    private readonly Dictionary<string, VerbFrame> _byId;

    public VerbService(GameContent content, RoundStore rounds)
        : base(content, rounds)
    {
        _byId = content.Verbs.Frames.ToDictionary(f => f.Id, StringComparer.Ordinal);
    }

    public override string Game => Id;

    public override GameOptions Options()
    {
        var levels = Content.Verbs.Levels.Select(level =>
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
        var level = Content.Verbs.Levels.FirstOrDefault(l => l.Id == levelId)
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

            /* 2. Choose the picture. The options are this level's other verbs. */
            new ChooseStep
            {
                Items = frames.Select(f => new ChooseItem
                {
                    Frame = f,
                    Options = OptionsFor(f, frames)
                }).ToList()
            }
        };
    }

    /// <summary>
    /// Four pictures at most: the answer plus three other verbs from the level.
    /// The order is stored in the round, so a resume shows exactly the same
    /// board instead of reshuffling it under the player.
    /// </summary>
    private static List<string> OptionsFor(VerbFrame frame, List<VerbFrame> frames)
    {
        var distractors = frames
            .Where(f => f.Id != frame.Id)
            .Select(f => f.Scene)
            .OrderBy(_ => Random.Shared.Next())
            .Take(3);

        return new[] { frame.Scene }
            .Concat(distractors)
            .OrderBy(_ => Random.Shared.Next())
            .ToList();
    }

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

    private RoundMove Choose(RoundState state, JsonElement move)
    {
        var step = CurrentStep(state) as ChooseStep
            ?? throw new InvalidMoveException("Nu kies je geen beeld.");
        if (state.Feedback) throw new InvalidMoveException("Dit item is al beantwoord.");

        var item = step.Items[state.Item];
        var chosen = String(move, "scene") ?? throw new InvalidMoveException("Geen beeld gekozen.");
        if (!item.Options.Contains(chosen)) throw new InvalidMoveException("Onbekend beeld.");

        var correct = chosen == item.Frame.Scene;
        state.Total++;
        if (correct) state.Correct++;

        state.Feedback = true;
        state.LastCorrect = correct;
        state.CorrectScene = item.Frame.Scene;
        state.ChosenScene = chosen;

        if (correct)
        {
            state.LastExplanation = Text("image-correct",
                ("verb", item.Frame.Verb), ("en", item.Frame.Gloss));
        }
        else
        {
            var other = _byId.Values.FirstOrDefault(f => f.Scene == chosen);
            state.LastExplanation = Text("image-wrong",
                ("verb", item.Frame.Verb), ("en", item.Frame.Gloss),
                ("other", other?.Verb ?? "?"));
        }

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
                ["correctScene"] = state.CorrectScene,
                ["chosenScene"] = state.ChosenScene
            };
        }

        return view;
    }

    private object DiscoverView(DiscoverStep step, RoundState state)
    {
        var frame = step.Cards[state.Item];
        var forms = new List<string>();
        if (!string.IsNullOrWhiteSpace(frame.Past)) forms.Add(frame.Past!);
        if (!string.IsNullOrWhiteSpace(frame.Perfect)) forms.Add(frame.Perfect!);

        return new Dictionary<string, object?>
        {
            ["card"] = new Dictionary<string, object?>
            {
                ["image"] = Image(frame.Scene),
                ["verb"] = frame.Verb,
                ["gloss"] = frame.Gloss,
                ["forms"] = forms,
                ["regular"] = frame.Regular
            }
        };
    }

    private object ChooseView(ChooseStep step, RoundState state)
    {
        var item = step.Items[state.Item];
        return new Dictionary<string, object?>
        {
            ["verb"] = item.Frame.Verb,
            ["options"] = item.Options.Select(Image).ToList()
        };
    }

    private object FinishedView(RoundState state) => new
    {
        done = true,
        correct = state.Correct,
        total = state.Total,
        level = state.LevelId
    };

    private object Image(string sceneId)
    {
        if (!Content.Verbs.Scenes.TryGetValue(sceneId, out var scene))
            return new { id = sceneId, url = "", alt = "" };

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
        state.CorrectScene = null;
        state.ChosenScene = null;
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
        public string? CorrectScene { get; set; }
        public string? ChosenScene { get; set; }
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
        public List<VerbFrame> Cards { get; set; } = new();
    }

    private sealed class ChooseStep : Step
    {
        public override string Kind => "choose";
        public List<ChooseItem> Items { get; set; } = new();
    }

    private sealed class ChooseItem
    {
        public VerbFrame Frame { get; set; } = new();
        public List<string> Options { get; set; } = new();
    }
}

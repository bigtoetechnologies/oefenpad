using System.Text.Json;
using System.Text.Json.Serialization;

namespace Oefenpad.Services.Games;

/// <summary>
/// Prepositions, server-side. The frames, scenes and examples are embedded
/// resources; the browser receives only the current card and never the
/// contrast partner or the tile order. Every answer is judged here.
/// </summary>
public sealed class PrepositionsService : GameService
{
    /// <summary>API segment and progress key.</summary>
    public const string Id = "prepositions";

    private readonly Dictionary<string, PrepositionFrame> _byId;
    private readonly List<PrepositionFrame> _practiceable;

    public PrepositionsService(GameContent content, RoundStore rounds)
        : base(content, rounds)
    {
        _byId = content.Prepositions.Frames.ToDictionary(f => f.Id, StringComparer.Ordinal);
        _practiceable = content.Prepositions.Frames.Where(f => !f.DiscoverOnly).ToList();
    }

    public override string Game => Id;

    public override GameOptions Options()
    {
        // The level list is metadata only. It used to join every frame phrase
        // into the subtitle, which handed the whole phrase inventory to any
        // caller of /options; a count of the scenes says as much and nothing more.
        var levels = Content.Prepositions.Levels.Select(level =>
        {
            var count = level.Frames.Count(_byId.ContainsKey);
            return new GameLevel(
                level.Id,
                level.Name,
                Subtitle: count == 1 ? "1 beeld" : $"{count} beelden");
        }).ToList();

        return new GameOptions(System.Array.Empty<GameCategory>(), levels);
    }

    public override RoundStart Start(JsonElement input)
    {
        var levelId = String(input, "level");
        var level = Content.Prepositions.Levels.FirstOrDefault(l => l.Id == levelId)
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
            "concept" => Concept(state, move),
            "choose" => Choose(state, move),
            "trueFalse" => TrueFalse(state, move),
            "build" => Build(state, move),
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
        var steps = new List<Step>();

        /* 1. Discover — input, no score. */
        var cards = frames.ToList();
        foreach (var extra in level.Extra ?? new List<string>())
        {
            if (_byId.TryGetValue(extra, out var frame)) cards.Add(frame);
        }
        steps.Add(new DiscoverStep { Cards = cards });

        /* 2. Choose the picture. */
        steps.Add(new ChooseStep
        {
            Items = frames.Select(f => new ChooseItem
            {
                Frame = f,
                Options = OptionsFor(f, level)
            }).ToList()
        });

        /* 3. Does the sentence fit? Only when the pair is in this level. */
        var hasContrast = frames.Any(f =>
            f.Contrast is not null && level.Frames.Contains(f.Contrast));

        if (hasContrast)
        {
            var items = new List<TrueFalseItem>();
            foreach (var f in frames)
            {
                if (f.Contrast is null || !_byId.TryGetValue(f.Contrast, out var partner)) continue;
                items.Add(new TrueFalseItem { Frame = f, SentenceFrame = f, Truth = true });
                items.Add(new TrueFalseItem { Frame = f, SentenceFrame = partner, Truth = false });
            }
            steps.Add(new TrueFalseStep { Items = Shuffle(items) });
        }

        /* 4. Build the sentence. */
        var builds = new List<BuildItem>();
        foreach (var f in frames)
        {
            foreach (var tokens in f.Build)
            {
                var tiles = tokens
                    .Select(text => new Tile { Id = Guid.NewGuid().ToString("N"), Text = text })
                    .ToList();

                var shuffled = Shuffle(tiles);
                // Never open with the answer already in the right order.
                if (shuffled.Select(t => t.Text).SequenceEqual(tokens) && tokens.Count > 1)
                    shuffled = Shuffle(tiles);

                builds.Add(new BuildItem { Frame = f, Target = tokens, Tiles = shuffled });
            }
        }
        steps.Add(new BuildStep { Items = builds });

        // A step with nothing in it would be rendered by indexing item 0 of an
        // empty list. Content can leave one empty (a frame with no build tokens,
        // an id that no longer resolves), so drop them here rather than trust it.
        return steps.Where(step => ItemCount(step) > 0).ToList();
    }

    private List<string> OptionsFor(PrepositionFrame frame, Level level)
    {
        var inside = level.Frames
            .Where(_byId.ContainsKey)
            .Select(id => _byId[id].Scene)
            .ToList();

        var outside = Shuffle(_practiceable
            .Where(f => !level.Frames.Contains(f.Id))
            .Select(f => f.Scene));

        var options = inside.ToList();
        var index = 0;
        while (options.Count < 3 && index < outside.Count)
        {
            var scene = outside[index++];
            if (!options.Contains(scene)) options.Add(scene);
        }

        return Shuffle(options);
    }

    /* =============================================================
       Actions
       ============================================================= */

    private RoundMove Next(RoundState state)
    {
        var step = CurrentStep(state);

        if (step is DiscoverStep)
        {
            // Discovery advances one card at a time; no answer to clear.
        }
        else if (!state.Feedback)
        {
            throw new InvalidMoveException("Beantwoord eerst de vraag.");
        }

        state.Item++;
        ClearFeedback(state);

        if (state.Item >= ItemCount(step))
        {
            state.Item = 0;

            // Step past anything with no items: a level whose content leaves a
            // step empty would otherwise render a view that indexes item 0 of an
            // empty list and 500s on every retry.
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

    private RoundMove Concept(RoundState state, JsonElement move)
    {
        if (state.Feedback is false || state.ConceptFrame is null)
            throw new InvalidMoveException("Er is geen conceptvraag.");

        var answer = Bool(move, "answer")
            ?? throw new InvalidMoveException("Geen antwoord.");

        state.ConceptAnswer = answer;
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
                ("frame", item.Frame.Frame), ("en", item.Frame.En));
        }
        else
        {
            var wrong = Content.Prepositions.Frames.FirstOrDefault(f => f.Scene == chosen);
            state.LastExplanation = Text("image-wrong",
                ("other", wrong is null ? Text("image-other") : wrong.Frame),
                ("frame", item.Frame.Frame));
        }

        return Result(state);
    }

    private RoundMove TrueFalse(RoundState state, JsonElement move)
    {
        var step = CurrentStep(state) as TrueFalseStep
            ?? throw new InvalidMoveException("Nu klopt er geen zin.");
        if (state.Feedback) throw new InvalidMoveException("Dit item is al beantwoord.");

        var item = step.Items[state.Item];
        var answer = Bool(move, "answer")
            ?? throw new InvalidMoveException("Geen antwoord.");

        var right = answer == item.Truth;
        state.Total++;
        if (right) state.Correct++;

        state.Feedback = true;
        state.LastCorrect = right;
        state.Expected = item.Truth;
        state.Chosen = answer;

        if (item.Truth)
        {
            state.LastExplanation = right
                ? Text("truth-correct", ("frame", item.Frame.Frame), ("en", item.Frame.En))
                : Text("truth-wrong-yes", ("frame", item.Frame.Frame));
        }
        else
        {
            // A false item is answered correctly with "nee", so the explanation
            // has to open with "Klopt" there, not with "Nee".
            state.LastExplanation = Text(
                right ? "truth-correct-no" : "truth-wrong-no",
                ("frame", item.Frame.Frame), ("used", item.SentenceFrame.Frame));
        }

        // The gloss ends without punctuation, so give the example sentence its own
        // sentence instead of running it on after "— to wait for".
        state.LastExplanation += (state.LastExplanation.EndsWith('.') ? " " : ". ")
            + Text("sentence-for-image", ("sentence", item.Frame.Example.Nl));

        // The concept question is about meaning, asked only after the form.
        state.ConceptFrame = item.Frame.Concept.Count > 0 ? item.Frame : null;
        state.ConceptAnswer = null;

        return Result(state);
    }

    private RoundMove Build(RoundState state, JsonElement move)
    {
        var step = CurrentStep(state) as BuildStep
            ?? throw new InvalidMoveException("Nu bouw je geen zin.");
        if (state.Feedback) throw new InvalidMoveException("Deze zin is al gecontroleerd.");

        var item = step.Items[state.Item];
        var chosen = Array(move, "tiles")
            .Select(t => t.ValueKind == JsonValueKind.String ? t.GetString() : null)
            .Where(x => x is not null)
            .Select(x => x!)
            .ToList();

        if (chosen.Count != item.Target.Count || chosen.Distinct().Count() != chosen.Count)
            throw new InvalidMoveException("Niet alle tegels zijn gebruikt.");

        var byId = item.Tiles.ToDictionary(t => t.Id, t => t.Text);
        if (chosen.Any(id => !byId.ContainsKey(id)))
            throw new InvalidMoveException("Onbekende tegel.");

        var answer = chosen.Select(id => byId[id]).ToList();
        var correct = answer.SequenceEqual(item.Target);

        state.Total++;
        if (correct) state.Correct++;

        state.Feedback = true;
        state.LastCorrect = correct;
        state.BuildTarget = string.Join(" ", item.Target) + ".";

        var prefixLast = item.Frame.Prefix is not null &&
                         answer.Contains(item.Frame.Prefix) &&
                         answer.LastIndexOf(item.Frame.Prefix) == item.Target.Count - 1;

        if (correct)
        {
            state.LastExplanation = item.Frame.Prefix is not null
                ? Text("build-correct-prefix", ("prefix", item.Frame.Prefix))
                : Text("build-correct");
        }
        else if (item.Frame.Prefix is not null &&
                 answer.Contains(item.Frame.Prefix) && !prefixLast)
        {
            state.LastExplanation = Text("build-almost", ("prefix", item.Frame.Prefix));
        }
        else
        {
            state.LastExplanation = Text("build-wrong");
        }

        state.LastExplanation += " " + Text("build-answer", ("sentence", state.BuildTarget));

        return Result(state);
    }

    private RoundMove Result(RoundState state) =>
        new(View(state), Correct: state.LastCorrect,
            Explanation: state.LastExplanation,
            CorrectCount: state.Correct, Total: state.Total);

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
            TrueFalseStep trueFalse => TrueFalseView(trueFalse, state),
            BuildStep build => BuildView(build, state),
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
                ["chosenScene"] = state.ChosenScene,
                ["expected"] = state.Expected,
                ["chosen"] = state.Chosen,
                ["target"] = state.BuildTarget,
                ["concept"] = state.ConceptFrame is null
                    ? null
                    : new
                    {
                        question = state.ConceptFrame.Concept[0].Question,
                        answer = state.ConceptAnswer,
                        explanation = state.ConceptAnswer is null
                            ? null
                            : Text(
                                state.ConceptFrame.Concept[0].Answer ? "concept-yes" : "concept-no",
                                ("nl", state.ConceptFrame.Example.Nl))
                    }
            };
        }

        return view;
    }

    private object DiscoverView(DiscoverStep step, RoundState state)
    {
        var f = step.Cards[state.Item];
        return new Dictionary<string, object?>
        {
            ["card"] = new Dictionary<string, object?>
            {
                ["image"] = Image(f.Scene),
                ["sentence"] = f.Example.Nl,
                ["focus"] = f.Focus,
                ["meaning"] = f.En,
                ["form"] = f.Pronominal is null
                    ? null
                    : Text("shorter", ("pronominal", f.Pronominal.Nl), ("en", f.Pronominal.En)),
                ["notice"] = f.Prefix is null
                    ? null
                    : Text("separable-notice", ("prefix", f.Prefix), ("frame", f.Frame))
            }
        };
    }

    private object ChooseView(ChooseStep step, RoundState state)
    {
        var item = step.Items[state.Item];
        return new Dictionary<string, object?>
        {
            ["sentence"] = item.Frame.Example.Nl,
            ["focus"] = item.Frame.Focus,
            ["options"] = item.Options.Select(Image).ToList()
        };
    }

    private object TrueFalseView(TrueFalseStep step, RoundState state)
    {
        var item = step.Items[state.Item];
        return new Dictionary<string, object?>
        {
            ["image"] = Image(item.Frame.Scene),
            ["sentence"] = item.SentenceFrame.Example.Nl,
            ["focus"] = item.SentenceFrame.Focus
        };
    }

    private object BuildView(BuildStep step, RoundState state)
    {
        var item = step.Items[state.Item];
        var hint = item.Frame.Prefix is null
            ? Text("build-hint", ("frame", item.Frame.Frame))
            : Text("build-hint-prefix", ("frame", item.Frame.Frame), ("prefix", item.Frame.Prefix));

        return new Dictionary<string, object?>
        {
            ["frame"] = item.Frame.Frame,
            ["hint"] = hint,
            ["image"] = Image(item.Frame.Scene),
            ["tiles"] = item.Tiles.Select(t => new { id = t.Id, text = t.Text }).ToList()
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
        if (!Content.Prepositions.Scenes.TryGetValue(sceneId, out var scene))
            return new { id = sceneId, url = "", alt = "" };

        return new
        {
            id = sceneId,
            url = "/assets/voorzetselpaden/" + Path.GetFileName(scene.File),
            alt = scene.Alt
        };
    }

    /* =============================================================
       Housekeeping
       ============================================================= */

    private static Step CurrentStep(RoundState state)
    {
        // The round is left in the store after it ends, so a double-click on the
        // last "volgende" sends a second action for a finished round. Answer that
        // as an expired round (410) rather than letting the indexer throw a 500.
        if (state.StepIndex < 0 || state.StepIndex >= state.Steps.Count)
            throw new RoundExpiredException();

        return state.Steps[state.StepIndex];
    }

    private static int ItemCount(Step step) => step switch
    {
        DiscoverStep d => d.Cards.Count,
        ChooseStep c => c.Items.Count,
        TrueFalseStep t => t.Items.Count,
        BuildStep b => b.Items.Count,
        _ => 0
    };

    private static void ClearFeedback(RoundState state)
    {
        state.Feedback = false;
        state.LastCorrect = null;
        state.LastExplanation = null;
        state.CorrectScene = null;
        state.ChosenScene = null;
        state.Expected = null;
        state.Chosen = null;
        state.BuildTarget = null;
        state.ConceptFrame = null;
        state.ConceptAnswer = null;
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
        public bool? Expected { get; set; }
        public bool? Chosen { get; set; }
        public string? BuildTarget { get; set; }
        public PrepositionFrame? ConceptFrame { get; set; }
        public bool? ConceptAnswer { get; set; }
    }

    [JsonPolymorphic]
    [JsonDerivedType(typeof(DiscoverStep), "discover")]
    [JsonDerivedType(typeof(ChooseStep), "choose")]
    [JsonDerivedType(typeof(TrueFalseStep), "trueFalse")]
    [JsonDerivedType(typeof(BuildStep), "build")]
    private abstract class Step
    {
        public abstract string Kind { get; }
    }

    private sealed class DiscoverStep : Step
    {
        public override string Kind => "discover";
        public List<PrepositionFrame> Cards { get; set; } = new();
    }

    private sealed class ChooseStep : Step
    {
        public override string Kind => "choose";
        public List<ChooseItem> Items { get; set; } = new();
    }

    private sealed class ChooseItem
    {
        public PrepositionFrame Frame { get; set; } = new();
        public List<string> Options { get; set; } = new();
    }

    private sealed class TrueFalseStep : Step
    {
        public override string Kind => "trueFalse";
        public List<TrueFalseItem> Items { get; set; } = new();
    }

    private sealed class TrueFalseItem
    {
        public PrepositionFrame Frame { get; set; } = new();
        public PrepositionFrame SentenceFrame { get; set; } = new();
        public bool Truth { get; set; }
    }

    private sealed class BuildStep : Step
    {
        public override string Kind => "build";
        public List<BuildItem> Items { get; set; } = new();
    }

    private sealed class BuildItem
    {
        public PrepositionFrame Frame { get; set; } = new();
        public List<string> Target { get; set; } = new();
        public List<Tile> Tiles { get; set; } = new();
    }

    private sealed class Tile
    {
        public string Id { get; set; } = "";
        public string Text { get; set; } = "";
    }
}

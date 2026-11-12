using System.Text.Json;
using FluentAssertions;
using Oefenpad.Services.Games;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// The embedded content is the one copy of the games' data. These tests pin
/// the shape the services and the meta counts rely on, so a bad content edit
/// fails here rather than in a browser.
/// </summary>
public sealed class GameContentTests
{
    private readonly GameContent _content = new();

    [Fact]
    public void Counts_match_the_meta_table()
    {
        var meta = _content.Meta;

        _content.Categories.Should().HaveCount(meta.Categories);
        _content.Categories.Values.Sum(c => c.Words.Count).Should().Be(meta.Words);
        _content.WordImages.Should().HaveCount(meta.WordImages);
        _content.Prepositions.Scenes.Should().HaveCount(meta.Scenes);
        _content.Prepositions.Frames.Should().HaveCount(meta.Frames);
        _content.Prepositions.Levels.Should().HaveCount(meta.Levels);
        _content.Reels.Should().HaveCount(meta.Reels);
    }

    [Fact]
    public void Every_text_bank_is_present_and_non_empty()
    {
        foreach (var game in new[]
                 {
                     "hangman", "memory", "matching", "wordsearch",
                     "prepositions", "storymachine"
                 })
        {
            var texts = _content.Texts(game);
            texts.Should().NotBeEmpty($"{game} needs its Dutch interface strings");
            texts.Values.Should().OnlyContain(value => !string.IsNullOrWhiteSpace(value));
        }
    }

    [Fact]
    public void Every_preposition_level_points_at_known_frames_and_scenes()
    {
        var frames = _content.Prepositions.Frames.ToDictionary(f => f.Id);
        var scenes = _content.Prepositions.Scenes;

        foreach (var level in _content.Prepositions.Levels)
        {
            level.Frames.Should().NotBeEmpty();
            foreach (var id in level.Frames)
            {
                frames.Should().ContainKey(id);
                scenes.Should().ContainKey(frames[id].Scene);
            }
        }
    }

    [Fact]
    public void Every_preposition_frame_builds_a_sentence_from_its_tokens()
    {
        foreach (var frame in _content.Prepositions.Frames)
        {
            frame.Build.Should().NotBeEmpty($"{frame.Id} needs at least one sentence");
            foreach (var sentence in frame.Build)
            {
                sentence.Should().NotBeEmpty();
                sentence.Should().OnlyContain(token => !string.IsNullOrWhiteSpace(token));
            }
        }
    }

    [Fact]
    public void Every_reel_has_tiles_in_both_languages()
    {
        foreach (var reel in _content.Reels)
        {
            reel.Tiles.Should().NotBeEmpty();
            reel.Tiles.Should().OnlyContain(tile =>
                !string.IsNullOrWhiteSpace(tile.Nl) &&
                !string.IsNullOrWhiteSpace(tile.En) &&
                !string.IsNullOrWhiteSpace(tile.Art));
        }
    }
}

/// <summary>
/// The round model: a service builds its steps once, and a round it never
/// stored is expired rather than an error page.
/// </summary>
public sealed class GameRoundTests
{
    private static readonly GameContent Content = new();

    private static JsonElement Body(object value) => JsonSerializer.SerializeToElement(value);

    private static JsonElement Json(object value) => JsonSerializer.SerializeToElement(value);

    [Fact]
    public void Every_level_with_a_contrast_pair_builds_four_steps_and_the_rest_three()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var frames = Content.Prepositions.Frames.ToDictionary(f => f.Id);

        foreach (var level in Content.Prepositions.Levels)
        {
            var round = service.Start(Body(new { level = level.Id }));
            var view = Json(round.View);

            var hasContrast = level.Frames
                .Where(frames.ContainsKey)
                .Any(id => frames[id].Contrast is { } other && level.Frames.Contains(other));

            var steps = view.GetProperty("steps");
            steps.GetArrayLength().Should().Be(
                hasContrast ? 4 : 3,
                $"{level.Id} has {(hasContrast ? "" : "no ")}contrast partner in the level");
        }
    }

    [Fact]
    public void A_round_opens_on_the_discover_step()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var level = Content.Prepositions.Levels.First(l => l.Id == "wachten");

        var view = Json(service.Start(Body(new { level = level.Id })).View);
        var kinds = view.GetProperty("steps").EnumerateArray()
            .Select(kind => kind.GetString()).ToList();

        kinds.Should().Contain("discover");
        view.GetProperty("kind").GetString().Should().Be("discover");
    }

    [Fact]
    public void Concept_feedback_repeats_the_scene_sentence_instead_of_the_gloss()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var round = service.Start(Body(new { level = "wachten" }));

        // Walk the discover cards and every picture to choose; the number of
        // frames per level varies. The sentence step is the one to answer.
        var view = Json(round.View);
        for (var guard = 0; guard < 50; guard++)
        {
            var kind = view.GetProperty("kind").GetString();
            var phase = view.GetProperty("phase").GetString();
            if (kind == "trueFalse" && phase == "question") break;

            var action = kind == "choose" && phase == "question"
                ? Body(new
                {
                    action = "choose",
                    scene = view.GetProperty("content").GetProperty("options")[0]
                        .GetProperty("id").GetString()
                })
                : Body(new { action = "next" });

            view = Json(service.Move(round.RoundId, action).View);
        }

        view.GetProperty("kind").GetString().Should().Be("trueFalse");
        view.GetProperty("phase").GetString().Should().Be("question");

        // Answering the sentence question raises the concept question.
        view = Json(service.Move(
            round.RoundId, Body(new { action = "trueFalse", answer = true })).View);
        view.GetProperty("feedback").GetProperty("concept").ValueKind
            .Should().NotBe(JsonValueKind.Null);

        // The concept answer repeats the card's Dutch sentence. The English
        // gloss used to follow "Ja.", which read as "Ja. to wait in front of."
        view = Json(service.Move(
            round.RoundId, Body(new { action = "concept", answer = true })).View);
        var explanation = view.GetProperty("feedback").GetProperty("concept")
            .GetProperty("explanation").GetString();

        explanation.Should().StartWith("Ja. ");

        var sentences = Content.Prepositions.Frames.Select(frame => frame.Example.Nl).ToList();
        sentences.Should().Contain(sentence =>
            explanation!.EndsWith(sentence, StringComparison.Ordinal));

        var glosses = Content.Prepositions.Frames
            .Select(frame => frame.En)
            .Where(gloss => !string.IsNullOrEmpty(gloss))
            .ToList();
        glosses.Should().OnlyContain(gloss =>
            !explanation!.Contains(gloss!, StringComparison.Ordinal));
    }

    [Fact]
    public void An_unknown_round_is_expired()
    {
        var service = new HangmanService(Content, new RoundStore());

        Assert.Throws<RoundExpiredException>(
            () => service.Move("does-not-exist", Body(new { action = "hint" })));
    }

    [Fact]
    public void An_unknown_level_is_refused_at_start()
    {
        var service = new PrepositionsService(Content, new RoundStore());

        Assert.Throws<InvalidMoveException>(
            () => service.Start(Body(new { level = "no-such-level" })));
    }

    [Fact]
    public void The_word_search_view_carries_no_placements()
    {
        var service = new WordSearchService(Content, new RoundStore());
        var view = Json(service.Start(Body(new { category = "animals", difficulty = "beginner" })).View);

        view.TryGetProperty("placements", out _).Should().BeFalse();
        view.GetProperty("grid").GetArrayLength().Should().Be(view.GetProperty("size").GetInt32());
        view.GetProperty("words").GetArrayLength().Should().BeGreaterThan(0);
        view.GetProperty("found").EnumerateArray().Should().OnlyContain(found => !found.GetBoolean());
    }

    [Fact]
    public void The_prepositions_options_carry_no_frame_phrases()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var phrases = Content.Prepositions.Frames.Select(frame => frame.Frame).ToList();

        service.Options().Levels.Should().OnlyContain(level =>
            phrases.All(phrase => !(level.Subtitle ?? string.Empty).Contains(phrase)));
    }

    [Fact]
    public void Round_store_expires_a_round_and_refuses_the_wrong_game()
    {
        var store = new RoundStore();

        var expired = store.Save("hangman", new object(), TimeSpan.FromMilliseconds(-1));
        store.Get(expired, "hangman").Should().BeNull();

        var live = store.Save("hangman", new object());
        store.Get(live, "memory").Should().BeNull();
    }
}

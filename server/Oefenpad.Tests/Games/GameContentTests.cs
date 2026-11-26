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
                     "prepositions", "verbs", "separable", "storymachine"
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
    public void Every_verb_level_points_at_known_frames_and_scenes()
    {
        var frames = _content.Verbs.Frames.ToDictionary(f => f.Id);

        foreach (var level in _content.Verbs.Levels)
        {
            level.Frames.Should().HaveCountGreaterThanOrEqualTo(2,
                "the choose step needs at least one distractor");
            foreach (var id in level.Frames)
            {
                frames.Should().ContainKey(id);
                _content.Verbs.Scenes.Should().ContainKey(frames[id].Scene);
            }
        }
    }

    [Fact]
    public void Every_verb_frame_has_an_image_and_predictable_forms()
    {
        foreach (var frame in _content.Verbs.Frames)
        {
            _content.Verbs.Scenes.Should().ContainKey(frame.Scene);
            frame.Verb.Should().NotBeNullOrWhiteSpace();
            frame.Gloss.Should().NotBeNullOrWhiteSpace();
            frame.Band.Should().NotBeNullOrWhiteSpace();

            // The generator writes both forms or neither: a regular verb has no
            // past/perfect line, an irregular one has the pair.
            (frame.Past is null).Should().Be(frame.Perfect is null, $"{frame.Id} has half a forms pair");
        }
    }

    [Fact]
    public void Every_separable_level_points_at_known_frames_of_its_band()
    {
        var frames = _content.Separable.Frames.ToDictionary(f => f.Id);
        _content.Separable.Levels.Should().NotBeEmpty();

        foreach (var level in _content.Separable.Levels)
        {
            level.Frames.Should().NotBeEmpty();
            foreach (var id in level.Frames)
            {
                frames.Should().ContainKey(id);
                frames[id].Band.Should().Be(level.Band, $"{id} sits in {level.Id}");
            }
        }
    }

    [Fact]
    public void Every_separable_frame_has_its_forms_and_an_example()
    {
        foreach (var frame in _content.Separable.Frames)
        {
            frame.Verb.Should().NotBeNullOrWhiteSpace();
            frame.Gloss.Should().NotBeNullOrWhiteSpace();
            frame.Band.Should().NotBeNullOrWhiteSpace();
            frame.Split.Should().NotBeNullOrWhiteSpace($"{frame.Id} needs its split form");
            frame.Perfect.Should().NotBeNullOrWhiteSpace($"{frame.Id} needs its perfect");
            frame.Example.Should().NotBeNullOrWhiteSpace($"{frame.Id} needs an example");
            frame.ExampleEn.Should().NotBeNullOrWhiteSpace($"{frame.Id} needs the example's translation");

            // A scene is optional, but one that is named must exist.
            if (frame.Scene is not null)
                _content.Separable.Scenes.Should().ContainKey(frame.Scene);
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
    public void Every_level_whose_frames_have_a_contrast_partner_builds_four_steps()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var frames = Content.Prepositions.Frames.ToDictionary(f => f.Id);

        foreach (var level in Content.Prepositions.Levels)
        {
            var round = service.Start(Body(new { level = level.Id }));
            var view = Json(round.View);

            // The partner now lives in another level: a level is one chunk, so
            // its contrast is the chunk it is contrasted with, not a sibling.
            var hasContrast = level.Frames
                .Where(frames.ContainsKey)
                .Any(id => frames[id].Contrast is { } other && frames.ContainsKey(other));

            var steps = view.GetProperty("steps");
            steps.GetArrayLength().Should().Be(
                hasContrast ? 4 : 3,
                $"{level.Id} has {(hasContrast ? "" : "no ")}resolvable contrast partner");
        }
    }

    [Fact]
    public void Every_level_is_one_chunk_with_several_example_scenes()
    {
        foreach (var level in Content.Prepositions.Levels)
        {
            level.Frames.Should().HaveCountGreaterThanOrEqualTo(1);

            var frames = level.Frames.Select(id => Content.Prepositions.Frames
                .Single(frame => frame.Id == id)).ToList();

            frames.Select(frame => frame.Frame).Distinct().Should().HaveCount(1,
                $"{level.Id} holds one verb-preposition combination");
            frames.Select(frame => frame.Example.Nl).Distinct().Should().HaveCount(
                frames.Count, $"{level.Id} practises each example once");
        }
    }

    [Fact]
    public void A_contrast_partner_is_another_chunk_and_another_sentence()
    {
        var frames = Content.Prepositions.Frames.ToDictionary(f => f.Id);

        foreach (var frame in Content.Prepositions.Frames.Where(f => f.Contrast is not null))
        {
            frames.Should().ContainKey(frame.Contrast!);
            var partner = frames[frame.Contrast!];
            partner.Frame.Should().NotBe(frame.Frame, $"{frame.Id} contrasts two chunks");
            partner.Example.Nl.Should().NotBe(frame.Example.Nl);
        }
    }

    [Fact]
    public void The_choose_step_offers_three_pictures_from_the_level()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var round = service.Start(Body(new { level = "bang-voor" }));
        var view = Json(round.View);

        while (view.GetProperty("kind").GetString() != "choose")
            view = Json(service.Move(round.RoundId, Body(new { action = "next" })).View);

        var count = view.GetProperty("count").GetInt32();
        for (var item = 0; item < count; item++)
        {
            var options = view.GetProperty("content").GetProperty("options")
                .EnumerateArray().Select(option => option.GetProperty("id").GetString()).ToList();

            options.Should().HaveCount(3, "the picture grid is three columns wide");
            options.Should().OnlyHaveUniqueItems();

            view = Json(service.Move(round.RoundId,
                Body(new { action = "choose", scene = options[0] })).View);
            view = Json(service.Move(round.RoundId, Body(new { action = "next" })).View);
        }
    }

    [Fact]
    public void A_round_opens_on_the_discover_step()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var level = Content.Prepositions.Levels.First(l => l.Id == "wachten-op");

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
        var round = service.Start(Body(new { level = "wachten-op" }));

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
        // Which word opens it depends on the card's control question.
        view = Json(service.Move(
            round.RoundId, Body(new { action = "concept", answer = true })).View);
        var explanation = view.GetProperty("feedback").GetProperty("concept")
            .GetProperty("explanation").GetString();

        explanation.Should().MatchRegex("^(Ja|Nee)\\. ");

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

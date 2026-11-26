using System.Text.Json;
using FluentAssertions;
using Oefenpad.Services.Games;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// Scheidbare werkwoorden: discover every card, then pick each verb's English
/// meaning from four. The tests run against whatever separable.json holds, so
/// they read the answers from the content instead of naming verbs.
/// </summary>
public sealed class SeparableServiceTests
{
    private static readonly GameContent Content = new();

    private static JsonElement Body(object value) => JsonSerializer.SerializeToElement(value);

    private static JsonElement Json(object value) => JsonSerializer.SerializeToElement(value);

    private static SeparableService Service() => new(Content, new RoundStore());

    private static Level LargestLevel() =>
        Content.Separable.Levels.OrderByDescending(l => l.Frames.Count).First();

    private static SeparableFrame FrameFor(string verb) =>
        Content.Separable.Frames.First(f => f.Verb == verb);

    /// <summary>Walks through the discover step and returns the first choose view.</summary>
    private static (SeparableService Service, string RoundId, JsonElement View) AtChoose(Level level)
    {
        var service = Service();
        var round = service.Start(Body(new { level = level.Id }));
        var view = Json(round.View);

        for (var i = 0; i < level.Frames.Count; i++)
        {
            view.GetProperty("kind").GetString().Should().Be("discover");
            view = Json(service.Move(round.RoundId, Body(new { action = "next" })).View);
        }

        view.GetProperty("kind").GetString().Should().Be("choose");
        return (service, round.RoundId, view);
    }

    private static List<string> Options(JsonElement view) =>
        view.GetProperty("content").GetProperty("options").EnumerateArray()
            .Select(o => o.GetString()!).ToList();

    [Fact]
    public void Options_list_every_level_with_its_band()
    {
        var levels = Service().Options().Levels;

        levels.Select(l => l.Id).Should().Equal(Content.Separable.Levels.Select(l => l.Id));
        levels.Should().OnlyContain(l => !string.IsNullOrEmpty(l.Band));
        Service().Texts()["title"].Should().Be("Scheidbare werkwoorden");
    }

    [Fact]
    public void Discover_shows_the_split_form_the_perfect_and_the_example()
    {
        var level = LargestLevel();
        var service = Service();
        var view = Json(service.Start(Body(new { level = level.Id })).View);

        var card = view.GetProperty("content").GetProperty("card");
        var frame = FrameFor(card.GetProperty("verb").GetString()!);

        frame.Id.Should().Be(level.Frames[0]);
        card.GetProperty("split").GetString().Should().Be(frame.Split);
        card.GetProperty("perfect").GetString().Should().Be(frame.Perfect);
        card.GetProperty("example").GetString().Should().Be(frame.Example);
        card.GetProperty("exampleEn").GetString().Should().Be(frame.ExampleEn);
        card.GetProperty("gloss").GetString().Should().Be(frame.Gloss);

        // No drawing, no image object: the client then shows no empty box.
        if (frame.Scene is null)
            card.GetProperty("image").ValueKind.Should().Be(JsonValueKind.Null);
    }

    [Fact]
    public void Choosing_every_right_meaning_scores_the_whole_level()
    {
        var level = LargestLevel();
        var (service, roundId, view) = AtChoose(level);
        RoundMove? last = null;

        for (var i = 0; i < level.Frames.Count; i++)
        {
            var content = view.GetProperty("content");
            var frame = FrameFor(content.GetProperty("verb").GetString()!);
            content.GetProperty("example").GetString().Should().Be(frame.Example);

            var options = Options(view);
            options.Should().HaveCount(Math.Min(4, Content.Separable.Frames
                .Where(f => f.Band == frame.Band).Select(f => f.Gloss).Distinct().Count()));
            options.Should().OnlyHaveUniqueItems();
            options.Should().ContainSingle(o => o == frame.Gloss);

            var answer = Body(new { action = "choose", option = options.IndexOf(frame.Gloss) });
            var chosen = service.Move(roundId, answer);
            chosen.Correct.Should().BeTrue();
            chosen.Explanation.Should().Be($"Goed. {frame.Verb} — {frame.Gloss}.");

            last = service.Move(roundId, Body(new { action = "next" }));
            view = Json(last.View);
        }

        last!.Done.Should().BeTrue();
        last.CorrectCount.Should().Be(level.Frames.Count);
        last.Total.Should().Be(level.Frames.Count);
        service.LevelOf(roundId).Should().Be(level.Id);
    }

    [Fact]
    public void A_wrong_meaning_names_what_the_chosen_gloss_means()
    {
        var (service, roundId, view) = AtChoose(LargestLevel());
        var frame = FrameFor(view.GetProperty("content").GetProperty("verb").GetString()!);
        var options = Options(view);
        var wrong = options.FindIndex(o => o != frame.Gloss);

        var move = service.Move(roundId, Body(new { action = "choose", option = wrong }));

        move.Correct.Should().BeFalse();
        move.Explanation.Should().Be($"Nee. Dat betekent '{options[wrong]}'. {frame.Verb} — {frame.Gloss}.");
        var feedback = Json(move.View).GetProperty("feedback");
        feedback.GetProperty("chosenOption").GetInt32().Should().Be(wrong);
        feedback.GetProperty("correctOption").GetInt32().Should().Be(options.IndexOf(frame.Gloss));

        // Answered once is answered.
        var again = () => service.Move(roundId, Body(new { action = "choose", option = wrong }));
        again.Should().Throw<InvalidMoveException>();
    }

    [Fact]
    public void Moves_out_of_turn_are_refused()
    {
        var level = LargestLevel();
        var service = Service();
        var round = service.Start(Body(new { level = level.Id }));

        var early = () => service.Move(round.RoundId, Body(new { action = "choose", option = 0 }));
        early.Should().Throw<InvalidMoveException>();

        var (choosing, roundId, _) = AtChoose(level);
        var skip = () => choosing.Move(roundId, Body(new { action = "next" }));
        skip.Should().Throw<InvalidMoveException>();
        var outside = () => choosing.Move(roundId, Body(new { action = "choose", option = 9 }));
        outside.Should().Throw<InvalidMoveException>();

        var unknown = () => service.Start(Body(new { level = "nope" }));
        unknown.Should().Throw<InvalidMoveException>();
    }

    [Fact]
    public void Resume_shows_the_same_board()
    {
        var (service, roundId, view) = AtChoose(LargestLevel());

        var resumed = service.Resume(service.Export(roundId)!);

        Json(resumed.View).GetRawText().Should().Be(view.GetRawText());
    }

    /* ---------- distractors, against made-up frames ---------- */

    private static SeparableFrame F(string id, string gloss, string band = "a2") =>
        new() { Id = id, Verb = id, Gloss = gloss, Band = band };

    [Fact]
    public void Options_never_repeat_a_gloss()
    {
        var frame = F("aandoen", "to switch on");
        var level = new List<SeparableFrame>
        {
            frame,
            F("aanzetten", "to switch on"),   // same meaning as the answer
            F("uitdoen", "to switch off"),
            F("uitzetten", "To switch off "), // same as uitdoen, other spelling
            F("opstaan", "to get up")
        };
        var band = level.Concat(new[] { F("opbellen", "to phone"), F("meenemen", "to take along") });

        for (var run = 0; run < 50; run++)
        {
            var options = SeparableService.OptionFrames(frame, level, band);

            options.Should().HaveCount(4);
            options[0].Should().BeSameAs(frame);
            options.Select(o => o.Gloss.Trim().ToLowerInvariant()).Should().OnlyHaveUniqueItems();
            options.Should().NotContain(o => o.Id == "aanzetten");
        }
    }

    [Fact]
    public void A_level_with_fewer_than_four_frames_is_topped_up_from_its_band()
    {
        var frame = F("ophouden", "to stop", "b1");
        var level = new List<SeparableFrame> { frame, F("toegeven", "to admit", "b1") };
        var all = level.Concat(new[]
        {
            F("voorstellen", "to introduce", "b1"),
            F("afspreken", "to arrange", "b1"),
            F("aandoen", "to switch on", "a2"),
            F("uitdoen", "to switch off", "a2")
        }).ToList();

        var options = SeparableService.OptionFrames(frame, level, all);

        options.Should().HaveCount(4);
        options.Should().OnlyContain(o => o.Band == "b1", "a top-up stays in the band");
        options.Select(o => o.Id).Should().Contain("toegeven", "the level's own verbs come first");
        options.Select(o => o.Gloss).Should().OnlyHaveUniqueItems();
    }

    [Fact]
    public void A_band_too_small_for_four_gives_fewer_options_not_duplicates()
    {
        var frame = F("ophouden", "to stop", "b2");
        var level = new List<SeparableFrame> { frame, F("toegeven", "to admit", "b2") };

        var options = SeparableService.OptionFrames(frame, level, level);

        options.Select(o => o.Id).Should().BeEquivalentTo("ophouden", "toegeven");
    }
}

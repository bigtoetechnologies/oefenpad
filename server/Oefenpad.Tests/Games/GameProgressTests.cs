using System.Text.Json;
using FluentAssertions;
using Oefenpad.DB.Models;
using Oefenpad.DTOs;
using Oefenpad.DTOs.Games;
using Oefenpad.Services.Games;
using Oefenpad.Tests.Account;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// A signed-in player may leave in the middle of a round. These tests pin the
/// contract that makes that possible: each game exports its private state,
/// can rebuild it, and the rebuilt round is playable again.
/// </summary>
public sealed class GameResumeTests
{
    private static readonly GameContent Content = new();

    private static JsonElement Body(object value) => JsonSerializer.SerializeToElement(value);

    private static JsonElement Json(object value) => JsonSerializer.SerializeToElement(value);

    [Fact]
    public void Word_search_keeps_the_grid_and_the_found_words()
    {
        var service = new WordSearchService(Content, new RoundStore());
        var round = service.Start(Body(new { category = "animals", difficulty = "easy" }));
        var before = Json(round.View);

        // Ask for a hint, then select exactly the cells it points at.
        var hinted = Json(service.Move(round.RoundId, Body(new { action = "hint" })).View);
        var hint = hinted.GetProperty("hint");
        var index = hint.GetProperty("index").GetInt32();
        var cells = hint.GetProperty("cells").EnumerateArray().ToList();
        var first = cells[0];
        var last = cells[^1];

        service.Move(round.RoundId, Body(new
        {
            action = "select",
            r1 = first.GetProperty("r").GetInt32(),
            c1 = first.GetProperty("c").GetInt32(),
            r2 = last.GetProperty("r").GetInt32(),
            c2 = last.GetProperty("c").GetInt32()
        }));

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var after = Json(resumed.View);

        after.GetProperty("grid").GetRawText().Should().Be(before.GetProperty("grid").GetRawText());
        after.GetProperty("words").GetArrayLength().Should().Be(before.GetProperty("words").GetArrayLength());
        after.GetProperty("found")[index].GetBoolean().Should().BeTrue();
        after.GetProperty("hintsLeft").GetInt32().Should().Be(before.GetProperty("hintsLeft").GetInt32() - 1);

        // Only the found word's cells travel, never the whole placement table.
        var placements = Json(resumed.Resume!).GetProperty("placements");
        placements.EnumerateObject().Select(property => property.Name)
            .Should().Equal(index.ToString());

        // The rebuilt round is still playable.
        var hintAgain = service.Move(resumed.RoundId, Body(new { action = "hint" }));
        Json(hintAgain.View).TryGetProperty("hint", out _).Should().BeTrue();
    }

    [Fact]
    public void Hangman_keeps_the_guesses_and_the_status()
    {
        var service = new HangmanService(Content, new RoundStore());
        var round = service.Start(Body(new { category = "animals", difficulty = "medium" }));

        service.Move(round.RoundId, Body(new { action = "guess", letter = "E" }));

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var view = Json(resumed.View);

        view.GetProperty("guessed").EnumerateArray()
            .Select(letter => letter.GetString()).Should().Contain("E");
        view.GetProperty("pattern").GetArrayLength().Should().BeGreaterThan(0);

        var next = service.Move(resumed.RoundId, Body(new { action = "guess", letter = "Z" }));
        next.View.Should().NotBeNull();
    }

    [Fact]
    public void Memory_keeps_the_deck_and_the_open_card()
    {
        var service = new MemoryService(Content, new RoundStore());
        var round = service.Start(Body(new { category = "animals", level = "4" }));

        service.Move(round.RoundId, Body(new { action = "flip", index = 0 }));

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var view = Json(resumed.View);

        view.GetProperty("cards").GetArrayLength().Should().Be(16);
        view.GetProperty("cards")[0].GetProperty("faceUp").GetBoolean().Should().BeTrue();

        var next = service.Move(resumed.RoundId, Body(new { action = "flip", index = 1 }));
        next.View.Should().NotBeNull();
    }

    [Fact]
    public void Matching_keeps_the_deck_and_the_open_card()
    {
        var service = new MatchingService(Content, new RoundStore());
        var round = service.Start(Body(new { category = "animals", pairs = 4 }));

        service.Move(round.RoundId, Body(new { action = "flip", index = 0 }));

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var view = Json(resumed.View);

        view.GetProperty("cards").GetArrayLength().Should().Be(8);
        view.GetProperty("cards")[0].GetProperty("faceUp").GetBoolean().Should().BeTrue();

        var next = service.Move(resumed.RoundId, Body(new { action = "flip", index = 1 }));
        next.View.Should().NotBeNull();
    }

    [Fact]
    public void Story_machine_keeps_the_tiles_and_the_held_reels()
    {
        var service = new StoryMachineService(Content, new RoundStore());
        var round = service.Start(Body(new { count = 3, language = "nl" }));
        var before = Json(round.View);

        service.Move(round.RoundId, Body(new { action = "hold", index = 1, held = true }));

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var view = Json(resumed.View);

        view.GetProperty("count").GetInt32().Should().Be(3);
        view.GetProperty("language").GetString().Should().Be("nl");
        view.GetProperty("reels").GetArrayLength().Should().Be(3);
        view.GetProperty("reels")[1].GetProperty("held").GetBoolean().Should().BeTrue();

        var tileIds = view.GetProperty("reels").EnumerateArray()
            .Select(reel => reel.GetProperty("tile").GetProperty("id").GetString()).ToList();
        var beforeIds = before.GetProperty("reels").EnumerateArray()
            .Select(reel => reel.GetProperty("tile").GetProperty("id").GetString()).ToList();
        tileIds.Should().Equal(beforeIds);

        var spin = service.Move(resumed.RoundId, Body(new { action = "spin" }));
        spin.View.Should().NotBeNull();
    }

    [Fact]
    public void Prepositions_keeps_the_step_machine_and_the_feedback()
    {
        var service = new PrepositionsService(Content, new RoundStore());
        var level = Content.Prepositions.Levels[0];
        var round = service.Start(Body(new { level = level.Id }));

        // Walk past the discover cards to the first question.
        var view = Json(round.View);
        while (view.GetProperty("kind").GetString() == "discover")
            view = Json(service.Move(round.RoundId, Body(new { action = "next" })).View);

        var kind = view.GetProperty("kind").GetString();
        view.GetProperty("level").GetString().Should().Be(level.Id);

        RoundMove answered;
        if (kind == "choose")
        {
            var scene = view.GetProperty("content").GetProperty("options")[0].GetProperty("id").GetString();
            answered = service.Move(round.RoundId, Body(new { action = "choose", scene }));
        }
        else if (kind == "trueFalse")
        {
            answered = service.Move(round.RoundId, Body(new { action = "trueFalse", answer = true }));
        }
        else
        {
            // Build: send the item's tiles back in the target order.
            var tiles = view.GetProperty("content").GetProperty("tiles").EnumerateArray()
                .Select(tile => tile.GetProperty("id").GetString()).ToList();
            var ordered = tiles!.OrderBy(x => x, StringComparer.Ordinal).ToList();
            answered = service.Move(round.RoundId, Body(new { action = "build", tiles = ordered }));
        }

        var answeredView = Json(answered.View);
        answeredView.GetProperty("phase").GetString().Should().Be("feedback");

        var saved = service.Export(round.RoundId);
        saved.Should().NotBeNull();

        var resumed = service.Resume(saved!);
        var after = Json(resumed.View);

        after.GetProperty("phase").GetString().Should().Be("feedback");
        after.GetProperty("kind").GetString().Should().Be(answeredView.GetProperty("kind").GetString());
        after.GetProperty("stepIndex").GetInt32().Should().Be(answeredView.GetProperty("stepIndex").GetInt32());
        after.GetProperty("item").GetInt32().Should().Be(answeredView.GetProperty("item").GetInt32());
        after.GetProperty("total").GetInt32().Should().Be(answeredView.GetProperty("total").GetInt32());
        after.GetProperty("content").GetRawText().Should().Be(answeredView.GetProperty("content").GetRawText());

        service.LevelOf(resumed.RoundId).Should().Be(level.Id);

        var next = service.Move(resumed.RoundId, Body(new { action = "next" }));
        next.View.Should().NotBeNull();
    }
}

/// <summary>
/// The account side: a guest is ignored, a signed-in player's save survives a
/// reload, and a level never loses the best score it has seen.
/// </summary>
public sealed class GameProgressServiceTests : SqliteTestBase
{
    private async Task<GameProgressService> SignedInService()
    {
        var user = new ApplicationUser
        {
            UserName = "speler@example.nl",
            Email = "speler@example.nl",
            EmailConfirmed = true
        };

        (await UserManager.CreateAsync(user, "goedwachtwoord1")).Succeeded.Should().BeTrue();

        CurrentUser.IsAuthenticated = true;
        CurrentUser.UserId = user.Id;

        return new GameProgressService(ContextFactory, CurrentUser);
    }

    [Fact]
    public async Task A_guest_is_ignored()
    {
        var service = new GameProgressService(ContextFactory, CurrentUser);

        service.IsSignedIn.Should().BeFalse();
        (await service.LoadSavedAsync("wordsearch")).Should().BeNull();
        (await service.LoadLevelsAsync("prepositions")).Should().BeEmpty();

        // Writing must not throw for a guest; the games keep working without an account.
        await service.SaveStateAsync("wordsearch", "round", "{}");
        await service.RecordLevelAsync("prepositions", "level", 1, 1);
    }

    [Fact]
    public async Task A_save_replaces_the_previous_round_and_can_be_cleared()
    {
        var service = await SignedInService();

        service.IsSignedIn.Should().BeTrue();

        await service.SaveStateAsync("wordsearch", "round-1", "{\"round\":1}");
        (await service.LoadSavedAsync("wordsearch"))!.StateJson.Should().Be("{\"round\":1}");

        await service.SaveStateAsync("wordsearch", "round-2", "{\"round\":2}");
        var saved = await service.LoadSavedAsync("wordsearch");
        saved!.RoundId.Should().Be("round-2");
        saved.StateJson.Should().Be("{\"round\":2}");

        await service.ClearStateAsync("wordsearch");
        (await service.LoadSavedAsync("wordsearch")).Should().BeNull();
    }

    [Fact]
    public async Task A_level_keeps_the_best_score()
    {
        var service = await SignedInService();

        await service.RecordLevelAsync("prepositions", "wachten", 3, 5);
        await service.RecordLevelAsync("prepositions", "wachten", 2, 6);
        await service.RecordLevelAsync("prepositions", "wachten", 4, 5);

        var levels = await service.LoadLevelsAsync("prepositions");
        levels.Should().ContainKey("wachten");
        levels["wachten"].Should().Be(new LevelProgress(4, 5));
    }

    [Fact]
    public async Task Saves_are_scoped_to_the_signed_in_player()
    {
        var first = await SignedInService();
        await first.SaveStateAsync("hangman", "round", "{\"word\":\"kat\"}");

        var other = new FakeCurrentUser { IsAuthenticated = true, UserId = "another-user" };
        var second = new GameProgressService(ContextFactory, other);

        (await second.LoadSavedAsync("hangman")).Should().BeNull();
        (await first.LoadSavedAsync("hangman")).Should().NotBeNull();
    }
}

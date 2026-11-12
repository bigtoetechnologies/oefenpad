using FluentAssertions;
using Oefenpad.Services.Games;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// The three tiers of Voorzetselpaden and the level chain behind them: three
/// levels for everyone, six more for an account, the rest for a paid plan. The
/// rule is deliberately simple — finishing a level opens the next — so these
/// tests pin exactly where each gate falls.
/// </summary>
public sealed class GameAccessTests
{
    private static readonly List<Level> Levels =
    [
        new() { Id = "een" },
        new() { Id = "twee" },
        new() { Id = "drie" },
        new() { Id = "vier" },
        new() { Id = "vijf" },
        new() { Id = "zes" },
        new() { Id = "zeven" },
        new() { Id = "acht" },
        new() { Id = "negen" },
        new() { Id = "tien" },
        new() { Id = "elf" },
        new() { Id = "twaalf" }
    ];

    private static HashSet<string> Passed(params string[] ids) => [.. ids];

    [Fact]
    public void A_guest_reaches_the_three_free_levels_and_no_more()
    {
        var locks = PrepositionAccess.Evaluate(Levels, null, isSignedIn: false);

        locks.Should().NotContainKeys("een", "twee", "drie");
        locks.Should().HaveCount(Levels.Count - PrepositionAccess.FreeLevels);
        locks["vier"].Should().Be(GameLock.Account);
        locks["negen"].Should().Be(GameLock.Account);
        locks["tien"].Should().Be(GameLock.Premium);
        locks["twaalf"].Should().Be(GameLock.Premium);
    }

    [Fact]
    public void A_signed_in_learner_with_nothing_finished_is_gated_on_progress()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed(), isSignedIn: true);

        locks["vier"].Should().Be(GameLock.Progress);
        locks["negen"].Should().Be(GameLock.Progress);
        locks["tien"].Should().Be(GameLock.Premium);
    }

    [Fact]
    public void Finishing_a_level_opens_exactly_the_next_one()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed("drie"), isSignedIn: true);

        locks.Should().NotContainKey("vier");
        locks["vijf"].Should().Be(GameLock.Progress);
        locks["tien"].Should().Be(GameLock.Premium);
    }

    [Fact]
    public void A_finished_level_stays_playable_when_an_earlier_one_is_missing()
    {
        // Progress rows are per level, so a level can only be reached through
        // the chain. If a row exists out of order, it still opens itself; the
        // gap before it stays closed.
        var locks = PrepositionAccess.Evaluate(Levels, Passed("vijf"), isSignedIn: true);

        locks["vier"].Should().Be(GameLock.Progress);
        locks.Should().NotContainKey("zes");
        locks["zeven"].Should().Be(GameLock.Progress);
    }

    [Fact]
    public void A_paid_plan_opens_the_premium_slice_and_keeps_the_chain()
    {
        // The first nine levels finished, so the tenth opens. A plan does not
        // skip the chain: the eleventh still waits for the tenth.
        var passed = Passed("een", "twee", "drie", "vier", "vijf",
            "zes", "zeven", "acht", "negen");

        var locks = PrepositionAccess.Evaluate(Levels, passed, isSignedIn: true, isPremium: true);

        locks.Should().NotContainKey("tien");
        locks["elf"].Should().Be(GameLock.Progress);
        locks["twaalf"].Should().Be(GameLock.Progress);
    }

    [Fact]
    public void A_finished_premium_level_locks_again_without_a_plan()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed("tien"), isSignedIn: true);

        locks["tien"].Should().Be(GameLock.Premium);
    }

    [Fact]
    public void Annotating_marks_only_the_closed_levels()
    {
        var access = GameAccess.WithLocks(true, new Dictionary<string, string>
        {
            ["vier"] = GameLock.Progress,
            ["vijf"] = GameLock.Account,
            ["zes"] = GameLock.Premium
        });

        var options = new GameOptions(
            System.Array.Empty<GameCategory>(),
            Levels.Take(6).Select(level => new GameLevel(level.Id, level.Id, Subtitle: "2 beelden")).ToList());

        var annotated = access.Annotate(options);

        annotated.Levels.Take(3).Should().OnlyContain(level => !level.Locked && level.LockReason == null);
        annotated.Levels[3].LockReason.Should().Be(GameLock.Progress);
        annotated.Levels[4].LockReason.Should().Be(GameLock.Account);
        annotated.Levels[5].LockReason.Should().Be(GameLock.Premium);
        annotated.Levels.Should().OnlyContain(level => level.Subtitle == "2 beelden");
    }

    [Fact]
    public void A_game_without_a_policy_is_left_open()
    {
        var access = GameAccess.Open(false);
        var options = new GameOptions(
            System.Array.Empty<GameCategory>(),
            [new GameLevel("beginner", "Beginner")]);

        access.Annotate(options).Levels.Should().OnlyContain(level => !level.Locked);
    }
}

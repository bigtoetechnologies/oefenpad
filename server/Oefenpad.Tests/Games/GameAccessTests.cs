using FluentAssertions;
using Oefenpad.Services.Games;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// The three tiers of Voorzetselpaden and the level chain behind them: A0 for
/// everyone, A1, A2 and the A2 pairs for an account, B1 and up for a paid plan. The tier is read off
/// the band, so adding a band cannot silently move the cut. The rule inside a
/// tier is deliberately simple — a band starts at its first level and finishing
/// a level opens the next — so these tests pin exactly where each gate falls.
/// </summary>
public sealed class GameAccessTests
{
    private static readonly List<Level> Levels =
    [
        new() { Id = "een", Band = "a0" },
        new() { Id = "twee", Band = "a0" },
        new() { Id = "drie", Band = "a0" },
        new() { Id = "vier", Band = "a1" },
        new() { Id = "vijf", Band = "a1" },
        new() { Id = "zes", Band = "a1" },
        new() { Id = "zeven", Band = "a1" },
        new() { Id = "acht", Band = "b1" },
        new() { Id = "negen", Band = "b1" }
    ];

    private static HashSet<string> Passed(params string[] ids) => [.. ids];

    [Fact]
    public void The_band_decides_the_tier()
    {
        PrepositionAccess.TierOf(new Level { Band = "a0" }).Should().Be(PrepositionAccess.Tier.Free);
        PrepositionAccess.TierOf(new Level { Band = "A1" }).Should().Be(PrepositionAccess.Tier.Account);
        PrepositionAccess.TierOf(new Level { Band = "a2" }).Should().Be(PrepositionAccess.Tier.Account);
        PrepositionAccess.TierOf(new Level { Band = "a2-pairs" }).Should().Be(PrepositionAccess.Tier.Account);
        PrepositionAccess.TierOf(new Level { Band = "b1" }).Should().Be(PrepositionAccess.Tier.Premium);
        PrepositionAccess.TierOf(new Level { Band = "b2" }).Should().Be(PrepositionAccess.Tier.Premium);

        // An unlabelled level stays free: a new band must not arrive shut.
        PrepositionAccess.TierOf(new Level()).Should().Be(PrepositionAccess.Tier.Free);
        PrepositionAccess.TierOf(new Level { Band = "" }).Should().Be(PrepositionAccess.Tier.Free);
    }

    [Fact]
    public void A_guest_reaches_the_whole_a0_band_and_no_more()
    {
        var locks = PrepositionAccess.Evaluate(Levels, null, isSignedIn: false);

        locks.Should().NotContainKeys("een", "twee", "drie");
        locks["vier"].Should().Be(GameLock.Account);
        locks["zeven"].Should().Be(GameLock.Account);
        locks["acht"].Should().Be(GameLock.Premium);
        locks["negen"].Should().Be(GameLock.Premium);
    }

    [Fact]
    public void An_account_opens_each_band_at_its_first_level()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed(), isSignedIn: true);

        // Nothing finished, so A1 opens where it starts and stops there.
        locks.Should().NotContainKey("vier");
        locks["vijf"].Should().Be(GameLock.Progress);
        locks["zeven"].Should().Be(GameLock.Progress);
    }

    [Fact]
    public void Finishing_a_level_opens_exactly_the_next_one()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed("vier"), isSignedIn: true);

        locks.Should().NotContainKey("vijf");
        locks["zes"].Should().Be(GameLock.Progress);
    }

    [Fact]
    public void A_finished_level_stays_playable_when_an_earlier_one_is_missing()
    {
        // Progress rows are per level, so a level can only be reached through
        // the chain. If a row exists out of order, it still opens itself; the
        // gap before it stays closed.
        var locks = PrepositionAccess.Evaluate(Levels, Passed("zes"), isSignedIn: true);

        locks["vijf"].Should().Be(GameLock.Progress);
        locks.Should().NotContainKeys("zes", "zeven");
    }

    [Fact]
    public void A_paid_plan_opens_the_premium_band_and_keeps_the_chain()
    {
        // A0 and A1 finished, so B1 opens at the plan boundary. A plan does not
        // skip the chain: the second B1 level still waits for the first.
        var passed = Passed("een", "twee", "drie", "vier", "vijf", "zes", "zeven");

        var locks = PrepositionAccess.Evaluate(Levels, passed, isSignedIn: true, isPremium: true);

        locks.Should().NotContainKey("acht");
        locks["negen"].Should().Be(GameLock.Progress);
    }

    [Fact]
    public void A_finished_premium_level_locks_again_without_a_plan()
    {
        var locks = PrepositionAccess.Evaluate(Levels, Passed("acht"), isSignedIn: true);

        locks["acht"].Should().Be(GameLock.Premium);
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

using System.Text.Json;
using FluentAssertions;
using Oefenpad.Services.Games;
using Xunit;

namespace Oefenpad.Tests.Games;

/// <summary>
/// The text-only categories of words.cards.json in the four word games. The
/// tests read the answers from the content, so a regenerated card file still
/// passes as long as its shape holds.
/// </summary>
public sealed class CardCategoryGameTests
{
    private static readonly GameContent Content = new();

    private static JsonElement Json(object value) => JsonSerializer.SerializeToElement(value);

    private static List<string> TextKeys() =>
        Content.Categories.Where(x => x.Value.TextOnly).Select(x => x.Key).ToList();

    /// <summary>The text category with the fewest pairs.</summary>
    private static string SmallestTextCategory() =>
        TextKeys().OrderBy(k => Content.TextPairs(k).Count).First();

    private static string LargestTextCategory() =>
        TextKeys().OrderByDescending(k => Content.TextPairs(k).Count).First();

    [Fact]
    public void Card_categories_are_text_only_and_add_no_pictures()
    {
        TextKeys().Should().NotBeEmpty();
        Content.ImageItems.Should().OnlyContain(item => !Content.IsTextOnly(item.Category));

        foreach (var key in TextKeys())
            Content.Categories[key].Words.Should().OnlyContain(w => Content.ImageFor(w) == null);
    }

    /* ---------- memory ---------- */

    [Fact]
    public void Memory_lists_text_categories_by_pair_count()
    {
        var options = new MemoryService(Content, new RoundStore()).Options();

        foreach (var key in TextKeys())
        {
            var pairs = Content.TextPairs(key).Count;
            var listed = options.Categories.SingleOrDefault(c => c.Id == key);
            if (pairs < 8)
            {
                listed.Should().BeNull($"{key} cannot fill the smallest board");
                continue;
            }

            listed.Should().NotBeNull();
            listed!.Count.Should().Be(pairs);
            listed.Name.Should().Be(Content.Categories[key].Label["nl"]);
            listed.Icon.Should().Be(Content.Categories[key].Icon);
        }
    }

    [Fact]
    public void Memory_refuses_a_board_the_text_category_cannot_fill()
    {
        var key = SmallestTextCategory();
        var pairs = Content.TextPairs(key).Count;
        var service = new MemoryService(Content, new RoundStore());

        // The listed count is what the client compares each board with.
        var tooBig = service.Options().Levels.First(l => l.Size > pairs);
        service.Options().Categories.Single(c => c.Id == key).Count.Should().BeLessThan(tooBig.Size!.Value);

        var start = () => service.Start(Json(new { category = key, level = tooBig.Id }));
        start.Should().Throw<InvalidMoveException>();
    }

    [Theory]
    [InlineData("4", 8)]
    [InlineData("10", 50)]
    public void Memory_text_round_pairs_each_Dutch_word_with_its_meaning(string level, int pairs)
    {
        var key = LargestTextCategory();
        var meaning = Content.TextPairs(key).ToDictionary(p => p.Dutch, p => p.English);
        var service = new MemoryService(Content, new RoundStore());

        var round = service.Start(Json(new { category = key, level }));
        var view = Json(round.View);
        view.GetProperty("text").GetBoolean().Should().BeTrue();
        view.GetProperty("pairs").GetInt32().Should().Be(pairs);
        var count = view.GetProperty("cards").GetArrayLength();
        count.Should().Be(pairs * 2);

        // Turn the cards two at a time to read every face.
        var faces = new Dictionary<int, (string Kind, string Word)>();
        for (var i = 0; i < count; i++)
        {
            var moved = Json(service.Move(round.RoundId, Json(new { action = "flip", index = i })).View);
            var face = moved.GetProperty("cards")[i].GetProperty("face");
            face.GetProperty("imageUrl").ValueKind.Should().Be(JsonValueKind.Null);
            faces[i] = (face.GetProperty("kind").GetString()!, face.GetProperty("word").GetString()!);
        }

        var words = faces.Where(f => f.Value.Kind == "word").ToList();
        var meanings = faces.Where(f => f.Value.Kind == "meaning").ToList();
        words.Should().HaveCount(pairs);
        meanings.Should().HaveCount(pairs);
        words.Select(f => f.Value.Word).Should().OnlyHaveUniqueItems();
        meanings.Select(f => f.Value.Word).Should().OnlyHaveUniqueItems();

        // Play the deal out; pairs the reading pass matched by chance are skipped.
        RoundMove? last = null;
        foreach (var (index, (_, word)) in words)
        {
            var partner = meanings.Single(m => m.Value.Word == meaning[word]).Key;
            var state = Json(service.Move(round.RoundId, Json(new { action = "flip", index })).View);
            if (state.GetProperty("cards")[index].GetProperty("matched").GetBoolean()) continue;

            last = service.Move(round.RoundId, Json(new { action = "flip", index = partner }));
            last.Correct.Should().BeTrue();
        }

        Json(service.Move(round.RoundId, Json(new { action = "flip", index = 0 })).View)
            .GetProperty("pairsFound").GetInt32().Should().Be(pairs);
    }

    /* ---------- matching ---------- */

    [Fact]
    public void Matching_text_round_has_unique_words_and_meanings()
    {
        var service = new MatchingService(Content, new RoundStore());
        var options = service.Options();

        foreach (var key in TextKeys())
        {
            var pool = Content.TextPairs(key, 24);
            options.Categories.Single(c => c.Id == key).Count.Should().Be(pool.Count);

            var round = service.Start(Json(new { category = key, pairs = 12 }));
            var view = Json(round.View);
            view.GetProperty("text").GetBoolean().Should().BeTrue();
            view.GetProperty("pairs").GetInt32().Should().Be(Math.Min(12, pool.Count));

            var cards = view.GetProperty("cards").EnumerateArray().ToList();
            var left = cards.Where(c => c.GetProperty("side").GetString() == "word")
                .Select(c => c.GetProperty("index").GetInt32()).ToList();
            var right = cards.Where(c => c.GetProperty("side").GetString() == "image")
                .Select(c => c.GetProperty("index").GetInt32()).ToList();
            left.Should().HaveCount(right.Count);

            // Turn one card from each panel at a time to read every face.
            var faces = new List<(string Side, string Kind, string Word)>();
            for (var k = 0; k < left.Count; k++)
            {
                foreach (var i in new[] { left[k], right[k] })
                {
                    var moved = Json(service.Move(round.RoundId, Json(new { action = "flip", index = i })).View);
                    var card = moved.GetProperty("cards")[i];
                    var face = card.GetProperty("face");
                    face.GetProperty("imageUrl").ValueKind.Should().Be(JsonValueKind.Null);
                    faces.Add((card.GetProperty("side").GetString()!, face.GetProperty("kind").GetString()!,
                        face.GetProperty("word").GetString()!));
                }
            }

            var dutch = faces.Where(f => f.Side == "word").Select(f => f.Word).ToList();
            var english = faces.Where(f => f.Side == "image").Select(f => f.Word).ToList();
            dutch.Should().OnlyHaveUniqueItems();
            english.Should().OnlyHaveUniqueItems();
            faces.Where(f => f.Side == "word").Should().OnlyContain(f => f.Kind == "word");
            faces.Where(f => f.Side == "image").Should().OnlyContain(f => f.Kind == "meaning");
            dutch.Should().OnlyContain(w => w.Length <= 24);
            dutch.Should().OnlyContain(w => pool.Any(p => p.Dutch == w));
            english.Should().OnlyContain(w => pool.Any(p => p.English == w));
        }
    }

    [Fact]
    public void Matching_text_round_can_be_won()
    {
        var key = SmallestTextCategory();
        var meaning = Content.TextPairs(key, 24).ToDictionary(p => p.Dutch, p => p.English);
        var service = new MatchingService(Content, new RoundStore());
        var round = service.Start(Json(new { category = key, pairs = 4 }));
        var cards = Json(round.View).GetProperty("cards");

        // Read every face: a word card, then each meaning card against it.
        var words = new List<int>();
        var meanings = new List<int>();
        for (var i = 0; i < cards.GetArrayLength(); i++)
            (cards[i].GetProperty("side").GetString() == "word" ? words : meanings).Add(i);

        var found = 0;
        foreach (var w in words)
        {
            foreach (var m in meanings)
            {
                var first = Json(service.Move(round.RoundId, Json(new { action = "flip", index = w })).View);
                var dutch = first.GetProperty("cards")[w].GetProperty("face").GetProperty("word").GetString()!;
                var result = service.Move(round.RoundId, Json(new { action = "flip", index = m }));
                var english = Json(result.View).GetProperty("cards")[m].GetProperty("face").GetProperty("word").GetString();

                result.Correct.Should().Be(meaning[dutch] == english);
                if (result.Correct == true)
                {
                    found++;
                    meanings.Remove(m);
                    break;
                }
            }
        }

        found.Should().Be(4);
    }

    [Fact]
    public void Matching_image_categories_are_unchanged()
    {
        var view = Json(new MatchingService(Content, new RoundStore())
            .Start(Json(new { category = "animals", pairs = 4 })).View);
        view.GetProperty("text").GetBoolean().Should().BeFalse();
    }

    /* ---------- hangman and word search ---------- */

    [Fact]
    public void Hangman_plays_a_card_category_with_the_English_meaning()
    {
        var service = new HangmanService(Content, new RoundStore());
        foreach (var key in TextKeys())
            service.Options().Categories.Should().Contain(c => c.Id == key && c.Name == Content.CategoryName(key));

        foreach (var key in new[] { LargestTextCategory(), TextKeys().First(k => k.StartsWith("expressions")) })
        {
            var round = service.Start(Json(new { category = key, difficulty = "hard", translateTo = "en" }));
            var view = Json(round.View);
            view.GetProperty("clueImageUrl").ValueKind.Should().Be(JsonValueKind.Null);

            var english = view.GetProperty("translation").GetString()!;
            var entry = Content.Categories[key].Words.First(w => w.En == english);
            var pattern = view.GetProperty("pattern");
            pattern.GetArrayLength().Should().Be(entry.Nl!.Length);
            for (var i = 0; i < entry.Nl.Length; i++)
                pattern[i].GetProperty("gap").GetBoolean().Should().Be(entry.Nl[i] == ' ');

            RoundMove? last = null;
            foreach (var letter in entry.Nl.Where(char.IsLetter).Distinct())
                last = service.Move(round.RoundId, Json(new { action = "guess", letter = letter.ToString() }));

            last!.Done.Should().BeTrue();
            Json(last.View).GetProperty("status").GetString().Should().Be("won");
            Json(last.View).GetProperty("answer").GetString().Should().Be(entry.Nl);
        }
    }

    [Fact]
    public void Word_search_plays_a_card_category()
    {
        var service = new WordSearchService(Content, new RoundStore());
        var key = TextKeys().First(k => k.StartsWith("separable"));
        service.Options().Categories.Should().Contain(c => c.Id == key);
        service.Options().Categories.Should().NotContain(c => c.Id.StartsWith("expressions"),
            "expressions have no single words");

        var view = Json(service.Start(Json(new { category = key, difficulty = "hard" })).View);
        view.GetProperty("category").GetProperty("id").GetString().Should().Be(key);

        var dutch = Content.Categories[key].Words.Select(w => w.Nl).ToHashSet();
        var words = view.GetProperty("words").EnumerateArray().ToList();
        words.Should().NotBeEmpty();
        words.Should().OnlyContain(w => dutch.Contains(w.GetProperty("text").GetString()));
        words.Should().OnlyContain(w => w.GetProperty("imageUrl").ValueKind == JsonValueKind.Null);
    }

    [Fact]
    public void Word_search_refuses_a_level_the_category_cannot_fill_instead_of_switching()
    {
        // Separable verbs are long; the beginner level takes words of 3 to 5 letters.
        var key = TextKeys().First(k => k.StartsWith("separable"));
        Content.Categories[key].Words.Count(w => w.Nl!.Length <= 5).Should().BeLessThan(3);

        var start = () => new WordSearchService(Content, new RoundStore())
            .Start(Json(new { category = key, difficulty = "beginner" }));
        start.Should().Throw<InvalidMoveException>().WithMessage("*te weinig woorden*");
    }
}

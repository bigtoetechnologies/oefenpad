using System.Text.Json;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Services.Games;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Api;

/// <summary>
/// The game API. One shape for every game: the browser asks for a round, is
/// given only the view of that round, and posts actions back. Word banks,
/// solutions and distractors stay on this side.
///
/// A signed-in player's live round is copied to the account after every
/// answer, and the finished level is recorded when a round ends. A guest
/// follows the same path; the progress service is simply a no-op for them.
///
/// Access is decided per request by <see cref="GameAccessService"/>: `/options`
/// marks a locked level, and starting one here answers 403. The round endpoint
/// is the check that matters, because a caller can skip `/options` entirely.
/// </summary>
public static class GamesApi
{
    public static IEndpointRouteBuilder MapGamesApi(this IEndpointRouteBuilder app)
    {
        var games = app.MapGroup("/api/games")
            .RequireRateLimiting(RateLimitPolicies.Games);

        games.MapGet("/", (GameRegistry registry) => Results.Ok(new
        {
            games = registry.Games
        }));

        games.MapGet("/{game}/texts", (string game, GameRegistry registry) =>
            registry.For(game) is { } service
                ? Results.Ok(service.Texts())
                : Results.NotFound(new { error = "Onbekend spel." }));

        games.MapGet("/{game}/options", async (
            string game,
            GameRegistry registry,
            GameAccessService access,
            CancellationToken cancellationToken) =>
        {
            if (registry.For(game) is not { } service)
                return Results.NotFound(new { error = "Onbekend spel." });

            var rules = await access.ForAsync(service.Game, cancellationToken);
            return Results.Ok(rules.Annotate(service.Options()));
        });

        // The player's saved round, ready to render. A guest, or an account
        // with nothing saved, gets { saved: false } so the browser can start
        // a fresh round without treating it as an error.
        games.MapGet("/{game}/saved", async (
            string game,
            GameRegistry registry,
            RoundStore rounds,
            IGameProgressService progress) =>
        {
            if (registry.For(game) is not { } service)
                return Results.NotFound(new { error = "Onbekend spel." });

            if (!progress.IsSignedIn)
                return Results.Ok(new { saved = false });

            var save = await progress.LoadSavedAsync(service.Game);
            if (save is null)
                return Results.Ok(new { saved = false });

            try
            {
                var round = service.Resume(save.StateJson);

                // Resume always mints a fresh id. When the round it was written
                // from is still live — a reload, or a second tab — keep the
                // browser on that id and drop the copy, instead of leaking one
                // slot per resume for the full three-hour lifetime. Removing
                // the original instead would 410 a tab still playing it.
                var roundId = round.RoundId;
                if (rounds.Get(save.RoundId, service.Game) is not null)
                {
                    rounds.Remove(round.RoundId);
                    roundId = save.RoundId;
                }

                return Results.Ok(new
                {
                    saved = true,
                    roundId,
                    view = round.View,
                    resume = round.Resume
                });
            }
            catch (Exception ex) when (
                ex is JsonException or RoundExpiredException or InvalidOperationException
                    or ArgumentException or NotSupportedException)
            {
                // A save the game can no longer rebuild is worthless. Drop it
                // and let the player start fresh rather than break the page.
                await progress.ClearStateAsync(service.Game);
                return Results.Ok(new { saved = false });
            }
        });

        // Finished levels with the best score reached on each. Empty for a guest.
        games.MapGet("/{game}/progress", async (
            string game,
            GameRegistry registry,
            IGameProgressService progress) =>
        {
            if (registry.For(game) is not { } service)
                return Results.NotFound(new { error = "Onbekend spel." });

            var levels = await progress.LoadLevelsAsync(service.Game);
            return Results.Ok(new { levels });
        });

        games.MapPost("/{game}/rounds", async (
            string game,
            HttpRequest request,
            GameRegistry registry,
            GameAccessService access,
            IGameProgressService progress) =>
        {
            if (registry.For(game) is not { } service)
                return Results.NotFound(new { error = "Onbekend spel." });

            if (await ReadAsync(request) is not { } input) return BadBody();

            // The level list hides a locked level; this is the check that holds
            // when the request did not come from that list.
            var rules = await access.ForAsync(service.Game, request.HttpContext.RequestAborted);
            if (rules.ReasonFor(LevelId(input)) is { } lockReason)
                return Results.Json(
                    new { error = GameLock.Message(lockReason) },
                    statusCode: StatusCodes.Status403Forbidden);

            try
            {
                var round = service.Start(input);
                await RememberAsync(progress, service, round.RoundId);
                return Results.Ok(round);
            }
            catch (RoundExpiredException)
            {
                return Gone();
            }
            catch (InvalidMoveException ex)
            {
                return Results.BadRequest(new { error = ex.Message });
            }
        });

        games.MapPost("/{game}/rounds/{roundId}/moves", async (
            string game,
            string roundId,
            HttpRequest request,
            GameRegistry registry,
            RoundStore rounds,
            IGameProgressService progress) =>
        {
            if (registry.For(game) is not { } service)
                return Results.NotFound(new { error = "Onbekend spel." });

            if (await ReadAsync(request) is not { } move) return BadBody();

            // One round, one mover at a time: the state is a shared mutable object
            // and every game's Move is check-then-act on it.
            var gate = rounds.Gate(roundId);
            if (gate is not null) await gate.WaitAsync(request.HttpContext.RequestAborted);

            try
            {
                var result = service.Move(roundId, move);

                if (result.Done)
                {
                    // The level is read before the round is forgotten: only a
                    // level round has one, and it ends here.
                    if (service.LevelOf(roundId) is { } level)
                    {
                        await progress.RecordLevelAsync(
                            service.Game,
                            level,
                            result.CorrectCount ?? 0,
                            result.Total ?? 0);
                    }

                    await progress.ClearStateAsync(service.Game);
                }
                else if (result.Rejection is null)
                {
                    await RememberAsync(progress, service, roundId);
                }

                return Results.Ok(result);
            }
            catch (RoundExpiredException)
            {
                return Gone();
            }
            catch (InvalidMoveException ex)
            {
                return Results.BadRequest(new { error = ex.Message });
            }
            finally
            {
                gate?.Release();
            }
        });

        return app;
    }

    private static async Task RememberAsync(
        IGameProgressService progress,
        IGameService service,
        string roundId)
    {
        if (!progress.IsSignedIn) return;
        if (service.Export(roundId) is { } json)
            await progress.SaveStateAsync(service.Game, roundId, json);
    }

    /// <summary>
    /// The level a start request names, if any. Only Voorzetselpaden starts by
    /// level; the other games take a difficulty or a category and have no gate.
    /// </summary>
    private static string? LevelId(JsonElement input) =>
        input.ValueKind == JsonValueKind.Object
        && input.TryGetProperty("level", out var level)
        && level.ValueKind == JsonValueKind.String
            ? level.GetString()
            : null;

    /// <summary>
    /// The request body, or null when it was present but unparseable. An empty
    /// body is a legitimate "use the defaults" and comes back as an undefined
    /// element; a truncated one must not quietly become that, or a round starts
    /// on settings the player never chose.
    /// </summary>
    private static async Task<JsonElement?> ReadAsync(HttpRequest request)
    {
        if (request.ContentLength == 0) return default(JsonElement);

        try
        {
            using var document = await JsonDocument.ParseAsync(request.Body);
            return document.RootElement.Clone();
        }
        catch (JsonException)
        {
            return null;
        }
    }

    private static IResult BadBody() =>
        Results.BadRequest(new { error = "Ongeldige aanvraag." });

    // 410: the round is gone (expired or never existed).
    private static IResult Gone() =>
        Results.Json(new { error = "Deze ronde bestaat niet meer." },
            statusCode: StatusCodes.Status410Gone);
}

using System.Security.Cryptography;
using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB;
using Oefenpad.DB.Models;
using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Services;

/// <summary>
/// Two-step deletion: a password proves the request is the account holder's, and following
/// the emailed link proves the mailbox is still theirs. Only the token's hash is stored.
/// </summary>
public class AccountDeletionService(
    UserManager<ApplicationUser> userManager,
    IOefenpadContextFactory contextFactory,
    IEmailDispatcher emailDispatcher,
    IAppUrlProvider appUrlProvider,
    ICurrentUserService currentUser,
    ILogger<AccountDeletionService> logger) : IAccountDeletionService
{
    private static readonly TimeSpan TokenLifetime = TimeSpan.FromHours(1);

    public async Task<Result<bool>> RequestDeletionAsync(
        DeleteAccountRequest request,
        CancellationToken cancellationToken = default)
    {
        if (!currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(currentUser.UserId))
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        var user = await userManager.FindByIdAsync(currentUser.UserId);
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        if (!await userManager.CheckPasswordAsync(user, request.Password))
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.WachtwoordFout);

        var rawToken = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32))
            .Replace('+', '-').Replace('/', '_').TrimEnd('=');
        var tokenHash = Hash(rawToken);

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);

        // A new request replaces any earlier link, so only the last email works.
        var previous = await context.AccountDeletionTokens
            .Where(t => t.ApplicationUserId == user.Id)
            .ToListAsync(cancellationToken);
        context.AccountDeletionTokens.RemoveRange(previous);

        var now = DateTime.UtcNow;
        context.AccountDeletionTokens.Add(new AccountDeletionToken
        {
            TokenHash = tokenHash,
            ApplicationUserId = user.Id,
            CreatedAt = now,
            ExpiresAt = now.Add(TokenLifetime)
        });

        await context.SaveChangesAsync(cancellationToken);

        try
        {
            var link = appUrlProvider.ToAbsoluteUrl(
                $"/Account/Verwijderen/Bevestig?token={Uri.EscapeDataString(rawToken)}");

            var name = await FirstNameAsync(user.Id, cancellationToken);
            var content = AccountEmails.AccountVerwijderen(name, link, Language(user));

            await emailDispatcher.SendAsync(
                new EmailMessage(user.Email!, Bilingual.Same(content.Subject), content.Html),
                cancellationToken);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Could not send account-deletion email for {UserId}.", user.Id);
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.Mislukt);
        }

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ConfirmDeletionAsync(
        string token,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(token))
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.TokenOngeldig);

        var tokenHash = Hash(token);

        await using var lookup = await contextFactory.CreateContextAsync(cancellationToken);
        var row = await lookup.AccountDeletionTokens
            .AsNoTracking()
            .FirstOrDefaultAsync(t => t.TokenHash == tokenHash, cancellationToken);

        if (row is null || row.ExpiresAt < DateTime.UtcNow)
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.TokenOngeldig);

        var user = await userManager.FindByIdAsync(row.ApplicationUserId);
        if (user is null)
        {
            await using var cleanup = await contextFactory.CreateContextAsync(cancellationToken);
            await cleanup.AccountDeletionTokens
                .Where(t => t.TokenHash == tokenHash)
                .ExecuteDeleteAsync(cancellationToken);
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.TokenOngeldig);
        }

        // The two rows live in two contexts, so there is no shared transaction. Delete
        // the login first: if that fails, nothing has been lost and the learner can try
        // again. Dropping the profile first and then failing here would leave an account
        // that still signs in but has no profile, and nothing recreates one.
        // The FK is SetNull, so note the profile's own id before the cascade clears it.
        int? personId;
        await using (var context = await contextFactory.CreateContextAsync(cancellationToken))
        {
            personId = await context.Persons
                .AsNoTracking()
                .Where(p => p.ApplicationUserId == user.Id)
                .Select(p => (int?)p.Id)
                .FirstOrDefaultAsync(cancellationToken);
        }

        var deleted = await userManager.DeleteAsync(user);
        if (!deleted.Succeeded)
        {
            logger.LogError("Could not delete account {UserId}: {Errors}", user.Id,
                string.Join(", ", deleted.Errors.Select(e => e.Code)));
            return ResultHelpers.Fout<bool>(AccountMessages.Verwijderen.Mislukt);
        }

        if (personId is { } id)
        {
            await using var context = await contextFactory.CreateContextAsync(cancellationToken);
            await context.Persons
                .Where(p => p.Id == id)
                .ExecuteDeleteAsync(cancellationToken);
        }

        logger.LogInformation("Account {UserId} deleted at its owner's request.", user.Id);
        return Result<bool>.Success(true);
    }

    private async Task<string> FirstNameAsync(string userId, CancellationToken cancellationToken)
    {
        await using var context = await contextFactory.CreateContextAsync(cancellationToken);
        return await context.Persons
            .AsNoTracking()
            .Where(p => p.ApplicationUserId == userId)
            .Select(p => p.FirstName)
            .FirstOrDefaultAsync(cancellationToken) ?? string.Empty;
    }

    private static string Hash(string token)
        => Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(token)));

    private static string Language(ApplicationUser user) => user.PreferredLanguageCode == "en" ? "en" : "nl";
}

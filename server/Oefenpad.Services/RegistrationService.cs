using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB;
using Oefenpad.DB.Models;
using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;
using Oefenpad.Enums;
using Oefenpad.Resources.Account;

namespace Oefenpad.Services;

public class RegistrationService(
    UserManager<ApplicationUser> userManager,
    IOefenpadContextFactory contextFactory,
    IEmailDispatcher emailDispatcher,
    IAppUrlProvider appUrlProvider,
    ILogger<RegistrationService> logger) : IRegistrationService
{
    public async Task<Result<RegistrationResult>> RegisterAsync(
        RegisterRequest request,
        CancellationToken cancellationToken = default)
    {
        var email = request.Email.Trim();
        var language = NormaliseLanguage(request.PreferredLanguageCode);

        // Registration answers the same whether or not the address already has an
        // account, the way resend and password reset already do. Otherwise the form
        // is an oracle for who uses the site. The holder is told by email instead.
        if (await userManager.FindByEmailAsync(email) is { } existing)
        {
            logger.LogInformation(
                "Registration for {Email} matched an existing account; neutral answer.", email);
            return await ExistingAccountAsync(existing, language, cancellationToken);
        }

        var user = new ApplicationUser
        {
            UserName = email,
            Email = email,
            PreferredLanguageCode = language
        };

        // Identity enforces unique address and password rules; a duplicate comes back as a
        // failure message, never as an exception.
        var create = await userManager.CreateAsync(user, request.Password);
        if (!create.Succeeded)
        {
            logger.LogWarning("Registration rejected for {Email}: {Errors}", email,
                string.Join(", ", create.Errors.Select(e => e.Code)));

            var failure = new Result<RegistrationResult>();
            failure.Messages.AddRange(IdentityErrorTranslator.ToMessages(create));
            return failure;
        }

        try
        {
            await using var context = await contextFactory.CreateContextAsync(cancellationToken);
            context.Persons.Add(new Person
            {
                ApplicationUserId = user.Id,
                FirstName = request.FirstName.Trim(),
                LastName = request.LastName.Trim()
            });
            await context.SaveChangesAsync(cancellationToken);
        }
        catch (Exception ex)
        {
            // The Identity user is already committed. Remove it so the address is free and a
            // retry does not meet a half-made account.
            logger.LogError(ex, "Creating Person failed for user {UserId} ({Email}); rolling the user back.",
                user.Id, email);

            await userManager.DeleteAsync(user);
            return ResultHelpers.Fout<RegistrationResult>(AccountMessages.Registratie.Mislukt);
        }

        var (sent, confirmationUrl) = await TrySendConfirmationAsync(
            user, request.FirstName.Trim(), language, cancellationToken);

        var result = Result<RegistrationResult>.Success(new RegistrationResult
        {
            UserId = user.Id,
            Email = email,
            ConfirmationUrl = confirmationUrl
        });

        if (!sent)
            result.Messages.Add(new ResultMessage(MessageSeverity.Warning, AccountMessages.Registratie.EmailNietVerzonden));

        logger.LogInformation("User {Email} registered; confirmation email {State}.",
            email, sent ? "sent" : "failed");

        return result;
    }

    public async Task<Result<bool>> ConfirmEmailAsync(
        string userId,
        string code,
        CancellationToken cancellationToken = default)
    {
        var user = await userManager.FindByIdAsync(userId);
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);

        string decoded;
        try
        {
            decoded = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(code));
        }
        catch (FormatException)
        {
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);
        }

        var result = await userManager.ConfirmEmailAsync(user, decoded);
        if (!result.Succeeded)
        {
            logger.LogWarning("Email confirmation failed for {UserId}: {Errors}", userId,
                string.Join(", ", result.Errors.Select(e => e.Code)));
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);
        }

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ResendConfirmationAsync(
        string email,
        CancellationToken cancellationToken = default)
    {
        var user = await userManager.FindByEmailAsync(email.Trim());

        // The answer is the same whether or not the address exists: this endpoint must not
        // become a way to discover who has an account.
        if (user is null || user.EmailConfirmed)
            return Result<bool>.Success(true);

        var name = await FirstNameAsync(user.Id, cancellationToken);
        await TrySendConfirmationAsync(user, name, NormaliseLanguage(user.PreferredLanguageCode), cancellationToken);

        return Result<bool>.Success(true);
    }

    private async Task<Result<RegistrationResult>> ExistingAccountAsync(
        ApplicationUser user,
        string language,
        CancellationToken cancellationToken)
    {
        var name = await FirstNameAsync(user.Id, cancellationToken);
        var sent = true;

        if (!user.EmailConfirmed)
        {
            // The common case behind a duplicate: the first confirmation never landed
            // or was lost. Sending it again is what the person actually needs.
            (sent, _) = await TrySendConfirmationAsync(user, name, language, cancellationToken);
        }
        else
        {
            try
            {
                var content = AccountEmails.AccountBestaatAl(
                    name,
                    appUrlProvider.ToAbsoluteUrl("/Account/Inloggen"),
                    appUrlProvider.ToAbsoluteUrl("/Account/WachtwoordVergeten"),
                    language);

                await emailDispatcher.SendAsync(
                    new EmailMessage(user.Email!, Bilingual.Same(content.Subject), content.Html),
                    cancellationToken);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Could not send the account-exists email to {Email}.", user.Email);
                sent = false;
            }
        }

        var result = Result<RegistrationResult>.Success(new RegistrationResult
        {
            UserId = user.Id,
            Email = user.Email ?? string.Empty
        });

        if (!sent)
            result.Messages.Add(new ResultMessage(MessageSeverity.Warning, AccountMessages.Registratie.EmailNietVerzonden));

        return result;
    }

    private async Task<(bool Sent, string Url)> TrySendConfirmationAsync(
        ApplicationUser user,
        string name,
        string language,
        CancellationToken cancellationToken)
    {
        string url = string.Empty;

        try
        {
            var token = await userManager.GenerateEmailConfirmationTokenAsync(user);
            var code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));

            url = appUrlProvider.ToAbsoluteUrl(
                $"/Account/Bevestig?userId={Uri.EscapeDataString(user.Id)}&code={Uri.EscapeDataString(code)}");

            var content = AccountEmails.Bevestig(name, url, language);
            await emailDispatcher.SendAsync(
                new EmailMessage(user.Email!, Bilingual.Same(content.Subject), content.Html),
                cancellationToken);

            return (true, url);
        }
        catch (Exception ex)
        {
            // Registration itself has succeeded. A mail failure is reported as a warning on the
            // page; the account and the address stay, and the link can be resent later.
            logger.LogError(ex, "Could not send confirmation email to {Email}. Link was {Url}.",
                user.Email, url);
            return (false, url);
        }
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

    private static string NormaliseLanguage(string? code) => code == "en" ? "en" : "nl";
}

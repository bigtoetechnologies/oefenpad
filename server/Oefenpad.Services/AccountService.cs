using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB;
using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.Services.Mappings;

namespace Oefenpad.Services;

public class AccountService(
    UserManager<ApplicationUser> userManager,
    SignInManager<ApplicationUser> signInManager,
    IOefenpadContextFactory contextFactory,
    IEmailDispatcher emailDispatcher,
    IAppUrlProvider appUrlProvider,
    ICurrentUserService currentUser,
    ILogger<AccountService> logger) : IAccountService
{
    public async Task<Result<AccountProfileDto>> GetProfileAsync(CancellationToken cancellationToken = default)
    {
        var user = await GetUserAsync();
        if (user is null)
            return ResultHelpers.Fout<AccountProfileDto>(AccountMessages.Beheer.NietIngelogd);

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);
        var person = await context.Persons
            .AsNoTracking()
            .Where(p => p.ApplicationUserId == user.Id)
            .Select(PersonMappings.ToDto)
            .FirstOrDefaultAsync(cancellationToken);

        if (person is null)
            return ResultHelpers.Fout<AccountProfileDto>(AccountMessages.Beheer.ProfielNietGevonden);

        return Result<AccountProfileDto>.Success(new AccountProfileDto
        {
            PersonId = person.Id,
            FirstName = person.FirstName,
            LastName = person.LastName,
            Email = user.Email ?? string.Empty,
            PreferredLanguageCode = Language(user)
        });
    }

    public async Task<Result<bool>> ChangeNameAsync(
        ChangeNameRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await GetUserAsync();
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        await using var context = await contextFactory.CreateContextAsync(cancellationToken);
        var person = await context.Persons
            .FirstOrDefaultAsync(p => p.ApplicationUserId == user.Id, cancellationToken);

        if (person is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.ProfielNietGevonden);

        person.FirstName = request.FirstName.Trim();
        person.LastName = request.LastName.Trim();
        await context.SaveChangesAsync(cancellationToken);

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ChangePasswordAsync(
        ChangePasswordRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await GetUserAsync();
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        var result = await userManager.ChangePasswordAsync(user, request.CurrentPassword, request.NewPassword);
        if (!result.Succeeded)
        {
            var failure = new Result<bool>();
            failure.Messages.AddRange(IdentityErrorTranslator.ToMessages(result));
            return failure;
        }

        // The change rotates the security stamp; refreshing now keeps this session valid
        // instead of signing the person out within the minute.
        await signInManager.RefreshSignInAsync(user);

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ChangeEmailAsync(
        ChangeEmailRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await GetUserAsync();
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        if (!await userManager.CheckPasswordAsync(user, request.CurrentPassword))
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.WachtwoordHuidigFout);

        var newEmail = request.NewEmail.Trim();

        if (string.Equals(user.Email, newEmail, StringComparison.OrdinalIgnoreCase))
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.EmailHetzelfde);

        var existing = await userManager.FindByEmailAsync(newEmail);
        if (existing is not null && existing.Id != user.Id)
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.EmailAlInGebruik);

        var oldEmail = user.Email ?? newEmail;

        // The account keeps its current address until the new one proves itself. Moving
        // it first would lock the learner out on a single mistyped character, and would
        // let whoever owns the typo address confirm it and take the account over.
        var language = Language(user);
        var name = await FirstNameAsync(user.Id, cancellationToken);

        try
        {
            var token = await userManager.GenerateChangeEmailTokenAsync(user, newEmail);
            var code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
            var link = appUrlProvider.ToAbsoluteUrl(
                $"/Account/Bevestig?userId={Uri.EscapeDataString(user.Id)}" +
                $"&email={Uri.EscapeDataString(newEmail)}" +
                $"&code={Uri.EscapeDataString(code)}");

            var confirmation = AccountEmails.BevestigNieuweEmail(name, link, language);
            await emailDispatcher.SendAsync(
                new EmailMessage(newEmail, Bilingual.Same(confirmation.Subject), confirmation.Html),
                cancellationToken);

            var notice = AccountEmails.EmailGewijzigd(name, newEmail, language);
            await emailDispatcher.SendAsync(
                new EmailMessage(oldEmail, Bilingual.Same(notice.Subject), notice.Html),
                cancellationToken);
        }
        catch (Exception ex)
        {
            // Nothing has moved, so the person can simply try again.
            logger.LogError(ex, "Could not send email-change confirmation for {UserId}.", user.Id);
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.EmailNietVerzonden);
        }

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ConfirmEmailChangeAsync(
        string userId,
        string newEmail,
        string code,
        CancellationToken cancellationToken = default)
    {
        var user = await userManager.FindByIdAsync(userId);
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);

        string token;
        try
        {
            token = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(code));
        }
        catch (FormatException)
        {
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);
        }

        var changed = await userManager.ChangeEmailAsync(user, newEmail, token);
        if (!changed.Succeeded)
            return ResultHelpers.Fout<bool>(AccountMessages.Registratie.BevestigOngeldig);

        // The username is the address, as it was at registration. Keep the two in step.
        var setUserName = await userManager.SetUserNameAsync(user, newEmail);
        if (!setUserName.Succeeded)
            return ResultHelpers.Fouten<bool>(setUserName.Errors.Select(IdentityErrorTranslator.Translate));

        // The cookie still carries the old address; end the session so the next sign-in
        // is made with the new one.
        await signInManager.SignOutAsync();

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ChangeLanguageAsync(
        string languageCode,
        CancellationToken cancellationToken = default)
    {
        var user = await GetUserAsync();
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.NietIngelogd);

        user.PreferredLanguageCode = languageCode == "en" ? "en" : "nl";

        var result = await userManager.UpdateAsync(user);
        if (!result.Succeeded)
            return ResultHelpers.Fouten<bool>(result.Errors.Select(IdentityErrorTranslator.Translate));

        await signInManager.RefreshSignInAsync(user);

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> SendPasswordResetAsync(
        string email,
        CancellationToken cancellationToken = default)
    {
        var user = await userManager.FindByEmailAsync(email.Trim());

        // Same answer either way: this endpoint must not reveal which addresses have accounts.
        if (user is null)
            return Result<bool>.Success(true);

        try
        {
            var token = await userManager.GeneratePasswordResetTokenAsync(user);
            var code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
            var link = appUrlProvider.ToAbsoluteUrl(
                $"/Account/WachtwoordHerstellen?email={Uri.EscapeDataString(user.Email ?? email)}&code={Uri.EscapeDataString(code)}");

            var name = await FirstNameAsync(user.Id, cancellationToken);
            var content = AccountEmails.WachtwoordHerstellen(name, link, Language(user));

            await emailDispatcher.SendAsync(
                new EmailMessage(user.Email ?? email, Bilingual.Same(content.Subject), content.Html),
                cancellationToken);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Could not send password-reset email for {Email}.", email);
        }

        return Result<bool>.Success(true);
    }

    public async Task<Result<bool>> ResetPasswordAsync(
        ResetPasswordRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await userManager.FindByEmailAsync(request.Email.Trim());
        if (user is null)
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.HerstelOngeldig);

        string decoded;
        try
        {
            decoded = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(request.Code));
        }
        catch (FormatException)
        {
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.HerstelOngeldig);
        }

        var result = await userManager.ResetPasswordAsync(user, decoded, request.Password);
        if (!result.Succeeded)
        {
            logger.LogWarning("Password reset failed for {UserId}: {Errors}", user.Id,
                string.Join(", ", result.Errors.Select(e => e.Code)));
            return ResultHelpers.Fout<bool>(AccountMessages.Beheer.HerstelOngeldig);
        }

        try
        {
            var name = await FirstNameAsync(user.Id, cancellationToken);
            var content = AccountEmails.WachtwoordGewijzigd(name, Language(user));
            await emailDispatcher.SendAsync(
                new EmailMessage(user.Email ?? request.Email, Bilingual.Same(content.Subject), content.Html),
                cancellationToken);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Could not send password-changed notice for {UserId}.", user.Id);
        }

        return Result<bool>.Success(true);
    }

    private async Task<ApplicationUser?> GetUserAsync()
    {
        if (!currentUser.IsAuthenticated || string.IsNullOrWhiteSpace(currentUser.UserId))
            return null;

        return await userManager.FindByIdAsync(currentUser.UserId);
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

    private static string Language(ApplicationUser user) => user.PreferredLanguageCode == "en" ? "en" : "nl";
}

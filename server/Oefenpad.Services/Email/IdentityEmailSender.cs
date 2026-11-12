using Microsoft.AspNetCore.Identity;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs;
using Oefenpad.Resources.Account;

namespace Oefenpad.Services.Email;

/// <summary>
/// Bridges Identity's <see cref="IEmailSender{TUser}"/> contract to the same dispatcher every
/// other account email uses, so a resend triggered by Identity is branded and translated too.
/// </summary>
public class IdentityEmailSender(IEmailDispatcher emailDispatcher) : IEmailSender<ApplicationUser>
{
    public Task SendConfirmationLinkAsync(ApplicationUser user, string email, string confirmationLink)
        => SendAsync(user, email, AccountEmails.Bevestig(Name(user), confirmationLink, Language(user)));

    public Task SendPasswordResetLinkAsync(ApplicationUser user, string email, string resetLink)
        => SendAsync(user, email, AccountEmails.WachtwoordHerstellen(Name(user), resetLink, Language(user)));

    public Task SendPasswordResetCodeAsync(ApplicationUser user, string email, string resetCode)
        => emailDispatcher.SendAsync(new EmailMessage(
            email,
            new Bilingual("Je herstelcode", "Your reset code"),
            $"<p style=\"font-size:28px;font-weight:900;letter-spacing:0.12em\">{resetCode}</p>"));

    private Task SendAsync(ApplicationUser user, string email, EmailContent content)
        => emailDispatcher.SendAsync(new EmailMessage(
            email,
            Bilingual.Same(content.Subject),
            content.Html));

    private static string Name(ApplicationUser user)
        => user.UserName?.Split('@')[0] ?? string.Empty;

    private static string Language(ApplicationUser user)
        => user.PreferredLanguageCode == "en" ? "en" : "nl";
}

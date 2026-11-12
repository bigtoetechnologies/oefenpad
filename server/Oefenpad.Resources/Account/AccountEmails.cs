using System.Net;

namespace Oefenpad.Resources.Account;

public sealed record EmailContent(string Subject, string Html);

/// <summary>
/// The five account emails, rendered in the recipient's language. Styling is inline because
/// email clients cannot read the site's CSS, but the palette and the heavy type are the same.
/// </summary>
public static class AccountEmails
{
    public static EmailContent Bevestig(string naam, string link, string taal)
        => taal == "en"
            ? new("Confirm your email address",
                Wrap("Confirm your email address",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>Welcome to Oefenpad. Confirm your email address so you can sign in.</p>" +
                    Button("Confirm my email address", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">The link works for 24 hours. If you did not create an account, ignore this email.</p>"))
            : new("Bevestig je e-mailadres",
                Wrap("Bevestig je e-mailadres",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Welkom bij Oefenpad. Bevestig je e-mailadres, dan kun je inloggen.</p>" +
                    Button("Bevestig mijn e-mailadres", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">De link werkt 24 uur. Heb je geen account gemaakt? Dan kun je deze e-mail negeren.</p>"));

    public static EmailContent BevestigNieuweEmail(string naam, string link, string taal)
        => taal == "en"
            ? new("Confirm your new email address",
                Wrap("Confirm your new email address",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>Use the button below to confirm this address for your Oefenpad account.</p>" +
                    Button("Confirm this address", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">Until you confirm, the account cannot sign in. The link works for 24 hours.</p>"))
            : new("Bevestig je nieuwe e-mailadres",
                Wrap("Bevestig je nieuwe e-mailadres",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Bevestig dit adres voor je Oefenpad-account met de knop hieronder.</p>" +
                    Button("Bevestig dit adres", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">Tot je bevestigt, kun je niet inloggen. De link werkt 24 uur.</p>"));

    public static EmailContent WachtwoordHerstellen(string naam, string link, string taal)
        => taal == "en"
            ? new("Reset your password",
                Wrap("Reset your password",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>Choose a new password for your Oefenpad account.</p>" +
                    Button("Choose a new password", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">The link works for 24 hours. If you did not ask for this, ignore this email; your password stays the same.</p>"))
            : new("Herstel je wachtwoord",
                Wrap("Herstel je wachtwoord",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Kies een nieuw wachtwoord voor je Oefenpad-account.</p>" +
                    Button("Kies een nieuw wachtwoord", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">De link werkt 24 uur. Heb je dit niet gevraagd? Dan kun je deze e-mail negeren; je wachtwoord blijft hetzelfde.</p>"));

    public static EmailContent WachtwoordGewijzigd(string naam, string taal)
        => taal == "en"
            ? new("Your password has been changed",
                Wrap("Your password has been changed",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>The password for your Oefenpad account has just been changed.</p>" +
                    "<p>If this was not you, reset your password immediately.</p>"))
            : new("Je wachtwoord is gewijzigd",
                Wrap("Je wachtwoord is gewijzigd",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Het wachtwoord van je Oefenpad-account is zojuist gewijzigd.</p>" +
                    "<p>Was jij dit niet? Herstel dan meteen je wachtwoord.</p>"));

    public static EmailContent EmailGewijzigd(string naam, string nieuwAdres, string taal)
        => taal == "en"
            ? new("The email address on your account is changing",
                Wrap("The email address on your account is changing",
                    $"<p>Hello {Name(naam)},</p>" +
                    $"<p>The email address for your Oefenpad account is being changed to <strong>{WebUtility.HtmlEncode(nieuwAdres)}</strong>.</p>" +
                    "<p>You will receive a confirmation link at the new address. If you did not ask for this, reply to this email.</p>"))
            : new("Het e-mailadres van je account verandert",
                Wrap("Het e-mailadres van je account verandert",
                    $"<p>Hallo {Name(naam)},</p>" +
                    $"<p>Het e-mailadres van je Oefenpad-account wordt gewijzigd naar <strong>{WebUtility.HtmlEncode(nieuwAdres)}</strong>.</p>" +
                    "<p>Je krijgt een bevestigingslink op het nieuwe adres. Heb je dit niet gevraagd? Antwoord dan op deze e-mail.</p>"));

    public static EmailContent AccountVerwijderen(string naam, string link, string taal)
        => taal == "en"
            ? new("Delete your Oefenpad account",
                Wrap("Delete your Oefenpad account",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>Use the button below to delete your account and your profile. This cannot be undone.</p>" +
                    Button("Delete my account", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">The link works for one hour. If you did not ask for this, ignore this email; your account stays as it is.</p>"))
            : new("Verwijder je Oefenpad-account",
                Wrap("Verwijder je Oefenpad-account",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Verwijder met de knop hieronder je account en je profiel. Dit kan niet ongedaan worden gemaakt.</p>" +
                    Button("Verwijder mijn account", link) +
                    Fallback(link, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">De link werkt één uur. Heb je dit niet gevraagd? Dan kun je deze e-mail negeren; je account blijft zoals het is.</p>"));

    public static EmailContent AccountBestaatAl(string naam, string inlogLink, string herstelLink, string taal)
        => taal == "en"
            ? new("You already have an Oefenpad account",
                Wrap("You already have an Oefenpad account",
                    $"<p>Hello {Name(naam)},</p>" +
                    "<p>Someone tried to create an account with this email address. You already have one, so nothing has changed.</p>" +
                    Button("Sign in", inlogLink) +
                    $"<p>Forgot your password? <a href=\"{WebUtility.HtmlEncode(herstelLink)}\" style=\"color:#2B50C8\">Choose a new one</a>.</p>" +
                    Fallback(inlogLink, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">Did you not ask for this? You can ignore this email.</p>"))
            : new("Je hebt al een account bij Oefenpad",
                Wrap("Je hebt al een account bij Oefenpad",
                    $"<p>Hallo {Name(naam)},</p>" +
                    "<p>Iemand probeerde een account te maken met dit e-mailadres. Je hebt er al een, dus er is niets veranderd.</p>" +
                    Button("Inloggen", inlogLink) +
                    $"<p>Wachtwoord vergeten? <a href=\"{WebUtility.HtmlEncode(herstelLink)}\" style=\"color:#2B50C8\">Kies een nieuw wachtwoord</a>.</p>" +
                    Fallback(inlogLink, taal) +
                    "<p style=\"color:#5C6578;font-size:13px\">Heb je dit niet gedaan? Dan kun je deze e-mail negeren.</p>"));

    private static string Name(string naam)
        => string.IsNullOrWhiteSpace(naam) ? string.Empty : WebUtility.HtmlEncode(naam.Trim());

    private static string Button(string label, string link)
        => $"<p style=\"margin:24px 0\"><a href=\"{WebUtility.HtmlEncode(link)}\" " +
           "style=\"display:inline-block;background:#E8601F;color:#FFFFFF;text-decoration:none;" +
           "font-weight:800;font-size:16px;padding:14px 26px\">" +
           WebUtility.HtmlEncode(label) + "</a></p>";

    private static string Fallback(string link, string taal)
        => taal == "en"
            ? "<p style=\"color:#5C6578;font-size:13px;line-height:1.5\">" +
              "Button not working? Copy this link into your browser:<br>" +
              "<span style=\"color:#2B50C8;word-break:break-all\">" + WebUtility.HtmlEncode(link) + "</span></p>"
            : "<p style=\"color:#5C6578;font-size:13px;line-height:1.5\">" +
              "Werkt de knop niet? Kopieer deze link naar je browser:<br>" +
              "<span style=\"color:#2B50C8;word-break:break-all\">" + WebUtility.HtmlEncode(link) + "</span></p>";

    private static string Wrap(string title, string body)
        => "<!DOCTYPE html><html><head><meta charset=\"utf-8\">" +
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>" +
           WebUtility.HtmlEncode(title) + "</title></head>" +
           "<body style=\"margin:0;padding:0;background:#F2F4F7;color:#101522;" +
           "font-family:Archivo,'Segoe UI',Arial,sans-serif\">" +
           "<table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" " +
           "style=\"background:#F2F4F7;padding:24px 12px\"><tr><td align=\"center\">" +
           "<table role=\"presentation\" width=\"560\" cellpadding=\"0\" cellspacing=\"0\" " +
           "style=\"max-width:560px;width:100%;background:#FFFFFF;border-top:8px solid #2B50C8\">" +
           "<tr><td style=\"padding:24px 28px 6px;font-size:22px;font-weight:900;letter-spacing:-0.03em\">Oefenpad</td></tr>" +
           "<tr><td style=\"padding:0 28px 8px;font-size:22px;font-weight:800;letter-spacing:-0.02em\">" +
           WebUtility.HtmlEncode(title) + "</td></tr>" +
           "<tr><td style=\"padding:0 28px 28px;font-size:15px;line-height:1.6\">" + body + "</td></tr>" +
           "</table></td></tr></table></body></html>";
}

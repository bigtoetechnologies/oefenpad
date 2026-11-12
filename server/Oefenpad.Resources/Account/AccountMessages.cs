using Oefenpad.DTOs;

namespace Oefenpad.Resources.Account;

/// <summary>
/// Every sentence the account pages and services can show. Kept as <see cref="Bilingual"/>
/// rather than .resx: both languages travel together, and the markup renders both, so
/// nothing depends on the request culture.
/// </summary>
public static class AccountMessages
{
    public static class Validatie
    {
        public static readonly Bilingual VoornaamVerplicht =
            new("Vul je voornaam in.", "Enter your first name.");

        public static readonly Bilingual AchternaamVerplicht =
            new("Vul je achternaam in.", "Enter your last name.");

        public static readonly Bilingual NaamTeLang =
            new("Een naam mag hoogstens 50 tekens hebben.", "A name can be at most 50 characters.");

        public static readonly Bilingual EmailVerplicht =
            new("Vul je e-mailadres in.", "Enter your email address.");

        public static readonly Bilingual EmailOngeldig =
            new("Dit lijkt geen geldig e-mailadres.", "That does not look like a valid email address.");

        public static readonly Bilingual EmailTeLang =
            new("Een e-mailadres mag hoogstens 256 tekens hebben.", "An email address can be at most 256 characters.");

        public static readonly Bilingual WachtwoordVerplicht =
            new("Vul je wachtwoord in.", "Enter your password.");

        public static readonly Bilingual WachtwoordTeKort =
            new("Je wachtwoord moet minstens 10 tekens hebben.", "Your password must be at least 10 characters.");

        public static readonly Bilingual WachtwoordZonderCijfer =
            new("Je wachtwoord moet minstens één cijfer bevatten.", "Your password must contain at least one digit.");

        public static readonly Bilingual WachtwoordKomtNietOvereen =
            new("De twee wachtwoorden zijn niet gelijk.", "The two passwords do not match.");

        public static readonly Bilingual WachtwoordHetzelfde =
            new("Het nieuwe wachtwoord moet verschillen van het huidige.", "The new password must differ from the current one.");

        public static readonly Bilingual VoorwaardenNodig =
            new("Je moet de voorwaarden accepteren om een account te maken.", "You must accept the terms to create an account.");

        public static readonly Bilingual TaalOngeldig =
            new("Kies Nederlands of Engels.", "Choose Dutch or English.");

        public static readonly Bilingual CodeVerplicht =
            new("Deze link mist een code. Vraag een nieuwe aan.", "This link is missing its code. Request a new one.");
    }

    public static class Registratie
    {
        public static readonly Bilingual Gelukt =
            new("Controleer je e-mail. We hebben je een bericht gestuurd om verder te gaan.",
                "Check your email. We have sent you a message to continue.");

        public static readonly Bilingual Mislukt =
            new("Het account kon niet worden aangemaakt. Probeer het opnieuw.",
                "The account could not be created. Please try again.");

        public static readonly Bilingual EmailAlInGebruik =
            new("Er bestaat al een account met dit e-mailadres.", "An account with this email address already exists.");

        public static readonly Bilingual BevestigOngeldig =
            new("Deze bevestigingslink is niet geldig of is verlopen. Vraag een nieuwe aan.",
                "This confirmation link is invalid or has expired. Request a new one.");

        public static readonly Bilingual BevestigGelukt =
            new("Je e-mailadres is bevestigd. Je kunt nu inloggen.", "Your email address is confirmed. You can sign in now.");

        public static readonly Bilingual BevestigVerzonden =
            new("Als dat adres bij ons bekend is, hebben we een nieuwe bevestigingslink gestuurd.",
                "If that address is known to us, we have sent a new confirmation link.");

        public static readonly Bilingual EmailNietVerzonden =
            new("Je account bestaat, maar de bevestigingsmail kon niet worden verstuurd. Probeer het later opnieuw.",
                "Your account exists, but the confirmation email could not be sent. Try again later.");
    }

    public static class Inloggen
    {
        public static readonly Bilingual Mislukt =
            new("E-mailadres of wachtwoord is niet juist.", "Email address or password is incorrect.");

        public static readonly Bilingual NietBevestigd =
            new("Bevestig eerst je e-mailadres via de link in je inbox.",
                "Confirm your email address first using the link in your inbox.");

        public static readonly Bilingual Vergrendeld =
            new("Te veel pogingen. Probeer het over vijf minuten opnieuw.",
                "Too many attempts. Try again in five minutes.");

        public static readonly Bilingual Uitgelogd =
            new("Je bent uitgelogd.", "You have signed out.");
    }

    public static class Beheer
    {
        public static readonly Bilingual NietIngelogd =
            new("Log in om je account te beheren.", "Sign in to manage your account.");

        public static readonly Bilingual ProfielNietGevonden =
            new("Je profiel kon niet worden gevonden.", "Your profile could not be found.");

        public static readonly Bilingual NaamGewijzigd =
            new("Je naam is bijgewerkt.", "Your name has been updated.");

        public static readonly Bilingual WachtwoordGewijzigd =
            new("Je wachtwoord is gewijzigd.", "Your password has been changed.");

        public static readonly Bilingual WachtwoordHuidigFout =
            new("Je huidige wachtwoord is niet juist.", "Your current password is incorrect.");

        public static readonly Bilingual EmailGewijzigd =
            new("Je nieuwe e-mailadres moet nog worden bevestigd. We hebben een link gestuurd.",
                "Your new email address still needs confirming. We have sent a link.");

        public static readonly Bilingual EmailHetzelfde =
            new("Dat is al je e-mailadres.", "That is already your email address.");

        public static readonly Bilingual TaalGewijzigd =
            new("De taal van je e-mails is bijgewerkt.", "Your email language has been updated.");

        public static readonly Bilingual HerstelVerzonden =
            new("Als dat adres bij ons bekend is, hebben we een link gestuurd om je wachtwoord te herstellen.",
                "If that address is known to us, we have sent a link to reset your password.");

        public static readonly Bilingual HerstelOngeldig =
            new("Deze herstellink is niet geldig of is verlopen. Vraag een nieuwe aan.",
                "This reset link is invalid or has expired. Request a new one.");

        public static readonly Bilingual Hersteld =
            new("Je wachtwoord is hersteld. Je kunt nu inloggen.", "Your password has been reset. You can sign in now.");

        public static readonly Bilingual OnbekendeFout =
            new("Er ging iets mis. Probeer het opnieuw.", "Something went wrong. Please try again.");
    }

    public static class Verwijderen
    {
        public static readonly Bilingual MailVerzonden =
            new("We hebben een link gestuurd om je account te verwijderen. De link werkt één uur.",
                "We have sent a link to delete your account. The link works for one hour.");

        public static readonly Bilingual TokenOngeldig =
            new("Deze verwijderlink is niet geldig of is verlopen.", "This deletion link is invalid or has expired.");

        public static readonly Bilingual Gelukt =
            new("Je account en je gegevens zijn verwijderd.", "Your account and your data have been deleted.");

        public static readonly Bilingual Mislukt =
            new("Het account kon niet worden verwijderd. Probeer het opnieuw.",
                "The account could not be deleted. Please try again.");

        public static readonly Bilingual WachtwoordFout =
            new("Je wachtwoord is niet juist.", "Your password is incorrect.");
    }
}

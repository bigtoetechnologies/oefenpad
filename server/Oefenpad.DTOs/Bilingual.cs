namespace Oefenpad.DTOs;

/// <summary>
/// A user-facing sentence in both of the site's languages.
/// Oefenpad ships Dutch and English in the same markup and lets CSS choose;
/// carrying both here means the service layer never guesses the request culture.
/// </summary>
public sealed record Bilingual(string Nl, string En)
{
    public static Bilingual Same(string text) => new(text, text);

    public string For(string? languageCode) =>
        string.Equals(languageCode, "en", StringComparison.OrdinalIgnoreCase) ? En : Nl;
}

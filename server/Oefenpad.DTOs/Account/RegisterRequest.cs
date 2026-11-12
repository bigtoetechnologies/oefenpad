namespace Oefenpad.DTOs.Account;

/// <summary>
/// Everything the registration form submits. Validation lives in
/// <c>Oefenpad.Validation</c>; this type carries only the values.
/// </summary>
public sealed class RegisterRequest
{
    public string FirstName { get; set; } = string.Empty;

    public string LastName { get; set; } = string.Empty;

    public string Email { get; set; } = string.Empty;

    public string Password { get; set; } = string.Empty;

    public string ConfirmPassword { get; set; } = string.Empty;

    public bool TermsAccepted { get; set; }

    /// <summary>ISO 639-1 code for account email; "nl" when not chosen.</summary>
    public string PreferredLanguageCode { get; set; } = "nl";
}

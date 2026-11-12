namespace Oefenpad.DTOs.Account;

public sealed class AccountProfileDto
{
    public int PersonId { get; init; }
    public string FirstName { get; init; } = string.Empty;
    public string LastName { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
    public string PreferredLanguageCode { get; init; } = "nl";
}

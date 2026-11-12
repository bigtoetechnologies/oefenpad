namespace Oefenpad.DTOs.Account;

public sealed class ChangeNameRequest
{
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
}

namespace Oefenpad.DTOs.Account;

public sealed class ChangeEmailRequest
{
    public string CurrentPassword { get; set; } = string.Empty;
    public string NewEmail { get; set; } = string.Empty;
}

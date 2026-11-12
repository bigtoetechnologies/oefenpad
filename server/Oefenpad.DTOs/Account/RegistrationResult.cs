namespace Oefenpad.DTOs.Account;

public sealed class RegistrationResult
{
    public required string UserId { get; init; }

    public required string Email { get; init; }

    /// <summary>
    /// The confirmation link that was emailed. The registration page shows it only in
    /// Development, where there is no real mailbox to open.
    /// </summary>
    public string? ConfirmationUrl { get; init; }
}

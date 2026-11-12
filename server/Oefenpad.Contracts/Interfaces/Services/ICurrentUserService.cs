namespace Oefenpad.Contracts.Interfaces.Services;

/// <summary>
/// The signed-in learner, read from the cookie's claims. An anonymous request reads
/// null / false and callers fail closed.
/// </summary>
public interface ICurrentUserService
{
    bool IsAuthenticated { get; }

    string? UserId { get; }

    int? PersonId { get; }

    string? Email { get; }

    /// <summary>"nl" or "en"; Dutch when the account has not chosen.</summary>
    string PreferredLanguageCode { get; }
}

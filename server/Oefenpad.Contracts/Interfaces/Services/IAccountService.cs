using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;

namespace Oefenpad.Contracts.Interfaces.Services;

public interface IAccountService
{
    Task<Result<AccountProfileDto>> GetProfileAsync(CancellationToken cancellationToken = default);

    Task<Result<bool>> ChangeNameAsync(ChangeNameRequest request, CancellationToken cancellationToken = default);

    Task<Result<bool>> ChangePasswordAsync(ChangePasswordRequest request, CancellationToken cancellationToken = default);

    /// <summary>
    /// Verifies the current password and emails a confirmation link to the new address.
    /// The account keeps its current address until that link is followed, so a typo
    /// cannot lock the learner out or hand the account to whoever owns the typo.
    /// </summary>
    Task<Result<bool>> ChangeEmailAsync(ChangeEmailRequest request, CancellationToken cancellationToken = default);

    /// <summary>
    /// Applies a pending address change once its emailed link is followed.
    /// </summary>
    Task<Result<bool>> ConfirmEmailChangeAsync(
        string userId,
        string newEmail,
        string code,
        CancellationToken cancellationToken = default);

    Task<Result<bool>> ChangeLanguageAsync(string languageCode, CancellationToken cancellationToken = default);

    Task<Result<bool>> SendPasswordResetAsync(string email, CancellationToken cancellationToken = default);

    Task<Result<bool>> ResetPasswordAsync(ResetPasswordRequest request, CancellationToken cancellationToken = default);
}

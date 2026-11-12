using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;

namespace Oefenpad.Contracts.Interfaces.Services;

public interface IRegistrationService
{
    /// <summary>
    /// Creates the Identity user and its Person, then emails a confirmation link.
    /// A duplicate address is returned as a failure, never thrown.
    /// </summary>
    Task<Result<RegistrationResult>> RegisterAsync(RegisterRequest request, CancellationToken cancellationToken = default);

    Task<Result<bool>> ConfirmEmailAsync(string userId, string code, CancellationToken cancellationToken = default);

    /// <summary>
    /// Sends a fresh confirmation link. Always reports success so the endpoint cannot be
    /// used to discover which addresses have accounts.
    /// </summary>
    Task<Result<bool>> ResendConfirmationAsync(string email, CancellationToken cancellationToken = default);
}

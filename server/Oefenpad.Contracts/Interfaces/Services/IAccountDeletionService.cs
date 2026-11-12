using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;

namespace Oefenpad.Contracts.Interfaces.Services;

public interface IAccountDeletionService
{
    /// <summary>Verifies the password and emails a one-hour deletion link.</summary>
    Task<Result<bool>> RequestDeletionAsync(DeleteAccountRequest request, CancellationToken cancellationToken = default);

    Task<Result<bool>> ConfirmDeletionAsync(string token, CancellationToken cancellationToken = default);
}

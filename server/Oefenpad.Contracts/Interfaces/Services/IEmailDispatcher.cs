using Oefenpad.DTOs;

namespace Oefenpad.Contracts.Interfaces.Services;

/// <summary>
/// The single way out for account email. Development uses a file sink; production uses
/// SMTP when configured, so services never know which is in play.
/// </summary>
public interface IEmailDispatcher
{
    Task SendAsync(EmailMessage message, CancellationToken cancellationToken = default);
}

namespace Oefenpad.Contracts.Interfaces.Services;

/// <summary>
/// Builds absolute links for email. <c>App:BaseUrl</c> wins when configured; otherwise
/// the current request supplies scheme and host.
/// </summary>
public interface IAppUrlProvider
{
    string ToAbsoluteUrl(string relativePath);
}

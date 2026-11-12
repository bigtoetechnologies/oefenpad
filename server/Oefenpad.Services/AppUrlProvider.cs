using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Oefenpad.Contracts.Interfaces.Services;

namespace Oefenpad.Services;

/// <summary>
/// Absolute links for email. A configured <c>App:BaseUrl</c> wins, because the request may
/// arrive on an internal host behind a proxy; otherwise the current request supplies it.
/// </summary>
public class AppUrlProvider(
    IConfiguration configuration,
    IHttpContextAccessor httpContextAccessor) : IAppUrlProvider
{
    public const string BaseUrlKey = "App:BaseUrl";

    public string ToAbsoluteUrl(string relativePath)
    {
        var path = relativePath.TrimStart('/');

        var configured = configuration[BaseUrlKey];
        if (!string.IsNullOrWhiteSpace(configured))
        {
            if (!configured.EndsWith('/'))
                configured += "/";

            if (Uri.TryCreate(configured, UriKind.Absolute, out var baseUri)
                && (baseUri.Scheme == Uri.UriSchemeHttp || baseUri.Scheme == Uri.UriSchemeHttps))
            {
                return new Uri(baseUri, path).ToString();
            }
        }

        var request = httpContextAccessor.HttpContext?.Request;
        if (request is not null)
            return $"{request.Scheme}://{request.Host}{request.PathBase}/{path}";

        return relativePath;
    }
}

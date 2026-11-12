using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using Oefenpad.Contracts.Interfaces.Services;

namespace Oefenpad.Services;

/// <summary>
/// Reads the signed-in learner from the authentication cookie. Anonymous requests read
/// null / false, and every caller treats that as "not allowed".
/// </summary>
public class CurrentUserService(IHttpContextAccessor httpContextAccessor) : ICurrentUserService
{
    private ClaimsPrincipal? User => httpContextAccessor.HttpContext?.User;

    public bool IsAuthenticated => User?.Identity?.IsAuthenticated ?? false;

    public string? UserId => User?.FindFirstValue(ClaimTypes.NameIdentifier);

    public int? PersonId
    {
        get
        {
            var value = User?.FindFirstValue(ClaimsKeys.PersonId);
            return int.TryParse(value, out var id) ? id : null;
        }
    }

    public string? Email => User?.FindFirstValue(ClaimTypes.Email) ?? User?.Identity?.Name;

    public string PreferredLanguageCode =>
        User?.FindFirstValue(ClaimsKeys.PreferredLanguage) == "en" ? "en" : "nl";
}

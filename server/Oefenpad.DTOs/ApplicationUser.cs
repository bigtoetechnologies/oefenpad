using Microsoft.AspNetCore.Identity;

namespace Oefenpad.DTOs;

/// <summary>
/// The Identity account. Profile data lives on <c>Person</c>; keeping them apart means
/// a person can outlive an account, the same split TotumTeams uses.
/// </summary>
public class ApplicationUser : IdentityUser
{
    /// <summary>ISO 639-1 code used for account email. Null means Dutch.</summary>
    public string? PreferredLanguageCode { get; set; }
}

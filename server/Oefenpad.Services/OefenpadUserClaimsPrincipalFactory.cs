using System.Security.Claims;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Oefenpad.DB;
using Oefenpad.DTOs;

namespace Oefenpad.Services;

/// <summary>
/// Adds the Person id and the email language to the cookie, so audit stamps and outgoing
/// mail do not need a database lookup on every request.
/// </summary>
public class OefenpadUserClaimsPrincipalFactory(
    UserManager<ApplicationUser> userManager,
    RoleManager<IdentityRole> roleManager,
    IOptions<IdentityOptions> options,
    IOefenpadContextFactory contextFactory)
    : UserClaimsPrincipalFactory<ApplicationUser, IdentityRole>(userManager, roleManager, options)
{
    protected override async Task<ClaimsIdentity> GenerateClaimsAsync(ApplicationUser user)
    {
        var identity = await base.GenerateClaimsAsync(user);

        await using var context = await contextFactory.CreateContextAsync();
        var personId = await context.Persons
            .AsNoTracking()
            .Where(p => p.ApplicationUserId == user.Id)
            .Select(p => p.Id)
            .FirstOrDefaultAsync();

        if (personId != 0)
            identity.AddClaim(new Claim(ClaimsKeys.PersonId, personId.ToString()));

        identity.AddClaim(new Claim(
            ClaimsKeys.PreferredLanguage,
            user.PreferredLanguageCode == "en" ? "en" : "nl"));

        return identity;
    }
}

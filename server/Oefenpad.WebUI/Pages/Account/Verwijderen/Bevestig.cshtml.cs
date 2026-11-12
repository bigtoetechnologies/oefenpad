using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account.Verwijderen;

/// <summary>
/// The emailed link is the credential here, so the page is anonymous: a person may open it
/// on a phone where they are not signed in.
/// </summary>
[EnableRateLimiting(RateLimitPolicies.DeleteAccount)]
public class BevestigModel(
    IAccountDeletionService deletionService,
    SignInManager<ApplicationUser> signInManager) : AccountPageModel
{
    [BindProperty(SupportsGet = true)]
    public string? Token { get; set; }

    public bool Verwijderd { get; private set; }

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (string.IsNullOrWhiteSpace(Token))
        {
            VoegFoutToe(AccountMessages.Verwijderen.TokenOngeldig);
            return Page();
        }

        var resultaat = await deletionService.ConfirmDeletionAsync(Token, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        // If the link was opened while signed in, the cookie now points at a deleted user.
        await signInManager.SignOutAsync();

        Verwijderd = true;
        VoegGeluktToe(AccountMessages.Verwijderen.Gelukt);

        return Page();
    }
}

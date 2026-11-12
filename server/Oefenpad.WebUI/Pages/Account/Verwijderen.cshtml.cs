using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[Authorize]
[EnableRateLimiting(RateLimitPolicies.DeleteAccount)]
public class VerwijderenModel(
    IAccountDeletionService deletionService,
    IValidator<DeleteAccountRequest> validator) : AccountPageModel
{
    [BindProperty]
    public DeleteAccountRequest Invoer { get; set; } = new();

    public bool Verzonden { get; private set; }

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await deletionService.RequestDeletionAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        Verzonden = true;
        VoegGeluktToe(AccountMessages.Verwijderen.MailVerzonden);

        return Page();
    }
}

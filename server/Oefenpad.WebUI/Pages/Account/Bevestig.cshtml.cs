using Microsoft.AspNetCore.Mvc;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Resources.Account;

namespace Oefenpad.WebUI.Pages.Account;

public class BevestigModel(
    IRegistrationService registrationService,
    IAccountService accountService) : AccountPageModel
{
    public bool Bevestigd { get; private set; }

    public async Task<IActionResult> OnGetAsync(string? userId, string? code, string? email)
    {
        if (string.IsNullOrWhiteSpace(userId) || string.IsNullOrWhiteSpace(code))
        {
            VoegFoutToe(AccountMessages.Registratie.BevestigOngeldig);
            return Page();
        }

        // An address on the link means this is a pending change, not a first
        // confirmation: the account only moves to it here.
        var resultaat = string.IsNullOrWhiteSpace(email)
            ? await registrationService.ConfirmEmailAsync(userId, code, HttpContext.RequestAborted)
            : await accountService.ConfirmEmailChangeAsync(
                userId, email.Trim(), code, HttpContext.RequestAborted);

        NeemResultaatOver(resultaat);
        Bevestigd = resultaat.IsSuccess;

        if (Bevestigd)
            VoegGeluktToe(AccountMessages.Registratie.BevestigGelukt);

        return Page();
    }
}

using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[Authorize]
[EnableRateLimiting(RateLimitPolicies.ChangeEmail)]
public class EmailModel(
    IAccountService accountService,
    IValidator<ChangeEmailRequest> validator) : AccountPageModel
{
    [BindProperty]
    public ChangeEmailRequest Invoer { get; set; } = new();

    public string HuidigEmail { get; private set; } = string.Empty;

    public async Task<IActionResult> OnGetAsync()
    {
        var resultaat = await accountService.GetProfileAsync(HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        HuidigEmail = resultaat.ResultContent!.Email;
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        Invoer.NewEmail = Invoer.NewEmail.Trim();

        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await accountService.ChangeEmailAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        // Nothing has moved yet: the account keeps its current address until the link in
        // the new mailbox is followed, so the session stays as it is.
        var profiel = await accountService.GetProfileAsync(HttpContext.RequestAborted);
        if (profiel.IsSuccess) HuidigEmail = profiel.ResultContent!.Email;

        Invoer = new ChangeEmailRequest();
        ModelState.Clear();
        VoegGeluktToe(Oefenpad.Resources.Account.AccountMessages.Beheer.EmailGewijzigd);
        return Page();
    }
}

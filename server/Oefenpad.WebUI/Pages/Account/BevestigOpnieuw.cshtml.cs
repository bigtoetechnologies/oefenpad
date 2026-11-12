using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[EnableRateLimiting(RateLimitPolicies.ResendConfirmation)]
public class BevestigOpnieuwModel(IRegistrationService registrationService) : AccountPageModel
{
    [BindProperty]
    public string Email { get; set; } = string.Empty;

    public bool Verzonden { get; private set; }

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        Email = Email.Trim();

        if (!new EmailAddressAttribute().IsValid(Email))
        {
            VoegFoutToe(AccountMessages.Validatie.EmailOngeldig);
            return Page();
        }

        await registrationService.ResendConfirmationAsync(Email, HttpContext.RequestAborted);

        Verzonden = true;
        VoegGeluktToe(AccountMessages.Registratie.BevestigVerzonden);

        return Page();
    }
}

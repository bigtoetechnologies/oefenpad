using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[EnableRateLimiting(RateLimitPolicies.PasswordReset)]
public class WachtwoordVergetenModel(IAccountService accountService) : AccountPageModel
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

        await accountService.SendPasswordResetAsync(Email, HttpContext.RequestAborted);

        // The same answer whether or not the address exists.
        Verzonden = true;
        VoegGeluktToe(AccountMessages.Beheer.HerstelVerzonden);

        return Page();
    }
}

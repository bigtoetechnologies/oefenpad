using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;

namespace Oefenpad.WebUI.Pages.Account;

[Authorize]
public class WachtwoordModel(
    IAccountService accountService,
    IValidator<ChangePasswordRequest> validator) : AccountPageModel
{
    [BindProperty]
    public ChangePasswordRequest Invoer { get; set; } = new();

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await accountService.ChangePasswordAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        return Redirect("/Account/Account?gewijzigd=wachtwoord");
    }
}

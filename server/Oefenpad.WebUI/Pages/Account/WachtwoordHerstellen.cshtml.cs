using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;

namespace Oefenpad.WebUI.Pages.Account;

public class WachtwoordHerstellenModel(
    IAccountService accountService,
    IValidator<ResetPasswordRequest> validator) : AccountPageModel
{
    [BindProperty]
    public ResetPasswordRequest Invoer { get; set; } = new();

    public void OnGet(string? email, string? code)
    {
        Invoer.Email = email ?? string.Empty;
        Invoer.Code = code ?? string.Empty;
    }

    public async Task<IActionResult> OnPostAsync()
    {
        Invoer.Email = Invoer.Email.Trim();

        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await accountService.ResetPasswordAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        return Redirect("/Account/Inloggen?hersteld=1");
    }
}

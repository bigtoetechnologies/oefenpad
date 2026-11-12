using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;

namespace Oefenpad.WebUI.Pages.Account;

[Authorize]
public class NaamModel(
    IAccountService accountService,
    IValidator<ChangeNameRequest> validator) : AccountPageModel
{
    [BindProperty]
    public ChangeNameRequest Invoer { get; set; } = new();

    public async Task<IActionResult> OnGetAsync()
    {
        var resultaat = await accountService.GetProfileAsync(HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        Invoer.FirstName = resultaat.ResultContent!.FirstName;
        Invoer.LastName = resultaat.ResultContent.LastName;

        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        Invoer.FirstName = Invoer.FirstName.Trim();
        Invoer.LastName = Invoer.LastName.Trim();

        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await accountService.ChangeNameAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        return Redirect("/Account/Account?gewijzigd=naam");
    }
}

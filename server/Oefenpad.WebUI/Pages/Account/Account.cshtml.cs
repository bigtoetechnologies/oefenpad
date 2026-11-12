using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.WebUI.Pages.Account;

[Authorize]
public class AccountModel(IAccountService accountService) : AccountPageModel
{
    public AccountProfileDto? Profiel { get; private set; }

    public async Task<IActionResult> OnGetAsync(string? gewijzigd = null)
    {
        await LoadProfileAsync();

        switch (gewijzigd)
        {
            case "naam":
                VoegGeluktToe(AccountMessages.Beheer.NaamGewijzigd);
                break;
            case "wachtwoord":
                VoegGeluktToe(AccountMessages.Beheer.WachtwoordGewijzigd);
                break;
            case "taal":
                VoegGeluktToe(AccountMessages.Beheer.TaalGewijzigd);
                break;
        }

        return Page();
    }

    /// <summary>The two language buttons post here; a language change is not a page of its own.</summary>
    public async Task<IActionResult> OnPostAsync(string? taal)
    {
        if (taal is not ("nl" or "en"))
            return Redirect("/Account/Account");

        var resultaat = await accountService.ChangeLanguageAsync(taal, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            await LoadProfileAsync();
            return Page();
        }

        return Redirect("/Account/Account?gewijzigd=taal");
    }

    private async Task LoadProfileAsync()
    {
        var resultaat = await accountService.GetProfileAsync(HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return;
        }

        Profiel = resultaat.ResultContent;
    }
}

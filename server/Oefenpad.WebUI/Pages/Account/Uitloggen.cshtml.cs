using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Oefenpad.DTOs;

namespace Oefenpad.WebUI.Pages.Account;

public class UitloggenModel(SignInManager<ApplicationUser> signInManager) : PageModel
{
    public IActionResult OnGet() => Redirect("/");

    public async Task<IActionResult> OnPostAsync()
    {
        await signInManager.SignOutAsync();
        return Redirect("/Account/Inloggen?uitgelogd=1");
    }
}

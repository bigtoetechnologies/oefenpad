using FluentValidation;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.DTOs;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[EnableRateLimiting(RateLimitPolicies.Login)]
public class InloggenModel(
    SignInManager<ApplicationUser> signInManager,
    UserManager<ApplicationUser> userManager,
    IValidator<LoginRequest> validator) : AccountPageModel
{
    [BindProperty]
    public LoginRequest Invoer { get; set; } = new();

    public string? ReturnUrl { get; private set; }

    public bool Hersteld { get; private set; }

    public bool EmailBevestig { get; private set; }

    public bool Uitgelogd { get; private set; }

    public void OnGet(
        string? returnUrl = null,
        bool hersteld = false,
        bool emailbevestig = false,
        bool uitgelogd = false)
    {
        ReturnUrl = returnUrl;
        Hersteld = hersteld;
        EmailBevestig = emailbevestig;
        Uitgelogd = uitgelogd;
    }

    public async Task<IActionResult> OnPostAsync(string? returnUrl = null)
    {
        ReturnUrl = returnUrl;
        Invoer.Email = Invoer.Email.Trim();

        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var user = await userManager.FindByEmailAsync(Invoer.Email.Trim());

        // An unknown address and a wrong password give the same sentence: the form must not
        // reveal which addresses have accounts.
        if (user is null)
        {
            VoegFoutToe(AccountMessages.Inloggen.Mislukt);
            return Page();
        }

        var resultaat = await signInManager.PasswordSignInAsync(
            user, Invoer.Password, Invoer.RememberMe, lockoutOnFailure: true);

        if (resultaat.Succeeded)
        {
            if (Url.IsLocalUrl(ReturnUrl))
                return LocalRedirect(ReturnUrl!);

            return Redirect("/Account/Account");
        }

        if (resultaat.IsNotAllowed)
            VoegFoutToe(AccountMessages.Inloggen.NietBevestigd);
        else if (resultaat.IsLockedOut)
            VoegFoutToe(AccountMessages.Inloggen.Vergrendeld);
        else
            VoegFoutToe(AccountMessages.Inloggen.Mislukt);

        return Page();
    }
}

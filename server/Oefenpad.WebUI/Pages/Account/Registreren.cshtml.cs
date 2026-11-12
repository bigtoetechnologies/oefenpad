using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.WebUI.Services;

namespace Oefenpad.WebUI.Pages.Account;

[EnableRateLimiting(RateLimitPolicies.Register)]
public class RegistrerenModel(
    IRegistrationService registrationService,
    IValidator<RegisterRequest> validator,
    IWebHostEnvironment environment,
    ILogger<RegistrerenModel> logger) : AccountPageModel
{
    [BindProperty]
    public RegisterRequest Invoer { get; set; } = new();

    public bool Verzonden { get; private set; }

    public string? Bevestigingslink { get; private set; }

    public void OnGet()
    {
    }

    public async Task<IActionResult> OnPostAsync()
    {
        Invoer.FirstName = Invoer.FirstName.Trim();
        Invoer.LastName = Invoer.LastName.Trim();
        Invoer.Email = Invoer.Email.Trim();

        if (!await ValideerAsync(validator, Invoer))
            return Page();

        var resultaat = await registrationService.RegisterAsync(Invoer, HttpContext.RequestAborted);

        if (!resultaat.IsSuccess)
        {
            NeemResultaatOver(resultaat);
            return Page();
        }

        Verzonden = true;
        NeemResultaatOver(resultaat);
        VoegGeluktToe(AccountMessages.Registratie.Gelukt);

        // There is no real mailbox in development; showing the link is the only way to
        // finish the flow locally. It is never rendered outside Development.
        if (environment.IsDevelopment())
            Bevestigingslink = resultaat.ResultContent?.ConfirmationUrl;

        logger.LogInformation("Registration completed for {Email}.", Invoer.Email);

        return Page();
    }
}

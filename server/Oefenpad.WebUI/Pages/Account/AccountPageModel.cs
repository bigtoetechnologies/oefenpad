using FluentValidation;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Oefenpad.DTOs;
using Oefenpad.Enums;

namespace Oefenpad.WebUI.Pages.Account;

/// <summary>
/// Shared plumbing for the account pages: bilingual messages, field error marks, and the
/// bridge from FluentValidation's <c>CustomState</c> back to both languages.
/// </summary>
public abstract class AccountPageModel : PageModel
{
    public List<Bilingual> Fouten { get; } = [];
    public List<Bilingual> Waarschuwingen { get; } = [];
    public List<Bilingual> Gelukt { get; } = [];
    public HashSet<string> FouteVelden { get; } = new(StringComparer.OrdinalIgnoreCase);

    protected void VoegFoutToe(Bilingual bericht) => Fouten.Add(bericht);

    protected void VoegGeluktToe(Bilingual bericht) => Gelukt.Add(bericht);

    protected void NeemResultaatOver<T>(Result<T> resultaat)
    {
        foreach (var message in resultaat.Messages)
        {
            switch (message.Severity)
            {
                case MessageSeverity.Error:
                    Fouten.Add(message.Text);
                    break;
                case MessageSeverity.Warning:
                    Waarschuwingen.Add(message.Text);
                    break;
                default:
                    Gelukt.Add(message.Text);
                    break;
            }
        }
    }

    protected async Task<bool> ValideerAsync<T>(IValidator<T> validator, T model)
    {
        var resultaat = await validator.ValidateAsync(model, HttpContext.RequestAborted);
        if (resultaat.IsValid)
            return true;

        foreach (var fout in resultaat.Errors)
        {
            Fouten.Add(fout.CustomState as Bilingual ?? Bilingual.Same(fout.ErrorMessage));

            if (!string.IsNullOrEmpty(fout.PropertyName))
                FouteVelden.Add(fout.PropertyName);
        }

        return false;
    }

    public string VeldClass(string property)
        => FouteVelden.Contains(property) ? "veld heeft-fout" : "veld";
}

using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class RegisterRequestValidator : AbstractValidator<RegisterRequest>
{
    public RegisterRequestValidator()
    {
        RuleFor(x => x.FirstName).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.VoornaamVerplicht)
            .MaximumLength(50).MetBericht(AccountMessages.Validatie.NaamTeLang);

        RuleFor(x => x.LastName).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.AchternaamVerplicht)
            .MaximumLength(50).MetBericht(AccountMessages.Validatie.NaamTeLang);

        RuleFor(x => x.Email).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.EmailVerplicht)
            .EmailAddress().MetBericht(AccountMessages.Validatie.EmailOngeldig)
            .MaximumLength(256).MetBericht(AccountMessages.Validatie.EmailTeLang);

        RuleFor(x => x.Password).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht)
            .MinimumLength(10).MetBericht(AccountMessages.Validatie.WachtwoordTeKort)
            .Matches("[0-9]").MetBericht(AccountMessages.Validatie.WachtwoordZonderCijfer);

        RuleFor(x => x.ConfirmPassword)
            .Equal(x => x.Password).MetBericht(AccountMessages.Validatie.WachtwoordKomtNietOvereen);

        RuleFor(x => x.TermsAccepted)
            .Must(accepted => accepted).MetBericht(AccountMessages.Validatie.VoorwaardenNodig);

        RuleFor(x => x.PreferredLanguageCode)
            .Must(code => code is "nl" or "en").MetBericht(AccountMessages.Validatie.TaalOngeldig);
    }
}

using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class ChangeEmailRequestValidator : AbstractValidator<ChangeEmailRequest>
{
    public ChangeEmailRequestValidator()
    {
        RuleFor(x => x.CurrentPassword)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht);

        RuleFor(x => x.NewEmail).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.EmailVerplicht)
            .EmailAddress().MetBericht(AccountMessages.Validatie.EmailOngeldig)
            .MaximumLength(256).MetBericht(AccountMessages.Validatie.EmailTeLang);
    }
}

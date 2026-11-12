using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class ChangeNameRequestValidator : AbstractValidator<ChangeNameRequest>
{
    public ChangeNameRequestValidator()
    {
        RuleFor(x => x.FirstName).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.VoornaamVerplicht)
            .MaximumLength(50).MetBericht(AccountMessages.Validatie.NaamTeLang);

        RuleFor(x => x.LastName).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.AchternaamVerplicht)
            .MaximumLength(50).MetBericht(AccountMessages.Validatie.NaamTeLang);
    }
}

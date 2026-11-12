using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class LoginRequestValidator : AbstractValidator<LoginRequest>
{
    public LoginRequestValidator()
    {
        RuleFor(x => x.Email).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.EmailVerplicht)
            .EmailAddress().MetBericht(AccountMessages.Validatie.EmailOngeldig);

        RuleFor(x => x.Password)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht);
    }
}

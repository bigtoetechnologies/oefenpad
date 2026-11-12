using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class ResetPasswordRequestValidator : AbstractValidator<ResetPasswordRequest>
{
    public ResetPasswordRequestValidator()
    {
        RuleFor(x => x.Email).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.EmailVerplicht)
            .EmailAddress().MetBericht(AccountMessages.Validatie.EmailOngeldig);

        RuleFor(x => x.Code)
            .NotEmpty().MetBericht(AccountMessages.Validatie.CodeVerplicht);

        RuleFor(x => x.Password).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht)
            .MinimumLength(10).MetBericht(AccountMessages.Validatie.WachtwoordTeKort)
            .Matches("[0-9]").MetBericht(AccountMessages.Validatie.WachtwoordZonderCijfer);

        RuleFor(x => x.ConfirmPassword)
            .Equal(x => x.Password).MetBericht(AccountMessages.Validatie.WachtwoordKomtNietOvereen);
    }
}

using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class ChangePasswordRequestValidator : AbstractValidator<ChangePasswordRequest>
{
    public ChangePasswordRequestValidator()
    {
        RuleFor(x => x.CurrentPassword)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht);

        RuleFor(x => x.NewPassword).Cascade(CascadeMode.Stop)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht)
            .MinimumLength(10).MetBericht(AccountMessages.Validatie.WachtwoordTeKort)
            .Matches("[0-9]").MetBericht(AccountMessages.Validatie.WachtwoordZonderCijfer)
            .NotEqual(x => x.CurrentPassword).MetBericht(AccountMessages.Validatie.WachtwoordHetzelfde);

        RuleFor(x => x.ConfirmPassword)
            .Equal(x => x.NewPassword).MetBericht(AccountMessages.Validatie.WachtwoordKomtNietOvereen);
    }
}

using FluentValidation;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;

namespace Oefenpad.Validation.Account;

public class DeleteAccountRequestValidator : AbstractValidator<DeleteAccountRequest>
{
    public DeleteAccountRequestValidator()
    {
        RuleFor(x => x.Password)
            .NotEmpty().MetBericht(AccountMessages.Validatie.WachtwoordVerplicht);
    }
}

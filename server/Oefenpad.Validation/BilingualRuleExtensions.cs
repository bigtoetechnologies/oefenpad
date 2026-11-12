using FluentValidation;
using Oefenpad.DTOs;

namespace Oefenpad.Validation;

/// <summary>
/// Attaches a <see cref="Bilingual"/> message to a rule. FluentValidation's own message is the
/// Dutch half, so anything that reads <c>ErrorMessage</c> still shows something sensible; the
/// account pages read <c>CustomState</c> and render both languages.
/// </summary>
public static class BilingualRuleExtensions
{
    public static IRuleBuilderOptions<T, TProperty> MetBericht<T, TProperty>(
        this IRuleBuilderOptions<T, TProperty> rule,
        Bilingual message)
    {
        return rule
            .WithMessage(message.Nl)
            .WithState(_ => message);
    }
}

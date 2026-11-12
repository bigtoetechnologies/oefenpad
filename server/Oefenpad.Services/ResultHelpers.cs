using Microsoft.AspNetCore.Identity;
using Oefenpad.DTOs;
using Oefenpad.Enums;
using Oefenpad.Resources.Account;

namespace Oefenpad.Services;

/// <summary>
/// Turns Identity's English error codes into sentences in both site languages. Anything
/// unrecognised falls back to Identity's own text rather than being hidden.
/// </summary>
public static class IdentityErrorTranslator
{
    public static Bilingual Translate(IdentityError error) => error.Code switch
    {
        "DuplicateUserName" or "DuplicateEmail" => AccountMessages.Registratie.EmailAlInGebruik,
        "PasswordMismatch" => AccountMessages.Beheer.WachtwoordHuidigFout,
        "PasswordTooShort" => AccountMessages.Validatie.WachtwoordTeKort,
        "PasswordRequiresDigit" => AccountMessages.Validatie.WachtwoordZonderCijfer,
        "InvalidToken" => AccountMessages.Beheer.HerstelOngeldig,
        _ => Bilingual.Same(error.Description)
    };

    public static List<ResultMessage> ToMessages(IdentityResult result)
        => result.Errors
            .Select(Translate)
            .Distinct()
            .Select(message => new ResultMessage(MessageSeverity.Error, message))
            .ToList();
}

public static class ResultHelpers
{
    public static Result<T> Fout<T>(Bilingual message, MessageSeverity severity = MessageSeverity.Error)
        => Result<T>.Failure(new ResultMessage(severity, message));

    public static Result<T> Fouten<T>(IEnumerable<Bilingual> messages)
        => Result<T>.Failure(messages
            .Select(message => new ResultMessage(MessageSeverity.Error, message))
            .ToArray());
}

using Oefenpad.Enums;

namespace Oefenpad.DTOs;

/// <summary>
/// One message produced by a service. Business-rule failures are returned, never thrown:
/// the caller checks <see cref="Result{T}.IsSuccess"/> and shows these messages.
/// </summary>
public sealed class ResultMessage
{
    public MessageSeverity Severity { get; }

    public Bilingual Text { get; }

    public ResultMessage(MessageSeverity severity, Bilingual text)
    {
        Severity = severity;
        Text = text;
    }
}

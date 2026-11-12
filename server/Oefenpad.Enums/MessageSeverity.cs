namespace Oefenpad.Enums;

/// <summary>
/// The tone of a message returned by a service. The UI decides how to present it;
/// a service never touches HTML.
/// </summary>
public enum MessageSeverity : byte
{
    Info = 0,
    Success = 1,
    Warning = 2,
    Error = 3
}

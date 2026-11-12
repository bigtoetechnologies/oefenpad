namespace Oefenpad.DTOs;

/// <summary>
/// One outbound email. The dispatcher decides how it leaves the machine; the body is
/// already rendered in the recipient's language by the caller.
/// </summary>
public sealed record EmailMessage(string To, Bilingual Subject, string Html);

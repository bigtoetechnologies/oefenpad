namespace Oefenpad.Contracts.Options;

public sealed class EmailOptions
{
    public const string SectionName = "Email";

    /// <summary>Envelope sender. Must be set before SMTP is used.</summary>
    public string FromAddress { get; set; } = "noreply@oefenpad.nl";

    public string FromName { get; set; } = "Oefenpad";

    /// <summary>
    /// Development sink. Relative paths resolve against the WebUI content root.
    /// Empty means <c>email-sink</c> next to the app.
    /// </summary>
    public string SinkPath { get; set; } = "email-sink";

    /// <summary>Empty means "write to the sink" instead of sending.</summary>
    public string SmtpHost { get; set; } = string.Empty;

    public int SmtpPort { get; set; } = 587;

    public bool SmtpUseSsl { get; set; } = true;

    public string SmtpUser { get; set; } = string.Empty;

    public string SmtpPassword { get; set; } = string.Empty;
}

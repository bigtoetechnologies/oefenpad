namespace Oefenpad.Contracts.Options;

public sealed class AppOptions
{
    public const string SectionName = "App";

    /// <summary>
    /// Canonical public address, e.g. https://oefenpad.nl. Used for links in email so they
    /// stay correct behind a proxy or when a request arrives on an internal host name.
    /// </summary>
    public string BaseUrl { get; set; } = string.Empty;
}

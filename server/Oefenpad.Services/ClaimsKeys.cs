namespace Oefenpad.Services;

/// <summary>Claim types this app adds on top of Identity's defaults.</summary>
public static class ClaimsKeys
{
    public const string PersonId = "oefenpad:person_id";
    public const string PreferredLanguage = "oefenpad:taal";
}

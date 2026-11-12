namespace Oefenpad.WebUI.Services;

/// <summary>
/// Named rate-limit policies. The names are referenced by page models, so they live here
/// rather than as string literals in two places.
/// </summary>
public static class RateLimitPolicies
{
    public const string Login = "login";
    public const string Register = "register";
    public const string ResendConfirmation = "resend-confirmation";
    public const string PasswordReset = "password-reset";
    public const string ChangeEmail = "change-email";
    public const string DeleteAccount = "delete-account";
    public const string Games = "games";
}

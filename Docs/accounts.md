# Accounts and sign-up

The static site stays static. Sign-up and account management are a separate
.NET 10 solution in `server/`, served from the same host, using the same
`assets/site/oefenpad.css`, so the account pages are visual siblings of the
home page rather than a second design.

The scope is deliberately one person per account. There are no organisations,
groups, invitations or roles beyond Identity's default role table.

This file is the living how-it-works reference. The session record — decisions,
rejected alternatives, evidence and the full file-by-file map — is in
[`accounts-handover.md`](accounts-handover.md).

## The shape, and what was copied from TotumTeams

TotumTeams is the architectural sample: the project layering, the `Result`
convention, the context factory, the UTC convention, the Identity settings and
the email adapter all follow it. Three things are deliberately different:

| TotumTeams | Here | Why |
|---|---|---|
| Blazor + MudBlazor | Razor Pages, server-rendered | The site's design system is hand-written CSS. A UI framework would fight it, and the pages need no interactive circuit. |
| `.resx` + `IStringLocalizer` | `Bilingual` records | Every page ships Dutch and English in the same markup; a message should carry both, not ask for a culture. |
| Organisations, members, roles | `ApplicationUser` + `Person` only | The agreed scope is a single person. |

Layering, each project referencing only what it needs:

```
Oefenpad.Enums
Oefenpad.DTOs           → Enums
Oefenpad.Contracts      → DTOs                 (interfaces, options)
Oefenpad.Resources      → DTOs                 (bilingual messages, email bodies)
Oefenpad.Validation     → DTOs, Resources      (FluentValidation)
Oefenpad.DB             → DTOs, Contracts      (EF Core, models, builders)
Oefenpad.Services       → Contracts, DB, DTOs, Enums, Resources, Validation
Oefenpad.WebUI          → all of the above     (Razor Pages, Program.cs)
Oefenpad.Tests          → Services, Validation, DB, WebUI
```

## Where the code lives

| Project | What it owns |
|---|---|
| `Oefenpad.Enums` | `MessageSeverity` only. |
| `Oefenpad.DTOs` | `Bilingual`, `Result`, `ResultMessage`, `ApplicationUser`, `EmailMessage`, and the request/profile records under `Account/`. No behaviour. |
| `Oefenpad.Contracts` | Service interfaces, `ICurrentUserService`, `IEmailDispatcher`, `IAppUrlProvider`, and the `App` / `Email` options. |
| `Oefenpad.Resources` | Every user-facing sentence (`AccountMessages`) and every email body (`AccountEmails`). |
| `Oefenpad.Validation` | FluentValidation rules and the `CustomState` bridge. |
| `Oefenpad.DB` | `OefenpadDbContext`, `Person`, `AccountDeletionToken`, model builders, UTC converter, context factory, migrations. |
| `Oefenpad.Services` | Registration, account, deletion, current user, URL provider, claims factory, email dispatchers. |
| `Oefenpad.WebUI` | `Program.cs` (DI, Identity, cookie, rate limits, static files, routes) and the Razor Pages under `Pages/Account/`. |
| `Oefenpad.Tests` | In-memory SQLite harness plus registration and validator tests. |

`Program.cs` is the entry point for anything cross-cutting. `AccountPageModel`
is the shared base for the account pages. `AccountMessages` and `AccountEmails`
are the only places a user-facing string should be written. The handover has the
file-by-file list and a table of where to change what.

## The data model

| Table | Contents |
|---|---|
| `AspNetUsers` | Identity account. `PreferredLanguageCode` is `nl` or `en` and chooses the language of account email. |
| `Persons` | `FirstName`, `LastName`, optional `ApplicationUserId`. Audit columns. Unique index on `ApplicationUserId`. |
| `AccountDeletionTokens` | `TokenHash` (SHA-256 hex), expiry, user. The raw token exists only in the email. |
| `GameSaves` | One live round per `(user, game)`: the game's private state JSON and the round id. Unique on `(ApplicationUserId, Game)`. |
| `GameLevelProgress` | Best score per `(user, game, level)`: `Correct`, `Total`, `CompletedAt`. Unique on the three ids. |
| Identity's own tables | Roles, claims, logins, tokens. |

`OefenpadDbContext` is an `IdentityDbContext<ApplicationUser>`. Every
`DateTime` is converted to UTC both ways, as in TotumTeams. Audit fields are
set in `SaveChangesAsync`; the author is the Person id from the cookie.

All database reads in services are projections (`Select(...)`). There is no
`Include`.

## The flows

| Route | What happens |
|---|---|
| `/Account/Registreren` | Validates with FluentValidation, creates the Identity user, creates the `Person`, emails a confirmation link. A duplicate address is returned as a message, never thrown. If the `Person` save fails the user is deleted again. |
| `/Account/Bevestig` | Decodes the base64url token, calls `ConfirmEmailAsync`. Until this succeeds, `RequireConfirmedEmail` blocks sign-in. |
| `/Account/BevestigOpnieuw` | Sends a fresh link. The answer is identical whether or not the address exists. |
| `/Account/Inloggen` | `PasswordSignInAsync` with lockout on failure. Unconfirmed, locked out and wrong credentials are three distinct bilingual messages. |
| `/Account/Account` | Profile summary, links to name, email and password, email-language buttons, sign-out. |
| `/Account/Naam` | Updates `Person`; the audit stamp records the change. |
| `/Account/Wachtwoord` | `ChangePasswordAsync`, then refreshes the sign-in so the current session survives the security-stamp rotation. |
| `/Account/E-mail` | Verifies the current password, moves email and username, marks the address unconfirmed, emails the new address and a notice to the old one, signs out. |
| `/Account/WachtwoordVergeten` | Emails a reset link; the answer does not reveal whether the address exists. |
| `/Account/WachtwoordHerstellen` | Resets the password and emails a confirmation. |
| `/Account/Verwijderen` | Password, then a one-hour emailed link. Only the token hash is stored. |
| `/Account/Verwijderen/Bevestig` | Removes the `Person`, then deletes the Identity user. The token page is anonymous: the link is the credential. |

Cookie settings: `oefenpad.auth`, `HttpOnly`, `SameSite=Lax`, 14 days with
sliding expiration, security stamp checked every minute. Password reset and
confirmation tokens last 24 hours.

## Email

`IEmailDispatcher` is the only way out. `Email:SmtpHost` empty selects
`FileEmailDispatcher`, which writes each message as an `.html` file under
`server/Oefenpad.WebUI/email-sink/`. Set `Email:SmtpHost` (and the user,
password and sender) to select `SmtpEmailDispatcher` instead.

`IdentityEmailSender` adapts Identity's `IEmailSender<TUser>` to the same
dispatcher, so a resend triggered by Identity is branded and translated too.

In Development the registration page also shows the confirmation link on the
page, clearly marked, because there is no real mailbox. It is never rendered
outside Development.

## Rate limiting

Policies are named in `WebUI/Services/RateLimitPolicies.cs` and applied to the
page model. **Only POST counts.** A Razor Page attribute covers every handler,
including the GET that renders the form; without the method check a person
correcting the form a few times would be turned away. The partition is the
client IP.

| Policy | POSTs allowed |
|---|---|
| Login | 10 per 5 minutes |
| Register | 5 per 10 minutes |
| Resend confirmation | 5 per 10 minutes |
| Password reset | 5 per 10 minutes |
| Change email | 5 per 10 minutes |
| Delete account | 3 per 10 minutes |

## Running it

```sh
# apply migrations and create an empty database
ASPNETCORE_ENVIRONMENT=Development dotnet run --project server/Oefenpad.WebUI -- migrate

# run on 8098 (8080 belongs to the owner)
ASPNETCORE_ENVIRONMENT=Development dotnet run --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098
```

The app applies pending migrations on every normal start too. The database is
`server/Oefenpad.WebUI/oefenpad.db` (SQLite, gitignored). Data Protection keys
are written to `server/Oefenpad.WebUI/dataprotection-keys/`.

Tests:

```sh
dotnet test server/Oefenpad.Tests
```

The host serves only `assets/` and the WebUI `wwwroot/` (which holds the built
React games under `spelen/`), plus the three static HTML pages by explicit
route. Do not serve the repo root itself: it would expose `.git` and `server/`.
The old `src/` game folders are gone.

## Conventions worth keeping

- Business-rule failures are `Result` messages, not exceptions. Unexpected
  failures throw. Sign-in state is checked through `ICurrentUserService`.
- Validation messages are `Bilingual` and travel in FluentValidation's
  `CustomState`; `AccountPageModel.ValideerAsync` reads them and marks the
  field. `.WithMessage` gets the Dutch text so anything else reading
  `ErrorMessage` still shows something sensible.
- Every user-facing sentence is Dutch and English in the markup; the CSS
  switch does the rest. Do not render only one language because the server
  happens to know a culture.
- `Docs/designguide.md` still governs the form styling: hard 2 px inset
  borders, no radius, no shadow, orange for the primary action only.
- Do not add account text to the games. The games remain Dutch-only.

## What must change before accounts go live

1. **The legal pages are now wrong.** `privacy.html` says no account is needed
   and no personal data is collected; `voorwaarden.html` says there is no
   registration. Both need rewriting: which data (name, email, password hash,
   progress), retention, deletion, and the mail provider as a processor. This
   is a legal-text change, not a code cleanup.
2. **The home page says "no account".** Accounts save progress, and
   Voorzetselpaden works in tiers: three levels free, six with an account, the
   last nine behind a paid plan that is not built yet. Word search is still
   open to guests. Decide whether it gets the same free slice and adjust the
   hero and meta description if sign-up becomes required.
3. **Production email and URLs.** `appsettings.json` ships empty placeholder
   keys; fill them through environment variables or a production settings file,
   never by editing the shared file with a live value.

   | Key | Required value | Why |
   |---|---|---|
   | `Email:SmtpHost` | the provider's SMTP host | otherwise mail goes to `email-sink/` |
   | `Email:SmtpPort`, `Email:SmtpUseSsl`, `Email:FromAddress` | match the provider | — |
   | `App:BaseUrl` | `https://oefenpad.nl` (the public origin, no trailing slash) | **mandatory outside Development**: the app throws on start without it, because links would otherwise be built from the caller-controlled `Host` header |
   | `App:KnownProxies` | comma-separated proxy IPs, e.g. `10.0.0.5` | restores `X-Forwarded-Proto` (Secure cookie) and per-client rate-limit partitions behind a TLS-terminating proxy |

   A production start therefore looks like:

   ```sh
   ASPNETCORE_ENVIRONMENT=Production \
   App__BaseUrl=https://oefenpad.nl \
   App__KnownProxies=10.0.0.5 \
   Email__SmtpHost=smtp.example.nl \
   dotnet Oefenpad.WebUI.dll
   ```

   Move the Data Protection keys (`dataprotection-keys/`) somewhere that
   survives a redeploy; the path is currently hard-coded under the content root.
4. **PostgreSQL** when the SQLite file stops being enough. The context is
   already provider-agnostic and `ExecuteWithRetryAsync` is in place for a
   retrying strategy.

using System.Security.Claims;
using System.Threading.RateLimiting;
using FluentValidation;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.FileProviders;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Contracts.Options;
using Oefenpad.DB;
using Oefenpad.DTOs;
using Oefenpad.Services;
using Oefenpad.Services.Email;
using Oefenpad.Services.Games;
using Oefenpad.Validation.Account;
using Oefenpad.WebUI.Api;
using Oefenpad.WebUI.Services;

var builder = WebApplication.CreateBuilder(args);

// ── Where the static site and the database live ──────────────────────────────
// The server sits in server/Oefenpad.WebUI; the repo root is two levels up.
var siteRoot = builder.Configuration["Site:RootPath"];
if (string.IsNullOrWhiteSpace(siteRoot))
    siteRoot = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "..", ".."));
else if (!Path.IsPathRooted(siteRoot))
    siteRoot = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, siteRoot));

var databasePath = builder.Configuration["Database:Path"];
if (string.IsNullOrWhiteSpace(databasePath))
    databasePath = Path.Combine(builder.Environment.ContentRootPath, "oefenpad.db");
else if (!Path.IsPathRooted(databasePath))
    databasePath = Path.Combine(builder.Environment.ContentRootPath, databasePath);

var connectionString = $"Data Source={databasePath}";

// ── Absolute links in email ─────────────────────────────────────────────────
// Without App:BaseUrl, AppUrlProvider falls back to the request's own Host
// header. That header is attacker-controlled, so a password-reset mail would
// carry a link to the attacker's host with a valid token on it. Outside
// Development the base URL is therefore mandatory and the app refuses to start
// without it.
if (!builder.Environment.IsDevelopment()
    && string.IsNullOrWhiteSpace(builder.Configuration[AppUrlProvider.BaseUrlKey]))
{
    throw new InvalidOperationException(
        $"{AppUrlProvider.BaseUrlKey} must be set outside Development: email links would " +
        "otherwise be built from the request's Host header, which the caller controls.");
}

// Behind a TLS-terminating proxy every request reaches Kestrel as plain HTTP
// from the proxy's address, which would leave the auth cookie without Secure
// and collapse every rate-limit partition into one bucket. Set
// App:KnownProxies to the proxy address(es) to restore both.
var knownProxies = (builder.Configuration["App:KnownProxies"] ?? string.Empty)
    .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
    .Select(value => System.Net.IPAddress.TryParse(value, out var address) ? address : null)
    .Where(address => address is not null)
    .ToList();

if (knownProxies.Count > 0)
{
    builder.Services.Configure<ForwardedHeadersOptions>(options =>
    {
        options.ForwardedHeaders =
            ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
        options.KnownProxies.Clear();
        options.KnownIPNetworks.Clear();
        foreach (var proxy in knownProxies) options.KnownProxies.Add(proxy!);
    });
}

// ── Data protection: keep cookies valid across restarts ─────────────────────
var keysPath = Path.Combine(builder.Environment.ContentRootPath, "dataprotection-keys");
Directory.CreateDirectory(keysPath);
builder.Services.AddDataProtection()
    .PersistKeysToFileSystem(new DirectoryInfo(keysPath));

// ── Database and domain services ────────────────────────────────────────────
builder.Services.AddDbContextFactory<OefenpadDbContext>(options => options.UseSqlite(connectionString));

// Identity's stores resolve the context itself, so register a scoped one as well.
builder.Services.AddScoped<OefenpadDbContext>(sp =>
    sp.GetRequiredService<IDbContextFactory<OefenpadDbContext>>().CreateDbContext());

builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<ICurrentUserService, CurrentUserService>();
builder.Services.AddScoped<IOefenpadContextFactory, OefenpadContextFactory>();
builder.Services.AddScoped<IAppUrlProvider, AppUrlProvider>();
builder.Services.AddScoped<IRegistrationService, RegistrationService>();
builder.Services.AddScoped<IAccountService, AccountService>();
builder.Services.AddScoped<IAccountDeletionService, AccountDeletionService>();

// ── Games ───────────────────────────────────────────────────────────────────
// Content banks live in embedded resources; a round's private state lives in
// memory. The browser only ever receives a projected view.
builder.Services.AddSingleton<GameContent>();
builder.Services.AddSingleton<RoundStore>();
builder.Services.AddSingleton<IGameService, PrepositionsService>();
builder.Services.AddSingleton<IGameService, HangmanService>();
builder.Services.AddSingleton<IGameService, MemoryService>();
builder.Services.AddSingleton<IGameService, MatchingService>();
builder.Services.AddSingleton<IGameService, WordSearchService>();
builder.Services.AddSingleton<IGameService, StoryMachineService>();
builder.Services.AddSingleton<GameRegistry>();

// Progress belongs to a signed-in learner, so this is scoped with the request. It
// quietly does nothing for a guest; the game services stay singletons and only
// hand over their private state when the API asks them to.
builder.Services.AddScoped<IGameProgressService, GameProgressService>();

// The free-tier and level-unlock rule reads that progress, so it is scoped too.
// Games that are not gated get an open access object.
builder.Services.AddScoped<GameAccessService>();

builder.Services.Configure<EmailOptions>(builder.Configuration.GetSection(EmailOptions.SectionName));
builder.Services.Configure<AppOptions>(builder.Configuration.GetSection(AppOptions.SectionName));

var emailOptions = builder.Configuration
    .GetSection(EmailOptions.SectionName)
    .Get<EmailOptions>() ?? new EmailOptions();

if (!string.IsNullOrWhiteSpace(emailOptions.SmtpHost))
    builder.Services.AddScoped<IEmailDispatcher, SmtpEmailDispatcher>();
else
    builder.Services.AddScoped<IEmailDispatcher, FileEmailDispatcher>();

// ── Identity ────────────────────────────────────────────────────────────────
builder.Services
    .AddIdentity<ApplicationUser, IdentityRole>(options =>
    {
        // Sign-in is always an explicit act by someone who has proved the address.
        options.SignIn.RequireConfirmedEmail = true;

        options.Lockout.AllowedForNewUsers = true;
        options.Lockout.MaxFailedAccessAttempts = 5;
        options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);

        options.User.RequireUniqueEmail = true;

        // A passphrase is easier to remember than a symbol soup, so length and one digit
        // carry the strength; no mandatory capitals or punctuation.
        options.Password.RequiredLength = 10;
        options.Password.RequireDigit = true;
        options.Password.RequireLowercase = false;
        options.Password.RequireUppercase = false;
        options.Password.RequireNonAlphanumeric = false;

        options.ClaimsIdentity.UserNameClaimType = ClaimTypes.Name;
        options.ClaimsIdentity.EmailClaimType = ClaimTypes.Email;
    })
    .AddEntityFrameworkStores<OefenpadDbContext>()
    .AddClaimsPrincipalFactory<OefenpadUserClaimsPrincipalFactory>()
    .AddDefaultTokenProviders();

builder.Services.AddTransient<IEmailSender<ApplicationUser>, IdentityEmailSender>();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Account/Inloggen";
    options.LogoutPath = "/Account/Uitloggen";
    options.AccessDeniedPath = "/Account/ToegangGeweigerd";

    options.Cookie.Name = "oefenpad.auth";
    options.Cookie.HttpOnly = true;
    options.Cookie.SameSite = SameSiteMode.Lax;
    // SameAsRequest would ship the session cookie without Secure whenever the
    // app sits behind a TLS-terminating proxy, because Kestrel then sees plain
    // HTTP. Development still runs on http://127.0.0.1, so only that relaxes it.
    options.Cookie.SecurePolicy = builder.Environment.IsDevelopment()
        ? CookieSecurePolicy.SameAsRequest
        : CookieSecurePolicy.Always;

    options.ExpireTimeSpan = TimeSpan.FromDays(14);
    options.SlidingExpiration = true;
});

builder.Services.Configure<DataProtectionTokenProviderOptions>(options =>
    options.TokenLifespan = TimeSpan.FromHours(24));

// A password change or reset rotates the security stamp; a one-minute check ends other
// sessions promptly instead of the default thirty minutes.
builder.Services.Configure<SecurityStampValidatorOptions>(options =>
    options.ValidationInterval = TimeSpan.FromMinutes(1));

// ── Abuse limits ────────────────────────────────────────────────────────────
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;

    AddPolicy(options, RateLimitPolicies.Login, permitLimit: 10, TimeSpan.FromMinutes(5));
    AddPolicy(options, RateLimitPolicies.Register, permitLimit: 5, TimeSpan.FromMinutes(10));
    AddPolicy(options, RateLimitPolicies.ResendConfirmation, permitLimit: 5, TimeSpan.FromMinutes(10));
    AddPolicy(options, RateLimitPolicies.PasswordReset, permitLimit: 5, TimeSpan.FromMinutes(10));
    AddPolicy(options, RateLimitPolicies.ChangeEmail, permitLimit: 5, TimeSpan.FromMinutes(10));
    AddPolicy(options, RateLimitPolicies.DeleteAccount, permitLimit: 3, TimeSpan.FromMinutes(10));
    AddPolicy(options, RateLimitPolicies.Games, permitLimit: 600, TimeSpan.FromMinutes(5), postOnly: false);
});

// ── Pages and validators ────────────────────────────────────────────────────
builder.Services.AddRazorPages();
builder.Services.AddValidatorsFromAssemblyContaining<RegisterRequestValidator>();

var app = builder.Build();

// dotnet Oefenpad.WebUI.dll migrate  → apply and exit.
if (args.Contains("migrate"))
{
    await ApplyMigrationsAsync(app);
    return;
}

await ApplyMigrationsAsync(app);

// Must run before anything reads the scheme or the client address: the auth
// cookie's Secure flag and every rate-limit partition depend on both.
if (knownProxies.Count > 0) app.UseForwardedHeaders();

if (!app.Environment.IsDevelopment()) app.UseHsts();

// HttpsRedirection would loop behind a TLS-terminating proxy; only turn it on when this
// app is exposed directly.
var configuredUrls = app.Configuration["urls"]
    ?? app.Configuration["ASPNETCORE_URLS"]
    ?? string.Empty;
var httpsPort = app.Configuration.GetValue<int?>("HttpsRedirection:HttpsPort");
if (httpsPort is not null || configuredUrls.Contains("https://", StringComparison.OrdinalIgnoreCase))
    app.UseHttpsRedirection();

// The static site is served from the repo root, but only the assets folder.
// Serving the root itself would expose .git and server/, and serving src/ would
// hand out the old game scripts and word banks.
var assetsPath = Path.Combine(siteRoot, "assets");
if (Directory.Exists(assetsPath))
{
    app.UseStaticFiles(new StaticFileOptions
    {
        FileProvider = new PhysicalFileProvider(assetsPath),
        RequestPath = "/assets"
    });
}

// The React game app. Its build output lives in this project's wwwroot, so the
// browser never gets a route to the old src/ scripts or the content banks.
app.UseStaticFiles();

app.UseRouting();
app.UseRateLimiter();
app.UseAuthentication();
app.UseAuthorization();

// The three existing static pages, mapped explicitly so the home page and legal pages
// keep their own URLs.
IResult StaticPage(string fileName)
{
    var fullPath = Path.Combine(siteRoot, fileName);
    return File.Exists(fullPath)
        ? Results.File(fullPath, "text/html; charset=utf-8")
        : Results.NotFound();
}

app.MapGet("/", () => StaticPage("index.html"));
app.MapGet("/index.html", () => StaticPage("index.html"));
app.MapGet("/privacy.html", () => StaticPage("privacy.html"));
app.MapGet("/voorwaarden.html", () => StaticPage("voorwaarden.html"));

app.MapGamesApi();
app.MapRazorPages();

// Client-side routes under /spelen/. Static files are served before routing,
// so only application routes reach the fallback. Routing ignores a trailing
// slash, so the one endpoint answers both /spelen and /spelen/; redirecting
// between them would loop. Any deeper route gets the same SPA document.
app.MapGet("/spelen", (IWebHostEnvironment env) =>
{
    var spaIndex = Path.Combine(env.ContentRootPath, "wwwroot", "spelen", "index.html");
    return File.Exists(spaIndex)
        ? Results.File(spaIndex, "text/html; charset=utf-8")
        : Results.NotFound();
});
app.MapFallbackToFile("/spelen/{*path:nonfile}", "spelen/index.html");

app.Run();

static async Task ApplyMigrationsAsync(WebApplication app)
{
    using var scope = app.Services.CreateScope();
    var factory = scope.ServiceProvider.GetRequiredService<IDbContextFactory<OefenpadDbContext>>();
    await using var context = await factory.CreateDbContextAsync();
    await context.Database.MigrateAsync();
}

static void AddPolicy(
    RateLimiterOptions options,
    string name,
    int permitLimit,
    TimeSpan window,
    bool postOnly = true)
{
    options.AddPolicy(name, context =>
    {
        var key = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";

        // Razor Pages put the attribute on every handler of the page, GET included. Only the
        // POST is the abuse case; a GET must never spend the budget a form needs. The game API
        // is read-heavy on purpose, so there every request counts.
        if (postOnly && !HttpMethods.IsPost(context.Request.Method))
            return RateLimitPartition.GetNoLimiter(key);

        return RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: key,
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                Window = window,
                SegmentsPerWindow = 5,
                PermitLimit = permitLimit,
                QueueLimit = 0
            });
    });
}

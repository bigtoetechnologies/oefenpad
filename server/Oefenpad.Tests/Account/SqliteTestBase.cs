using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Http;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB;
using Oefenpad.DTOs;
using Oefenpad.Services;
using Xunit;

namespace Oefenpad.Tests.Account;

/// <summary>
/// One in-memory SQLite database per test, kept open for the test's lifetime. Identity is
/// wired with the same settings the web host uses, so the confirmation gate is real.
/// </summary>
public abstract class SqliteTestBase : IAsyncLifetime
{
    private readonly SqliteConnection _connection;
    private readonly ServiceProvider _provider;

    protected DbContextOptions<OefenpadDbContext> Options { get; }

    protected FakeCurrentUser CurrentUser { get; } = new();

    protected FakeEmailDispatcher Email { get; } = new();

    protected IOefenpadContextFactory ContextFactory { get; }

    protected IAppUrlProvider UrlProvider { get; }

    protected SqliteTestBase()
    {
        _connection = new SqliteConnection("Data Source=:memory:");
        _connection.Open();

        Options = new DbContextOptionsBuilder<OefenpadDbContext>()
            .UseSqlite(_connection)
            .Options;

        using (var context = new OefenpadDbContext(Options))
            context.Database.EnsureCreated();

        ContextFactory = new TestContextFactory(Options, CurrentUser);

        var configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["App:BaseUrl"] = "https://test.oefenpad.local/"
            })
            .Build();

        var services = new ServiceCollection();
        services.AddLogging();
        services.AddHttpContextAccessor();
        services.AddAuthentication();
        services.AddSingleton(Options);
        services.AddScoped<OefenpadDbContext>(_ => new OefenpadDbContext(Options));

        services.AddIdentityCore<ApplicationUser>(options =>
            {
                options.SignIn.RequireConfirmedEmail = true;
                options.User.RequireUniqueEmail = true;
                options.Password.RequiredLength = 10;
                options.Password.RequireDigit = true;
                options.Password.RequireLowercase = false;
                options.Password.RequireUppercase = false;
                options.Password.RequireNonAlphanumeric = false;
            })
            .AddEntityFrameworkStores<OefenpadDbContext>()
            .AddSignInManager()
            .AddDefaultTokenProviders();

        _provider = services.BuildServiceProvider();

        UrlProvider = new AppUrlProvider(
            configuration,
            _provider.GetRequiredService<IHttpContextAccessor>());
    }

    protected UserManager<ApplicationUser> UserManager
        => _provider.GetRequiredService<UserManager<ApplicationUser>>();

    protected SignInManager<ApplicationUser> SignInManager
        => _provider.GetRequiredService<SignInManager<ApplicationUser>>();

    public Task InitializeAsync() => Task.CompletedTask;

    public async Task DisposeAsync()
    {
        await _provider.DisposeAsync();
        await _connection.DisposeAsync();
    }
}

public sealed class FakeCurrentUser : ICurrentUserService
{
    public bool IsAuthenticated { get; set; }
    public string? UserId { get; set; }
    public int? PersonId { get; set; }
    public string? Email { get; set; }
    public string PreferredLanguageCode { get; set; } = "nl";
}

public sealed class FakeEmailDispatcher : IEmailDispatcher
{
    public List<EmailMessage> Messages { get; } = [];

    public Task SendAsync(EmailMessage message, CancellationToken cancellationToken = default)
    {
        Messages.Add(message);
        return Task.CompletedTask;
    }
}

public sealed class TestContextFactory(
    DbContextOptions<OefenpadDbContext> options,
    ICurrentUserService currentUser) : IOefenpadContextFactory
{
    public Task<OefenpadDbContext> CreateContextAsync(CancellationToken cancellationToken = default)
    {
        var context = new OefenpadDbContext(options);
        context.SetCurrentUserService(currentUser);
        return Task.FromResult(context);
    }
}

using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.DB.Models;
using Oefenpad.DTOs;

namespace Oefenpad.DB;

/// <summary>
/// The whole database: Identity's tables plus the learner profile and its deletion tokens.
/// There is no tenant column and no organisation table — one person, one account.
/// </summary>
public class OefenpadDbContext : IdentityDbContext<ApplicationUser>
{
    public OefenpadDbContext(DbContextOptions<OefenpadDbContext> options) : base(options) { }

    public DbSet<Person> Persons => Set<Person>();
    public DbSet<AccountDeletionToken> AccountDeletionTokens => Set<AccountDeletionToken>();
    public DbSet<GameSave> GameSaves => Set<GameSave>();
    public DbSet<GameLevelProgress> GameLevelProgress => Set<GameLevelProgress>();

    protected override void ConfigureConventions(ModelConfigurationBuilder configurationBuilder)
    {
        // All stored values are UTC by convention. SQLite hands every value back as
        // Unspecified; stamping the kind both ways keeps the model honest if the
        // provider is later swapped for PostgreSQL.
        configurationBuilder.Properties<DateTime>().HaveConversion<UtcDateTimeConverter>();
    }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        // Identity's own configuration must come first, then ours may adjust it.
        base.OnModelCreating(builder);
        builder.ApplyConfigurationsFromAssembly(typeof(OefenpadDbContext).Assembly);
    }

    private ICurrentUserService? _currentUserService;

    /// <summary>
    /// Supplies the person id used for the audit columns. Contexts opened through
    /// <see cref="IOefenpadContextFactory"/> get this set; Identity's own store contexts
    /// do not, which is why audit columns are only guaranteed on domain writes.
    /// </summary>
    public void SetCurrentUserService(ICurrentUserService currentUserService)
        => _currentUserService = currentUserService;

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        ApplyAuditFields();
        return await base.SaveChangesAsync(cancellationToken);
    }

    private void ApplyAuditFields()
    {
        var now = DateTime.UtcNow;
        var personId = _currentUserService?.PersonId;

        // Registration and background work have no signed-in person. A null author honestly
        // says "nobody", whereas skipping the block would leave the previous editor's stamp
        // on a row they did not touch.
        foreach (var entry in ChangeTracker.Entries<AuditableEntry>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Property(nameof(AuditableEntry.CreatedAt)).CurrentValue ??= now;
                entry.Property(nameof(AuditableEntry.CreatedBy)).CurrentValue ??= personId;
            }

            if (entry.State == EntityState.Modified)
            {
                entry.Property(nameof(AuditableEntry.UpdatedAt)).CurrentValue = now;
                entry.Property(nameof(AuditableEntry.UpdatedBy)).CurrentValue = personId;
            }
        }
    }
}

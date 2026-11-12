namespace Oefenpad.DB;

/// <summary>
/// Creates a context with the audit user attached. Services must use this rather than
/// resolving <see cref="OefenpadDbContext"/> directly, so updates carry the right author.
/// </summary>
public interface IOefenpadContextFactory
{
    Task<OefenpadDbContext> CreateContextAsync(CancellationToken cancellationToken = default);
}

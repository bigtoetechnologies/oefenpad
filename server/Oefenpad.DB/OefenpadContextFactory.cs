using Microsoft.EntityFrameworkCore;
using Oefenpad.Contracts.Interfaces.Services;

namespace Oefenpad.DB;

public class OefenpadContextFactory(
    IDbContextFactory<OefenpadDbContext> contextFactory,
    ICurrentUserService currentUserService) : IOefenpadContextFactory
{
    public async Task<OefenpadDbContext> CreateContextAsync(CancellationToken cancellationToken = default)
    {
        var context = await contextFactory.CreateDbContextAsync(cancellationToken);
        context.SetCurrentUserService(currentUserService);
        return context;
    }
}

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace Oefenpad.DB;

/// <summary>
/// Used only by <c>dotnet ef</c>. The real connection comes from the WebUI's configuration;
/// migrations never need to reach a database, they only need the model.
/// </summary>
public class OefenpadDbContextFactory : IDesignTimeDbContextFactory<OefenpadDbContext>
{
    public OefenpadDbContext CreateDbContext(string[] args)
    {
        var options = new DbContextOptionsBuilder<OefenpadDbContext>()
            .UseSqlite("Data Source=oefenpad-design.db")
            .Options;

        return new OefenpadDbContext(options);
    }
}

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;

namespace Oefenpad.DB;

public static class OefenpadContextFactoryExtensions
{
    /// <summary>
    /// Runs an operation that opens its own transaction under the database's retry strategy.
    /// A retrying strategy refuses a caller-opened transaction outside this wrapper.
    /// Each attempt gets a fresh context, so a retry starts from what the database holds
    /// rather than from the failed attempt's change tracker.
    /// </summary>
    public static async Task<T> ExecuteWithRetryAsync<T>(
        this IOefenpadContextFactory factory,
        Func<OefenpadDbContext, Task<T>> operation,
        Func<OefenpadDbContext, Task<(bool Succeeded, T Result)>>? verifySucceeded = null,
        CancellationToken cancellationToken = default)
    {
        await using var strategyContext = await factory.CreateContextAsync(cancellationToken);
        return await strategyContext.Database.CreateExecutionStrategy().ExecuteAsync(
            state: 0,
            operation: async (_, _, _) =>
            {
                await using var context = await factory.CreateContextAsync(cancellationToken);
                return await operation(context);
            },
            verifySucceeded: verifySucceeded is null
                ? null
                : async (_, _, _) =>
                {
                    await using var context = await factory.CreateContextAsync(cancellationToken);
                    var (succeeded, result) = await verifySucceeded(context);
                    return new ExecutionResult<T>(succeeded, result);
                });
    }
}

using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace Oefenpad.DB;

/// <summary>
/// Marks DateTime values as UTC on the way into and out of the database, without shifting
/// them: every stored value is UTC by convention, whatever kind the caller left on it.
/// </summary>
public class UtcDateTimeConverter() : ValueConverter<DateTime, DateTime>(
    v => DateTime.SpecifyKind(v, DateTimeKind.Utc),
    v => DateTime.SpecifyKind(v, DateTimeKind.Utc));

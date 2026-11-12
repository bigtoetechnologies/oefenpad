namespace Oefenpad.DB.Models;

/// <summary>
/// Audit stamps every writable domain row. Ids are Person ids, not ApplicationUser ids:
/// the person is the lasting record, the login is one way to reach it.
/// </summary>
public abstract class AuditableEntry
{
    public int? CreatedBy { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public int? UpdatedBy { get; set; }
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

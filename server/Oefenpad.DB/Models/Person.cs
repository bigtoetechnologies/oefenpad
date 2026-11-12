using Oefenpad.DTOs;

namespace Oefenpad.DB.Models;

/// <summary>
/// The learner. Kept apart from <see cref="ApplicationUser"/> so the profile can outlive
/// (or briefly exist without) a login, the same split TotumTeams uses.
/// </summary>
public class Person : AuditableEntry
{
    public int Id { get; set; }

    public required string FirstName { get; set; }

    public required string LastName { get; set; }

    public string? ApplicationUserId { get; set; }

    public ApplicationUser? ApplicationUser { get; set; }
}

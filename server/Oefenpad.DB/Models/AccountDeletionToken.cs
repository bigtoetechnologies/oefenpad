using Oefenpad.DTOs;

namespace Oefenpad.DB.Models;

/// <summary>
/// A one-hour confirmation token for deleting an account under GDPR Article 17.
/// Only the SHA-256 hash is stored, so a database leak cannot be replayed as a deletion link.
/// </summary>
public class AccountDeletionToken
{
    public int Id { get; set; }

    /// <summary>Hex-encoded SHA-256 of the random token sent by email.</summary>
    public required string TokenHash { get; set; }

    public required string ApplicationUserId { get; set; }

    public ApplicationUser? ApplicationUser { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime ExpiresAt { get; set; }
}

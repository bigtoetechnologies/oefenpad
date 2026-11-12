using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Oefenpad.DB.Models;

namespace Oefenpad.DB.ModelBuilders;

public class AccountDeletionTokenBuilder : IEntityTypeConfiguration<AccountDeletionToken>
{
    public void Configure(EntityTypeBuilder<AccountDeletionToken> entity)
    {
        entity.ToTable("AccountDeletionTokens");
        entity.HasKey(x => x.Id);

        entity.HasIndex(x => x.TokenHash).IsUnique();

        entity.Property(x => x.TokenHash).HasMaxLength(64).IsRequired();
        entity.Property(x => x.ApplicationUserId).HasMaxLength(450).IsRequired();

        entity.HasOne(x => x.ApplicationUser)
            .WithMany()
            .HasForeignKey(x => x.ApplicationUserId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}

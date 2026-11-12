using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Oefenpad.DB.Models;

namespace Oefenpad.DB.ModelBuilders;

public class GameSaveBuilder : IEntityTypeConfiguration<GameSave>
{
    public void Configure(EntityTypeBuilder<GameSave> entity)
    {
        entity.ToTable("GameSaves");
        entity.HasKey(s => s.Id);

        entity.Property(s => s.ApplicationUserId).HasMaxLength(450).IsRequired();
        entity.Property(s => s.Game).HasMaxLength(40).IsRequired();
        entity.Property(s => s.RoundId).HasMaxLength(32).IsRequired();
        entity.Property(s => s.StateJson).IsRequired();

        entity.HasOne(s => s.ApplicationUser)
            .WithMany()
            .HasForeignKey(s => s.ApplicationUserId)
            .OnDelete(DeleteBehavior.Cascade);

        entity.HasIndex(s => new { s.ApplicationUserId, s.Game }).IsUnique();
    }
}

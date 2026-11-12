using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Oefenpad.DB.Models;

namespace Oefenpad.DB.ModelBuilders;

public class GameLevelProgressBuilder : IEntityTypeConfiguration<GameLevelProgress>
{
    public void Configure(EntityTypeBuilder<GameLevelProgress> entity)
    {
        entity.ToTable("GameLevelProgress");
        entity.HasKey(p => p.Id);

        entity.Property(p => p.ApplicationUserId).HasMaxLength(450).IsRequired();
        entity.Property(p => p.Game).HasMaxLength(40).IsRequired();
        entity.Property(p => p.LevelId).HasMaxLength(80).IsRequired();

        entity.HasOne(p => p.ApplicationUser)
            .WithMany()
            .HasForeignKey(p => p.ApplicationUserId)
            .OnDelete(DeleteBehavior.Cascade);

        entity.HasIndex(p => new { p.ApplicationUserId, p.Game, p.LevelId }).IsUnique();
    }
}

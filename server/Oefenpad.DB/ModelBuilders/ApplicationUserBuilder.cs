using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Oefenpad.DTOs;

namespace Oefenpad.DB.ModelBuilders;

public class ApplicationUserBuilder : IEntityTypeConfiguration<ApplicationUser>
{
    public void Configure(EntityTypeBuilder<ApplicationUser> entity)
    {
        entity.Property(u => u.PreferredLanguageCode)
            .HasMaxLength(5)
            .IsRequired(false);
    }
}

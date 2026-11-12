using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Oefenpad.DB.Models;

namespace Oefenpad.DB.ModelBuilders;

public class PersonBuilder : IEntityTypeConfiguration<Person>
{
    public void Configure(EntityTypeBuilder<Person> entity)
    {
        entity.ToTable("Persons");
        entity.HasKey(p => p.Id);

        entity.Property(p => p.FirstName).HasMaxLength(50).IsRequired();
        entity.Property(p => p.LastName).HasMaxLength(50).IsRequired();

        entity.HasOne(p => p.ApplicationUser)
            .WithMany()
            .HasForeignKey(p => p.ApplicationUserId)
            .OnDelete(DeleteBehavior.SetNull)
            .IsRequired(false);

        entity.HasIndex(p => p.ApplicationUserId).IsUnique();
    }
}

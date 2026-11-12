using System.Linq.Expressions;
using Oefenpad.DB.Models;
using Oefenpad.DTOs.Account;

namespace Oefenpad.Services.Mappings;

public static class PersonMappings
{
    /// <summary>
    /// A projection, not a mapper call: database reads must select only the columns they
    /// need, never load the entity and map it in memory.
    /// </summary>
    public static readonly Expression<Func<Person, PersonDto>> ToDto =
        p => new PersonDto
        {
            Id = p.Id,
            FirstName = p.FirstName,
            LastName = p.LastName
        };
}

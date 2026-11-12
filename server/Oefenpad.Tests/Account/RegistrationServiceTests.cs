using System.Text;
using FluentAssertions;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using Oefenpad.DB;
using Oefenpad.DB.Models;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.Services;
using Xunit;

namespace Oefenpad.Tests.Account;

public class RegistrationServiceTests : SqliteTestBase
{
    private const string Password = "goedwachtwoord1";

    private RegistrationService CreateService() => new(
        UserManager,
        ContextFactory,
        Email,
        UrlProvider,
        NullLogger<RegistrationService>.Instance);

    private static RegisterRequest NewRequest(string email = "sanne@example.nl") => new()
    {
        FirstName = "Sanne",
        LastName = "de Vries",
        Email = email,
        Password = Password,
        ConfirmPassword = Password,
        TermsAccepted = true,
        PreferredLanguageCode = "nl"
    };

    [Fact]
    public async Task Register_creates_user_person_and_sends_confirmation()
    {
        var service = CreateService();

        var result = await service.RegisterAsync(NewRequest());

        result.IsSuccess.Should().BeTrue();
        result.ResultContent!.Email.Should().Be("sanne@example.nl");

        Email.Messages.Should().HaveCount(1);
        Email.Messages[0].To.Should().Be("sanne@example.nl");
        Email.Messages[0].Html.Should().Contain("/Account/Bevestig");

        await using var context = new OefenpadDbContext(Options);
        var person = await context.Persons.SingleAsync();
        person.FirstName.Should().Be("Sanne");
        person.LastName.Should().Be("de Vries");
        person.ApplicationUserId.Should().Be(result.ResultContent.UserId);
    }

    [Fact]
    public async Task Register_answers_an_existing_address_the_same_way_and_emails_its_holder()
    {
        var service = CreateService();

        (await service.RegisterAsync(NewRequest())).IsSuccess.Should().BeTrue();
        var second = await service.RegisterAsync(NewRequest());

        // The form must not become a way to ask who has an account. The first
        // attempt is still unconfirmed, so the second resends the confirmation.
        second.IsSuccess.Should().BeTrue();
        second.Messages.Should().NotContain(message =>
            message.Text == AccountMessages.Registratie.EmailAlInGebruik);

        await using var context = new OefenpadDbContext(Options);
        (await context.Users.CountAsync()).Should().Be(1);
        (await context.Persons.CountAsync()).Should().Be(1);

        Email.Messages.Should().HaveCount(2);
        Email.Messages[1].Html.Should().Contain("/Account/Bevestig");
    }

    [Fact]
    public async Task Register_for_a_confirmed_address_sends_a_sign_in_route()
    {
        var service = CreateService();
        await service.RegisterAsync(NewRequest());

        var user = await UserManager.FindByEmailAsync("sanne@example.nl");
        var token = await UserManager.GenerateEmailConfirmationTokenAsync(user!);
        var code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));
        (await service.ConfirmEmailAsync(user!.Id, code)).IsSuccess.Should().BeTrue();

        Email.Messages.Clear();
        var second = await service.RegisterAsync(NewRequest());

        second.IsSuccess.Should().BeTrue();
        Email.Messages.Should().ContainSingle();
        Email.Messages[0].Html.Should().Contain("/Account/Inloggen");
        Email.Messages[0].Html.Should().Contain("/Account/WachtwoordVergeten");
    }

    [Fact]
    public async Task Unconfirmed_address_cannot_sign_in_and_confirmation_unlocks_it()
    {
        var service = CreateService();
        var registered = await service.RegisterAsync(NewRequest());
        registered.IsSuccess.Should().BeTrue();

        var user = await UserManager.FindByEmailAsync("sanne@example.nl");
        user.Should().NotBeNull();

        var blocked = await SignInManager.CheckPasswordSignInAsync(user!, Password, lockoutOnFailure: false);
        blocked.IsNotAllowed.Should().BeTrue("RequireConfirmedEmail is on");

        var token = await UserManager.GenerateEmailConfirmationTokenAsync(user!);
        var code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(token));

        var confirmed = await service.ConfirmEmailAsync(user!.Id, code);
        confirmed.IsSuccess.Should().BeTrue();

        var allowed = await SignInManager.CheckPasswordSignInAsync(user!, Password, lockoutOnFailure: false);
        allowed.Succeeded.Should().BeTrue();
    }

    [Fact]
    public async Task Confirmation_rejects_a_tampered_code()
    {
        var service = CreateService();
        var registered = await service.RegisterAsync(NewRequest());

        var result = await service.ConfirmEmailAsync(registered.ResultContent!.UserId, "niet-een-code");

        result.IsSuccess.Should().BeFalse();
        result.Messages.Should().Contain(message =>
            message.Text == AccountMessages.Registratie.BevestigOngeldig);
    }
}

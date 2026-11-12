using FluentAssertions;
using Oefenpad.DTOs.Account;
using Oefenpad.Resources.Account;
using Oefenpad.Validation.Account;
using Xunit;

namespace Oefenpad.Tests.Account;

public class RegisterRequestValidatorTests
{
    private static RegisterRequest Valid() => new()
    {
        FirstName = "Sanne",
        LastName = "de Vries",
        Email = "sanne@example.nl",
        Password = "goedwachtwoord1",
        ConfirmPassword = "goedwachtwoord1",
        TermsAccepted = true,
        PreferredLanguageCode = "nl"
    };

    [Fact]
    public async Task Password_mismatch_is_reported_in_both_languages()
    {
        var request = Valid();
        request.ConfirmPassword = "iets-anders-1";

        var result = await new RegisterRequestValidator().ValidateAsync(request);

        result.IsValid.Should().BeFalse();
        var failure = result.Errors.Single(error => error.PropertyName == nameof(RegisterRequest.ConfirmPassword));
        failure.CustomState.Should().Be(AccountMessages.Validatie.WachtwoordKomtNietOvereen);
    }

    [Fact]
    public async Task Terms_must_be_accepted()
    {
        var request = Valid();
        request.TermsAccepted = false;

        var result = await new RegisterRequestValidator().ValidateAsync(request);

        result.IsValid.Should().BeFalse();
        result.Errors.Select(error => error.CustomState)
            .Should().Contain(AccountMessages.Validatie.VoorwaardenNodig);
    }

    [Fact]
    public async Task Password_needs_ten_characters_and_a_digit()
    {
        var request = Valid();
        request.Password = "kort";
        request.ConfirmPassword = "kort";

        var result = await new RegisterRequestValidator().ValidateAsync(request);

        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(error => error.PropertyName == nameof(RegisterRequest.Password));
    }

    [Fact]
    public async Task A_complete_request_is_valid()
    {
        var result = await new RegisterRequestValidator().ValidateAsync(Valid());

        result.IsValid.Should().BeTrue();
    }
}

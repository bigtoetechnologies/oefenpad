using System.Net;
using System.Net.Mail;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Oefenpad.Contracts.Interfaces.Services;
using Oefenpad.Contracts.Options;
using Oefenpad.DTOs;

namespace Oefenpad.Services.Email;

/// <summary>
/// Development sink: writes each message as an .html file so it can be opened in a browser.
/// Nothing leaves the machine, and the confirmation link is readable from the file.
/// </summary>
public class FileEmailDispatcher(
    IOptions<EmailOptions> options,
    IHostEnvironment environment,
    ILogger<FileEmailDispatcher> logger) : IEmailDispatcher
{
    public async Task SendAsync(EmailMessage message, CancellationToken cancellationToken = default)
    {
        var sink = options.Value.SinkPath;
        if (string.IsNullOrWhiteSpace(sink))
            sink = "email-sink";

        if (!Path.IsPathRooted(sink))
            sink = Path.Combine(environment.ContentRootPath, sink);

        Directory.CreateDirectory(sink);

        var safeRecipient = string.Concat(message.To.Select(c => Path.GetInvalidFileNameChars().Contains(c) ? '-' : c));
        var file = Path.Combine(
            sink,
            $"{DateTime.UtcNow:yyyyMMdd-HHmmss}-{safeRecipient}-{Guid.NewGuid():N}.html");

        await File.WriteAllTextAsync(file, message.Html, cancellationToken);

        logger.LogInformation(
            "E-mail for {Recipient} written to {File}. Subject: {Subject} / {SubjectEn}",
            message.To, file, message.Subject.Nl, message.Subject.En);
    }
}

/// <summary>
/// SMTP transport, selected only when <c>Email:SmtpHost</c> is configured. Development uses
/// <see cref="FileEmailDispatcher"/> instead.
/// </summary>
public class SmtpEmailDispatcher(
    IOptions<EmailOptions> options,
    ILogger<SmtpEmailDispatcher> logger) : IEmailDispatcher
{
    public async Task SendAsync(EmailMessage message, CancellationToken cancellationToken = default)
    {
        var settings = options.Value;

        using var client = new SmtpClient(settings.SmtpHost, settings.SmtpPort)
        {
            EnableSsl = settings.SmtpUseSsl
        };

        if (!string.IsNullOrWhiteSpace(settings.SmtpUser))
            client.Credentials = new NetworkCredential(settings.SmtpUser, settings.SmtpPassword);

        using var mail = new MailMessage
        {
            From = new MailAddress(settings.FromAddress, settings.FromName),
            Subject = message.Subject.Nl,
            Body = message.Html,
            IsBodyHtml = true
        };
        mail.To.Add(message.To);

        await client.SendMailAsync(mail, cancellationToken);

        logger.LogInformation("E-mail for {Recipient} sent over SMTP.", message.To);
    }
}

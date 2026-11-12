using System.Text;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc.Rendering;
using Oefenpad.DTOs;

namespace Oefenpad.WebUI.Helpers;

/// <summary>
/// Renders both languages in the markup, so the CSS <c>html[data-taal]</c> switch works
/// without the server knowing which language the visitor chose.
/// </summary>
public static class BilingualHtml
{
    public static IHtmlContent Beide(this IHtmlHelper html, string nl, string en)
        => new HtmlString(
            $"<span lang=\"nl\">{HtmlEncoder.Default.Encode(nl)}</span>" +
            $"<span lang=\"en\">{HtmlEncoder.Default.Encode(en)}</span>");

    /// <summary>
    /// A message block. <paramref name="soort"/> is "fout" for errors, "goed" for success
    /// and "let-op" for warnings.
    /// </summary>
    public static IHtmlContent Meldingen(
        this IHtmlHelper html,
        IEnumerable<Bilingual>? berichten,
        string soort = "fout")
    {
        var lijst = berichten?.ToList() ?? [];
        if (lijst.Count == 0)
            return HtmlString.Empty;

        var builder = new StringBuilder();
        builder.Append("<div class=\"melding ").Append(soort).Append("\" role=\"")
            .Append(soort == "fout" ? "alert" : "status").Append("\">");

        foreach (var bericht in lijst)
        {
            builder.Append("<p><span lang=\"nl\">").Append(HtmlEncoder.Default.Encode(bericht.Nl))
                .Append("</span><span lang=\"en\">").Append(HtmlEncoder.Default.Encode(bericht.En))
                .Append("</span></p>");
        }

        builder.Append("</div>");
        return new HtmlString(builder.ToString());
    }
}

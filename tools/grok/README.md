# Grok drawing tool

`grok.py` runs a Voorzetselpaden batch in Grok from the command line: open a
chat, attach the style references, paste the prompt, send, wait, and download
the zip. It drives a real Chrome over the DevTools protocol, so Grok's own
sign-in is used and nothing is scraped.

## Before the first batch

Chrome must run with a debugging port and a profile that is signed in to
grok.com. It cannot be your everyday profile: Chrome refuses a debugging port on
the default profile, and the profile holds every site you are signed in to.

```sh
google-chrome --user-data-dir=<profile-folder> --remote-debugging-port=9333 \
  --no-first-run https://grok.com/
```

The first time, sign in to Grok in that window. The login stays in the profile
folder, so closing Chrome does not sign you out; deleting the folder does. A
folder under `/tmp` is wiped on reboot.

Anything on this machine can drive a browser with an open debugging port, so
close it when you are not drawing. A different port goes in `GROK_CDP_PORT`.

The tool needs Python 3 and `websocket-client` (`python3-websocket` on Debian
and Mint).

## One batch

A batch is one chunk: every card of one verb with its preposition, as the band
page in `Docs/voorzetselpaden/<band>.html` shows it now.

```sh
tools/grok/grok.py prompt a0 "drinken uit" > prompt.txt
tools/grok/grok.py new
tools/grok/grok.py compose prompt.txt     # attaches the style-a references
tools/grok/grok.py send                   # prints the chat URL
tools/grok/grok.py wait oefenpad-a0-drinken-uit.zip
tools/grok/grok.py download oefenpad-a0-drinken-uit.zip <folder>
```

`prompt` reads the cards from the page at the moment it runs and puts
`base-prompt.txt` in front of them, so the prompt always matches the page. Use
`--only <id> …` to redraw some cards of a chunk, and `--zip <name>` to give a
retry its own zip name.

`compose` attaches the three files in
`assets/verb-propositions/referenceimages/style-a/` unless you name others, and
types nothing until all three have uploaded. `wait` checks every 30 seconds and
gives up after 45 minutes.

Unzip into a folder of its own, review, and only then copy the images that pass
into `assets/verb-propositions/incoming/`. How to review is in
`Docs/game-art.md` under *Voorzetselpaden uses style A*.

## What breaks it

| Symptom | Cause |
|---|---|
| `no grok.com tab open` | Chrome is not running with the port, or no tab is on grok.com |
| `references did not finish uploading` | Grok's upload was slow or failed; run `new` and `compose` again |
| `wait` never finishes | Grok returned the images inline instead of a zip. The prompt's DELIVERY lines name the zip and list every file; if Grok ignored them, ask in the chat for the zip |
| `no download button` | The zip name differs from the one in DELIVERY; check the chat |

Inline images cannot be downloaded by this tool: Grok's image URLs refuse any
request but the page's own, and the canvas is locked. Ask for the zip instead.

The tool reads Grok's page by its button labels (`Send`, `Stop`,
`Download <file>`, `Remove <file>`). If Grok renames them, `eval` is the way to
look: `grok.py eval "document.title"` runs any JavaScript in the Grok tab.

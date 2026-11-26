#!/usr/bin/env python3
"""Drive a Grok chat in a locally running Chrome over the DevTools protocol.

Chrome must already be running with --remote-debugging-port (default 9333) and
be signed in to grok.com; see README.md. Needs the websocket-client package.

    grok.py prompt BAND CHUNK [--only ID ...]    print a batch prompt built from the current cards
    grok.py verbprompt PAGE... [--batch N] [--size K] [--follow|--refresh] [--avoid]\n                                               prompt for one batch of werkwoorden cards (--follow: no style text)
    grok.py new                                  open a fresh Grok chat
    grok.py compose PROMPT [REF ...] [--no-refs] attach references (unless --no-refs), type the prompt
    grok.py send                                 press Send, print the chat URL
    grok.py wait ZIPNAME [--timeout S]           wait until that zip can be downloaded
    grok.py download ZIPNAME DEST                download the zip into DEST
    grok.py usage                                print the weekly usage from Settings > Usage
    grok.py eval JS                              evaluate JavaScript in the Grok tab

compose without REF attaches the three files in
assets/verb-propositions/referenceimages/style-a/.
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path
from websocket import create_connection

ROOT = Path(__file__).resolve().parents[2]
STYLE_A = ROOT / "assets/verb-propositions/referenceimages/style-a"
PORT = int(os.environ.get("GROK_CDP_PORT", "9333"))


class Tab:
    def __init__(self, timeout=120):
        tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
        pages = [t for t in tabs if t["type"] == "page" and "grok.com" in t.get("url", "")]
        if not pages:
            sys.exit("no grok.com tab open in the debugging Chrome")
        self.ws = create_connection(pages[0]["webSocketDebuggerUrl"], timeout=timeout,
                                    suppress_origin=True)
        self.n = 0

    def call(self, method, params=None):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.n:
                if "error" in r:
                    raise RuntimeError(r["error"])
                return r.get("result", {})

    def js(self, expr):
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True,
                                           "awaitPromise": True})
        return r.get("result", {}).get("value")


COMPOSER = "[...document.querySelectorAll('[contenteditable=true]')].find(e=>e.offsetParent!==null)"


def labels(tab):
    return tab.js("JSON.stringify([...document.querySelectorAll('[aria-label]')]"
                  ".map(e=>e.getAttribute('aria-label')))")


def cmd_prompt(a):
    """Base prompt plus the chunk's cards, read from the band page as it is now."""
    import subprocess, tempfile, re as _re
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        subprocess.run([sys.executable, "-I", str(ROOT / "tools/prepositions-pages.py"), "read",
                        "--out", tmp.name], check=True, capture_output=True)
        recs = json.load(open(tmp.name, encoding="utf-8"))
    page = a.band if a.band.endswith(".html") else a.band + ".html"
    cards = [r for r in recs if r["page"] == page and r.get("chunk") == a.chunk]
    if a.only:
        cards = [r for r in cards if r["id"] in a.only]
        missing = set(a.only) - {r["id"] for r in cards}
        if missing:
            sys.exit("not cards of that chunk: " + ", ".join(sorted(missing)))
    if not cards:
        sys.exit(f"no cards for chunk {a.chunk!r} on {page}")
    gloss = next((r["gloss"] for r in recs if r["page"] == page and r.get("chunk") == a.chunk
                  and r.get("gloss")), "")

    def sentence(v):
        v = v.strip()
        v = v[0].upper() + v[1:]
        return v if v[-1] in ".!?" else v + "."

    scenes = []
    for r in cards:
        lines = [f"{r['id']}.png — {a.chunk}" + (f" ({gloss})" if gloss else ""),
                 "Scene: " + sentence(r["scene"])]
        if r.get("must"):
            lines.append("Must read: " + r["must"])
        if r.get("avoid"):
            lines.append("Avoid: " + r["avoid"])
        scenes.append("\n".join(lines))
    band = page[:-5]
    zipname = a.zip or f"oefenpad-{band}-{_re.sub(r'[^a-z0-9]+', '-', a.chunk.lower()).strip('-')}.zip"
    base = (ROOT / "Docs/voorzetselpaden/base-prompt.txt").read_text(encoding="utf-8").rstrip()
    print(base + "\n\nTHE SCENES\n" + "\n\n".join(scenes) +
          f"\n\nDELIVERY\nReturn one zip named {zipname} containing exactly these files and nothing else:\n"
          + ", ".join(r["id"] + ".png" for r in cards) + "\nAttach the zip to your reply.")


def cmd_new(a):
    t = Tab()
    t.call("Page.navigate", {"url": "https://grok.com/"})
    time.sleep(6)
    print(t.js("location.href"))


def cmd_compose(a):
    refs = [] if a.no_refs else ([Path(r).resolve() for r in a.refs] or sorted(
        p for p in STYLE_A.glob("*.png")))
    for r in refs:
        if not r.is_file():
            sys.exit(f"missing reference: {r}")
    text = Path(a.prompt).read_text(encoding="utf-8")
    t = Tab()
    if refs:
        root = t.call("DOM.getDocument", {"depth": 1})["root"]["nodeId"]
        node = t.call("DOM.querySelector", {"nodeId": root, "selector": "input[type=file]"})["nodeId"]
        t.call("DOM.setFileInputFiles", {"files": [str(r) for r in refs], "nodeId": node})
        want = {f"Remove {r.name}" for r in refs}
        for _ in range(40):
            time.sleep(2)
            if want <= set(json.loads(labels(t))):
                break
        else:
            sys.exit("references did not finish uploading; nothing typed")
    t.js(f"(()=>{{{COMPOSER}.focus();return 1}})()")
    time.sleep(0.5)
    t.call("Input.insertText", {"text": text})
    time.sleep(1)
    print("attached:", ", ".join(r.name for r in refs))
    print("composer chars:", t.js(f"{COMPOSER}.innerText.length"), "of", len(text))


def cmd_send(a):
    t = Tab()
    ok = t.js("(()=>{const b=[...document.querySelectorAll('button')]"
              ".find(x=>(x.getAttribute('aria-label')||'').trim()==='Send');"
              "if(!b)return false;b.click();return true})()")
    if not ok:
        sys.exit("no Send button")
    time.sleep(8)
    print(t.js("location.href"))


def cmd_wait(a):
    t = Tab(timeout=60)
    start = time.time()
    while time.time() - start < a.timeout:
        try:
            ready = f"Download {a.zip}" in json.loads(labels(t))
            busy = "Stop" in json.loads(labels(t))
        except Exception:
            time.sleep(20)
            t = Tab(timeout=60)
            continue
        print(int(time.time() - start), "s  zip ready" if ready else "s  waiting",
              "(busy)" if busy else "", flush=True)
        if ready and not busy:
            print("DONE")
            return
        time.sleep(30)
    sys.exit("TIMEOUT")


def cmd_download(a):
    dest = Path(a.dest).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    t = Tab()
    t.call("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(dest),
                                           "eventsEnabled": True})
    before = set(os.listdir(dest))
    ok = t.js("(()=>{const e=[...document.querySelectorAll('[aria-label]')]"
              f".find(x=>x.getAttribute('aria-label')==={json.dumps('Download ' + a.zip)});"
              "if(!e)return false;e.click();return true})()")
    if not ok:
        sys.exit(f"no download button for {a.zip}")
    for _ in range(60):
        time.sleep(1)
        new = [f for f in os.listdir(dest) if f not in before and not f.endswith(".crdownload")]
        if new:
            print("downloaded:", *(dest / f for f in new))
            return
    sys.exit("download did not finish in 60 s")


def cmd_usage(a):
    """Read the weekly usage text from Grok's Settings > Usage (opens and leaves the dialog open)."""
    t = Tab()
    t.js("(()=>{const b=[...document.querySelectorAll('button')].find(x=>(x.getAttribute('aria-label')||'').startsWith('Account menu'));b&&b.click()})()")
    time.sleep(2)
    t.js("(()=>{const b=[...document.querySelectorAll('[role=menuitem],[data-radix-collection-item]')].find(x=>(x.innerText||'').trim()==='Settings');b&&b.click()})()")
    time.sleep(2)
    t.js("(()=>{const b=[...document.querySelectorAll('[role=dialog] button,[role=tab]')].find(x=>(x.innerText||'').trim()==='Usage');b&&b.click()})()")
    time.sleep(3)
    txt = t.js("(()=>{const d=document.querySelector('[role=dialog]');return d?d.innerText:''})()") or ""
    import re as _re
    m = _re.search(r"Weekly SuperGrok Limit\s*\n?\s*(\d+)%.*?Resets ([^\n]+).*?Imagine\s*\n?\s*(\d+)%.*?Chat\s*\n?\s*(\d+)%", txt, flags=_re.S)
    print(f"weekly {m.group(1)}% used (imagine {m.group(3)}%, chat {m.group(4)}%), resets {m.group(2)}" if m else txt[:400])
    t.call("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
    t.call("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})


def cmd_eval(a):
    print(json.dumps(Tab().js(a.js), ensure_ascii=False))


def cmd_verbprompt(a):
    """Prompt for one batch of werkwoorden cards from one or more Docs/werkwoorden band pages.

    Default: full style text (first message of a chat). --follow: no style text, for later batches
    in the same chat. --refresh: short style lock. Avoid lines only with --avoid (retries).
    """
    import re as _re, html as _html
    cards = []
    for pg in a.pages:
        page = ROOT / "Docs/werkwoorden" / (pg.removesuffix(".html") + ".html")
        text = page.read_text(encoding="utf-8")
        for m in _re.finditer(r'<article id="([^"]+)".*?</article>', text, flags=_re.S):
            blk = m.group(0)
            if 'class="geenbeeld"' not in blk and not a.only:      # already drawn; --only redraws
                continue
            dd = {k: _html.unescape(v).strip() for k, v in _re.findall(r'<dd class="(\w+)">(.*?)</dd>', blk, flags=_re.S)}
            verb = _html.unescape(_re.search(r'<h3 class="chunk">(.*?)</h3>', blk).group(1))
            gloss = _html.unescape(_re.search(r'<p class="gloss">(.*?)</p>', blk).group(1))
            cards.append({"id": m.group(1), "verb": verb, "gloss": gloss, **dd})
    if a.only:
        cards = [c for c in cards if c["id"] in a.only]
    else:
        cards = [c for c in cards if c["id"] not in (a.skip or [])]
        cards = cards[(a.batch - 1) * a.size: a.batch * a.size]
    if not cards:
        sys.exit("no cards in that batch")
    def sentence(v):
        v = v[0].upper() + v[1:]
        return v if v[-1] in ".!?" else v + "."
    scenes = []
    for c in cards:
        lines = [f"{c['id']}.png — {c['verb']} ({c['gloss']})", f"Scene: {sentence(c['scene'])}"]
        if c.get("must"):
            lines.append(f"Must read: {c['must']}")
        if a.avoid and c.get("avoid"):
            lines.append(f"Avoid: {c['avoid']}")
        scenes.append("\n".join(lines))
    tag = "+".join(p.removesuffix(".html") for p in a.pages)
    zipname = a.zip or f"oefenpad-ww-{tag}-{a.batch}.zip"
    d = ROOT / "Docs/werkwoorden"
    if a.follow:
        head = "Same style and rules as before, same attached references. Next batch, one drawing per scene."
    elif a.refresh:
        head = (d / "style-lock.txt").read_text(encoding="utf-8").rstrip()
    else:
        head = (d / "base-prompt.txt").read_text(encoding="utf-8").rstrip()
    print(head + "\n\nSCENES\n" + "\n\n".join(scenes) +
          f"\n\nOUTPUT\nOne zip named {zipname} with exactly: "
          + ", ".join(c["id"] + ".png" for c in cards) + ". Attach it to your reply.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt"); p.add_argument("band"); p.add_argument("chunk")
    p.add_argument("--only", nargs="+"); p.add_argument("--zip")
    p = sub.add_parser("verbprompt"); p.add_argument("pages", nargs="+"); p.add_argument("--batch", type=int, default=1)
    p.add_argument("--size", type=int, default=7); p.add_argument("--only", nargs="+"); p.add_argument("--zip")
    p.add_argument("--follow", action="store_true"); p.add_argument("--refresh", action="store_true")
    p.add_argument("--avoid", action="store_true")
    p.add_argument("--skip", nargs="+", help="card ids to leave out (retries exhausted)")
    sub.add_parser("new")
    p = sub.add_parser("compose"); p.add_argument("prompt"); p.add_argument("refs", nargs="*")
    p.add_argument("--no-refs", action="store_true", help="type only; references already in this chat")
    sub.add_parser("send")
    p = sub.add_parser("wait"); p.add_argument("zip"); p.add_argument("--timeout", type=int, default=2700)
    p = sub.add_parser("download"); p.add_argument("zip"); p.add_argument("dest")
    sub.add_parser("usage")
    p = sub.add_parser("eval"); p.add_argument("js")
    a = ap.parse_args()
    globals()["cmd_" + a.cmd](a)


if __name__ == "__main__":
    main()

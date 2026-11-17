import json, subprocess, time, urllib.request, shutil, base64
import websocket

URL = "file:///media/tony/Data/repos/oefenpad/tools/lexicon/index.html"
profile = "/tmp/cdp-test-profile"
shutil.rmtree(profile, ignore_errors=True)
chrome = subprocess.Popen(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
    "--remote-debugging-port=9334", "--remote-allow-origins=*",
    "--user-data-dir=" + profile, "--window-size=1400,1000", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
errors = []
try:
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9334/json")); break
        except Exception: time.sleep(0.2)
    ws = websocket.create_connection([t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"], timeout=25)
    mid = [0]
    def send(method, params=None):
        mid[0] += 1
        ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == mid[0]:
                return msg
            if msg.get("method") == "Runtime.exceptionThrown":
                errors.append(json.dumps(msg["params"])[:400])
            if msg.get("method") == "Log.entryAdded" and msg["params"]["entry"]["level"] == "error":
                errors.append(json.dumps(msg["params"])[:400])
    def ev(e):
        r = send("Runtime.evaluate", {"expression": e, "returnByValue": True})
        res = r.get("result", {})
        if res.get("exceptionDetails"):
            errors.append(json.dumps(res["exceptionDetails"])[:400])
        return res.get("result", {}).get("value")
    def shot(name, w=1400, h=1000):
        send("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False})
        time.sleep(0.6)
        data = send("Page.captureScreenshot", {"format": "png"})["result"]["data"]
        open(".shots/" + name, "wb").write(base64.b64decode(data))

    def tab(mode):
        ev("document.querySelector('[data-mode=%s]').click()" % mode)
    def type_search(text):
        ev("document.getElementById('search').value=" + json.dumps(text) +
           ";document.getElementById('search').dispatchEvent(new Event('input',{bubbles:true}));")
    def pick(mode, fkey, value):
        ev("(function(){var s=document.getElementById('f-%s-%s');s.value=%s;"
           "s.dispatchEvent(new Event('change',{bubbles:true}));})()" % (mode, fkey, json.dumps(value)))
    def count(): return ev("document.getElementById('count').textContent")
    def first(): return ev("document.querySelector('tbody tr td.nl') && document.querySelector('tbody tr td.nl').textContent")
    def nrows(): return ev("document.querySelectorAll('tbody tr').length")

    send("Runtime.enable"); send("Log.enable"); send("Page.enable")
    send("Page.navigate", {"url": URL})
    time.sleep(3)

    print("T1 initial:", count(), "| rows", nrows(), "| first", first())
    type_search("sfeer");     print("T2 sfeer:", count(), "| first", first())
    type_search("SFEER");     print("T3 SFEER:", count())
    type_search("cafe");      print("T4 cafe (no accent):", count(), "|", first())
    type_search("schon");     print("T5 schon:", count())
    type_search("eten");      print("T6 eten in gloss:", count(), "| first", first())
    shot("t6-search-eten.png")
    type_search("")
    print("T7 thema=Algemeen count:", ev("[...document.querySelectorAll('#f-master-thema option')].find(o=>o.value==='algemeen').textContent"))
    pick("master", "pos", "verb");       print("T8 pos=verb:", count())
    pick("master", "herkomst", "spel:*"); print("T9 +spel:*:", count())
    pick("master", "pos", "");           print("T10 spel:* only:", count())
    pick("master", "herkomst", "spel:art"); print("T11 spel:art:", count())
    pick("master", "herkomst", "bijlage8"); print("T12 bijlage8:", count())
    print("T13 herkomst options:", ev("document.querySelectorAll('#f-master-herkomst option').length"),
          "| first opts:", ev("[...document.querySelectorAll('#f-master-herkomst option')].slice(0,3).map(o=>o.textContent).join(' | ')"))
    ev("document.getElementById('reset').click()")
    print("T14 after reset:", count(), "| search box:", ev("JSON.stringify(document.getElementById('search').value)"),
          "| select:", ev("document.getElementById('f-master-herkomst').value"))
    ev("document.querySelectorAll('#thead-row th')[1].click()")
    a = first()
    ev("document.querySelectorAll('#thead-row th')[1].click()")
    print("T15 sort nl:", a, "->", first())
    ev("document.querySelectorAll('#thead-row th')[0].click()")
    print("T16 back to #:", first(), "| rows", nrows())
    ev("document.getElementById('more').click()")
    print("T17 show more:", nrows())
    print("T18 no-match message:", (type_search("zzzzqqq"), ev("getComputedStyle(document.getElementById('none')).display"))[-1])
    type_search("")
    tab("knm")
    print("T19 knm:", count(), "| rows", nrows(),
          "| meta:", ev("document.getElementById('meta').textContent"),
          "| blank themes:", ev("[...document.querySelectorAll('tbody tr')].filter(r=>r.querySelectorAll('td')[5].textContent.trim()==='—').length"),
          "| thema opts:", ev("[...document.querySelectorAll('#f-knm-thema option')].map(o=>o.textContent).join(' | ')"),
          "| prio opts:", ev("[...document.querySelectorAll('#f-knm-prioriteit option')].map(o=>o.textContent).join(' | ')"))
    print("T20 summary hidden on knm:", ev("getComputedStyle(document.getElementById('summary')).display"))
    shot("t20-knm.png")
    tab("kandidaten")
    print("T21 kandidaten:", count(), "| filters:", ev("[...document.querySelectorAll('#filters select')].map(s=>s.id).join(',')"))
    shot("t21-kandidaten.png")
    tab("master")
    shot("t22-master-1400.png")
    shot("t23-master-800.png", 800, 1000)
    print("T24 scrollWidth vs viewport @800:", ev("document.documentElement.scrollWidth + ' vs ' + window.innerWidth"))
    print("T25 summary themed:", ev("document.querySelector('.themed-note b').textContent"),
          "| details:", ev("document.querySelectorAll('.summary details').length"),
          "| open:", ev("document.querySelectorAll('.summary details[open]').length"))
    print("T26 themed list first 3:", ev("[...document.querySelectorAll('.summary details:last-of-type .kv')].slice(0,3).map(e=>e.textContent).join(' | ')"))
    print("T27 #1 row cells:", ev("[...document.querySelectorAll('tbody tr')[0].cells].map(c=>c.textContent).join(' | ')"))
    print("T28 row 8714 (quotes):", ev("document.querySelectorAll('#thead-row th')[0].click(), [1].map(()=>0), 0") )
    ev("(function(){var s=document.querySelectorAll('#thead-row th');return 0})()")
    print("T29 total width @1400:", ev("document.documentElement.scrollWidth + ' vs ' + window.innerWidth"))
finally:
    chrome.terminate()

print("JS ERRORS:", len(errors))
for e in errors[:10]:
    print(" ", e)

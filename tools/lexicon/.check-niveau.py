"""Assert the filter counts add up. Throwaway harness, like .cdp-test.py.

Scenario from the owner's report: domein = Animals, thema = algemeen, every
prioriteit. Reads the rendered <select> options and checks that, for each
filter, the option counts sum to the filter's own "all (N)".
"""

import json
import os
import shutil
import subprocess
import time
import urllib.request

import websocket

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "file://" + os.path.join(HERE, "index.html") + "?v=" + str(int(time.time()))
profile = "/tmp/cdp-niveau-profile"
shutil.rmtree(profile, ignore_errors=True)
shots = os.path.join(HERE, ".shots")
os.makedirs(shots, exist_ok=True)

chrome = subprocess.Popen(
    ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
     "--remote-debugging-port=9335", "--remote-allow-origins=*",
     "--user-data-dir=" + profile, "--window-size=1500,1100", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

errors = []
try:
    tabs = None
    for _ in range(60):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9335/json"))
            break
        except Exception:
            time.sleep(0.2)
    ws = websocket.create_connection(
        [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"], timeout=30)
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

    def ev(expr):
        r = send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        res = r.get("result", {})
        if res.get("exceptionDetails"):
            errors.append(json.dumps(res["exceptionDetails"])[:400])
        return res.get("result", {}).get("value")

    def pick(fkey, value):
        ev("(function(){var s=document.getElementById('f-master-%s');"
           "s.value=%s;s.dispatchEvent(new Event('change',{bubbles:true}));})()"
           % (fkey, json.dumps(value)))
        time.sleep(0.35)

    def options(fkey):
        return ev("(function(){var s=document.getElementById('f-master-%s');"
                  "var o=[];for(var i=0;i<s.options.length;i++)"
                  "o.push([s.options[i].value,Number((s.options[i].textContent.match(/\\((\\d[\\d,]*)\\)/)||[0,'-1'])[1].replace(/,/g,''))]);"
                  "return o;})()" % fkey)

    send("Runtime.enable")
    send("Log.enable")
    send("Page.enable")
    send("Page.navigate", {"url": URL})
    time.sleep(3.5)

    pick("domein", "Animals")
    pick("thema", "algemeen")

    count = ev("document.getElementById('count').textContent")
    print("showing:", count)

    ok = True
    # herkomst is multi-valued: one row can be "bijlage8;spel:movies", so its
    # options deliberately sum higher than "all". Every other facet partitions.
    multi = {"herkomst"}
    for fkey in ("pos", "thema", "domein", "prioriteit", "niveau", "trede", "herkomst"):
        opts = options(fkey)
        all_n = [n for v, n in opts if v == ""][0]
        parts = [(v, n) for v, n in opts if v != ""]
        total = sum(n for _, n in parts)
        if fkey in multi:
            flag = "n/a"
        else:
            flag = "OK " if total == all_n else "BAD"
            if total != all_n:
                ok = False
        print(f"{flag} {fkey:11} all={all_n:5}  options={len(parts):3}  sum={total:5}")
        if fkey in ("niveau", "trede"):
            print("      " + ", ".join(f"{v}={n}" for v, n in parts))

    send("Emulation.setDeviceMetricsOverride",
         {"width": 1500, "height": 1100, "deviceScaleFactor": 1, "mobile": False})
    time.sleep(0.5)
    data = send("Page.captureScreenshot", {"format": "png"})["result"]["data"]
    import base64
    with open(os.path.join(shots, "niveau-filter.png"), "wb") as fh:
        fh.write(base64.b64decode(data))

    print("errors:", errors or "none")
    print("RESULT:", "counts add up" if ok else "MISMATCH")
finally:
    chrome.terminate()

#!/usr/bin/env python3
"""Smoke-test account progress on a running Oefenpad server.

Usage:
    ASPNETCORE_ENVIRONMENT=Development dotnet run \
        --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098
    python3 tools/smoke-game-progress.py [base-url]

Defaults to http://127.0.0.1:8098. The server must run in Development: the
confirmation link is rendered on the registration response only there.

It registers a throwaway account, confirms and signs in, then checks the
thing that matters: a saved Word Search round comes back with the grid and
the found word's cells, and a finished preposition level is recorded with
the score the player reached. Prints one line per check and exits non-zero
on the first failure.
"""

import html
import http.cookiejar
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8098"
DB = pathlib.Path(__file__).resolve().parent.parent / "server/Oefenpad.WebUI/oefenpad.db"
TOKEN = re.compile(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"')
EMAIL = f"speler-{time.time_ns()}@example.nl"
PASSWORD = "goedwachtwoord1"


class Session:
    def __init__(self):
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get(self, path, expect=200):
        return self._read(self.opener.open(BASE + path), expect)

    def post_form(self, path, fields):
        data = urllib.parse.urlencode(fields).encode()
        request = urllib.request.Request(
            BASE + path, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        return self._read(self.opener.open(request))

    def get_json(self, path):
        return json.loads(self.get(path))

    def post_json(self, path, body):
        data = json.dumps(body).encode()
        request = urllib.request.Request(
            BASE + path, data=data,
            headers={"Content-Type": "application/json"})
        return json.loads(self._read(self.opener.open(request)))

    @staticmethod
    def _read(response, expect=200):
        with response:
            if response.status != expect:
                raise AssertionError(f"{response.status} != {expect}")
            return response.read().decode("utf-8")


def token(page):
    match = TOKEN.search(page)
    if not match:
        raise SystemExit("no antiforgery token in the page; is the server running?")
    return match.group(1)


def check(label, condition, detail=""):
    print(("ok   " if condition else "FAIL ") + label + (" — " + detail if detail else ""))
    if not condition:
        sys.exit(1)


# ---------------------------------------------------------------- anonymous
guest = Session()
check("guest has no saved round",
      guest.get_json("/api/games/wordsearch/saved") == {"saved": False})
check("guest progress is empty",
      guest.get_json("/api/games/prepositions/progress") == {"levels": {}})

# ------------------------------------------------------ register and confirm
player = Session()
page = player.get("/Account/Registreren")
page = player.post_form("/Account/Registreren", {
    "__RequestVerificationToken": token(page),
    "Invoer.FirstName": "Test",
    "Invoer.LastName": "Speler",
    "Invoer.Email": EMAIL,
    "Invoer.Password": PASSWORD,
    "Invoer.ConfirmPassword": PASSWORD,
    "Invoer.PreferredLanguageCode": "nl",
    "Invoer.TermsAccepted": "true",
})
link = re.search(r'href="([^"]*Account/Bevestig[^"]*)"', page)
check("registration shows the development confirmation link", link is not None)
parsed = urllib.parse.urlsplit(html.unescape(link.group(1)))
player.get(parsed.path + ("?" + parsed.query if parsed.query else ""))

# ---------------------------------------------------------------- sign in
page = player.get("/Account/Inloggen")
player.post_form("/Account/Inloggen", {
    "__RequestVerificationToken": token(page),
    "Invoer.Email": EMAIL,
    "Invoer.Password": PASSWORD,
    "Invoer.RememberMe": "false",
})

# ------------------------------------------ word search: start, save, resume
round = player.post_json("/api/games/wordsearch/rounds",
                         {"category": "animals", "difficulty": "easy"})
check("word search starts", "roundId" in round and round["view"]["words"])
grid = json.dumps(round["view"]["grid"])

saved = player.get_json("/api/games/wordsearch/saved")
check("start was saved to the account", saved.get("saved") is True)
check("saved round is the same grid", json.dumps(saved["view"]["grid"]) == grid)

hinted = player.post_json(
    f"/api/games/wordsearch/rounds/{round['roundId']}/moves", {"action": "hint"})
hint = hinted["view"]["hint"]
first, last = hint["cells"][0], hint["cells"][-1]
selected = player.post_json(
    f"/api/games/wordsearch/rounds/{round['roundId']}/moves",
    {"action": "select", "r1": first["r"], "c1": first["c"],
     "r2": last["r"], "c2": last["c"]})
check("hinted word is found", selected["correct"] is True)

saved = player.get_json("/api/games/wordsearch/saved")
check("resume keeps the found word",
      saved["view"]["found"][hint["index"]] is True)
check("resume carries only the found word's cells",
      list(saved.get("resume", {}).get("placements", {}).keys()) == [str(hint["index"])])

check("resumed round is playable",
      player.post_json(f"/api/games/wordsearch/rounds/{saved['roundId']}/moves",
                       {"action": "hint"})["view"].get("hint") is not None)

# ------------------------------------ prepositions: finish levels, gate the rest
levels = player.get_json("/api/games/prepositions/options")["levels"]

check("a signed-in learner with nothing finished is gated on progress",
      levels[3]["locked"] and levels[3]["lockReason"] == "progress")


def play(level_id):
    start = player.post_json("/api/games/prepositions/rounds", {"level": level_id})
    view = start["view"]
    round_id = start["roundId"]
    for _ in range(200):
        if view.get("done"):
            return view

        if view["phase"] == "question" and view["kind"] != "discover":
            content = view["content"]
            if view["kind"] == "choose":
                action = {"action": "choose", "scene": content["options"][0]["id"]}
            elif view["kind"] == "trueFalse":
                action = {"action": "trueFalse", "answer": True}
            else:
                action = {"action": "build", "tiles": [t["id"] for t in content["tiles"]]}
        else:
            action = {"action": "next"}

        view = player.post_json(
            f"/api/games/prepositions/rounds/{round_id}/moves", action)["view"]
    raise SystemExit("prepositions round did not finish")


finished = {}
for level in levels[:3]:
    finished[level["id"]] = play(level["id"])

level_id = levels[0]["id"]
view = finished[level_id]
check("level finishes", view.get("done") is True)
check("finished level has a score", view.get("total", 0) > 0)

progress = player.get_json("/api/games/prepositions/progress")["levels"]
check("finished level is recorded", level_id in progress)
check("recorded score matches", progress[level_id]["total"] == view["total"],
      f"{progress[level_id]} vs {view}")
check("finishing clears the saved round",
      player.get_json("/api/games/prepositions/saved") == {"saved": False})

levels = player.get_json("/api/games/prepositions/options")["levels"]
check("finishing the third free level opens the fourth", not levels[3]["locked"])
check("the fifth still waits for the fourth",
      levels[4]["locked"] and levels[4]["lockReason"] == "progress")
check("the fourth level now starts",
      "roundId" in player.post_json("/api/games/prepositions/rounds", {"level": levels[3]["id"]}))

# ----------------------------------------- the database holds what the API said
db = sqlite3.connect(DB)
saves = db.execute(
    "select count(*) from GameSaves s join AspNetUsers u on u.Id = s.ApplicationUserId "
    "where u.Email = ?", (EMAIL,)).fetchone()[0]
level_rows = db.execute(
    "select count(*) from GameLevelProgress p join AspNetUsers u on u.Id = p.ApplicationUserId "
    "where u.Email = ?", (EMAIL,)).fetchone()[0]
check("a saved round row per started game", saves == 2, f"{saves} rows")
check("three level progress rows for the player", level_rows == 3, f"{level_rows} rows")

print(f"\naccount: {EMAIL}")
print(f"level {level_id}: {view.get('correct')} / {view.get('total')}")
print("all checks passed")

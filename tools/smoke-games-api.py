#!/usr/bin/env python3
"""Smoke-test the game API on a running Oefenpad server.

Usage:
    python3 tools/smoke-games-api.py [base-url]

Defaults to http://127.0.0.1:8098. Prints one line per check and exits
non-zero on the first failure.
"""

import json
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8098"
GAMES = "/api/games"


def call(method, path, body=None, expect=200):
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            payload = response.read().decode()
    except urllib.error.HTTPError as error:
        status = error.code
        payload = error.read().decode()

    if status != expect:
        raise AssertionError(f"{method} {path}: {status} != {expect}: {payload}")
    return json.loads(payload) if payload else None


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    print("ok  ", label)


def start(game, body):
    return call("POST", f"{GAMES}/{game}/rounds", body)


def move(game, round_id, body):
    return call("POST", f"{GAMES}/{game}/rounds/{round_id}/moves", body)


def assert_no_answers(view, forbidden):
    text = json.dumps(view)
    for value in forbidden:
        if value and value in text:
            raise AssertionError(f"view leaks {value!r}: {text[:300]}")


# ---------------------------------------------------------------- registry
games = call("GET", GAMES)
check("all seven games are registered", set(games["games"]) == {
    "hangman", "matching", "memory", "prepositions", "verbs", "storymachine", "wordsearch"
})

# ------------------------------------------------------------ prepositions
options = call("GET", f"{GAMES}/prepositions/options")
check("prepositions offers ninety-six levels", len(options["levels"]) == 96)
check("prepositions options carry no frame phrases",
      all(" \u00b7 " not in (level.get("subtitle") or "") for level in options["levels"]))
check("a0 levels are free for a guest",
      all(not level["locked"] for level in options["levels"] if level.get("band") == "a0"))
check("a1 and a2 levels need an account",
      all(level["locked"] and level["lockReason"] == "account"
          for level in options["levels"]
          if level.get("band") in ("a1", "a2", "a2-pairs")))

# A start that did not come from the level list must still be refused.
locked = next(level for level in options["levels"] if level["locked"])
call("POST", f"{GAMES}/prepositions/rounds", {"level": locked["id"]}, expect=403)

# This free level is the one a0 chunk with a contrast partner, so the
# true/false and concept steps are exercised too.
started = start("prepositions", {"level": "stappen-uit"})
round_id = started["roundId"]
view = started["view"]
check("prepositions opens on discover", view["kind"] == "discover")
check("discover view carries only the current card",
      json.dumps(view).count('"sentence"') == 1)

steps = 0
concept_answered = False
while steps < 80:
    steps += 1
    kind = view["kind"]
    phase = view["phase"]

    if phase == "feedback":
        concept = view["feedback"].get("concept")
        if concept and concept.get("answer") is None:
            view = move("prepositions", round_id, {"action": "concept", "answer": True})["view"]
            concept_answered = True
            continue
        result = move("prepositions", round_id, {"action": "next"})
        if result.get("done"):
            view = result["view"]
            break
        view = result["view"]
        continue

    if kind == "discover":
        result = move("prepositions", round_id, {"action": "next"})
    elif kind == "choose":
        scene = view["content"]["options"][1]["id"]
        result = move("prepositions", round_id, {"action": "choose", "scene": scene})
    elif kind == "trueFalse":
        result = move("prepositions", round_id, {"action": "trueFalse", "answer": False})
    elif kind == "build":
        tiles = view["content"]["tiles"]
        result = move("prepositions", round_id, {"action": "build", "tiles": [t["id"] for t in tiles]})
    else:
        raise AssertionError(f"unknown step {kind}")

    check(f"prepositions step {kind} answered",
          kind == "discover" or result["view"]["phase"] == "feedback")
    view = result["view"]

check("prepositions reached the end", view.get("done") is True, )
check("prepositions scored every step", view["total"] >= 4)
check("a concept question was offered", concept_answered)

# ------------------------------------------------------------------- verbs
options = call("GET", f"{GAMES}/verbs/options")
check("verbs offers twenty-two levels", len(options["levels"]) == 22)
check("verbs options carry a band", all(level.get("band") for level in options["levels"]))

started = start("verbs", {"level": "a0-1"})
round_id = started["roundId"]
view = started["view"]
check("verbs opens on discover", view["kind"] == "discover")
check("verbs discover card carries a verb and a picture",
      bool(view["content"]["card"]["verb"]) and bool(view["content"]["card"]["image"]["url"]))

done = False
while not done:
    if view["kind"] == "discover" or view.get("phase") == "feedback":
        result = move("verbs", round_id, {"action": "next"})
    else:
        option = view["content"]["options"][0]["id"]
        result = move("verbs", round_id, {"action": "choose", "scene": option})
        check("verbs judges a choice", result["correct"] in (True, False))
    view = result["view"]
    done = result.get("done") is True

check("verbs reaches the end", done)
check("verbs scores every verb", view["total"] >= 4)

# ------------------------------------------------------------------ memory
options = call("GET", f"{GAMES}/memory/options")
check("memory has four levels", [l["id"] for l in options["levels"]] == ["4", "6", "8", "10"])

started = start("memory", {"category": "animals", "level": "4"})
round_id = started["roundId"]
view = started["view"]
check("memory deals 16 cards", len(view["cards"]) == 16)
check("memory hides every face", all(card["face"] is None for card in view["cards"]))

view = move("memory", round_id, {"action": "flip", "index": 0})["view"]
check("memory reveals the flipped card", view["cards"][0]["face"] is not None)
view = move("memory", round_id, {"action": "flip", "index": 1})["view"]
check("memory counts a move with two cards", view["moves"] == 1)
check("memory still hides the other cards", sum(1 for c in view["cards"] if c["face"]) <= 2)

# ---------------------------------------------------------------- matching
started = start("matching", {"category": "animals", "pairs": 4})
round_id = started["roundId"]
view = started["view"]
check("matching deals eight cards", len(view["cards"]) == 8)
check("matching has two panels", {c["side"] for c in view["cards"]} == {"word", "image"})

view = move("matching", round_id, {"action": "flip", "index": 0})["view"]
side = view["cards"][0]["side"]
same = next(c["index"] for c in view["cards"] if c["side"] == side and c["index"] != 0)
result = move("matching", round_id, {"action": "flip", "index": same})
check("matching refuses a same-panel pick", result.get("rejection") == "sameSide")

# ----------------------------------------------------------------- hangman
started = start("hangman", {"category": "animals", "difficulty": "easy"})
round_id = started["roundId"]
view = started["view"]
check("hangman hides the word", view["answer"] is None)
check("hangman sends a pattern", len(view["pattern"]) == view["wordLength"])

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    result = move("hangman", round_id, {"action": "guess", "letter": letter})
    view = result["view"]
    if result.get("done"):
        break
check("hangman finishes after guessing", view["status"] in ("won", "lost"))
check("hangman reveals the answer only at the end", view["answer"] is not None)

# ------------------------------------------------------------- storymachine
started = start("storymachine", {"count": 4, "language": "nl"})
round_id = started["roundId"]
view = started["view"]
check("storymachine shows four reels", len(view["reels"]) == 4)

held = move("storymachine", round_id, {"action": "hold", "index": 0, "held": True})["view"]
check("storymachine holds a reel", held["reels"][0]["held"] is True)

spun = move("storymachine", round_id, {"action": "spin"})
check("storymachine returns a strip per free reel", len(spun["view"]["strips"]) == 3)
check("storymachine keeps the held tile", spun["view"]["view"]["reels"][0]["tile"]["id"] == held["reels"][0]["tile"]["id"])
assert_no_answers(spun["view"], [])

# --------------------------------------------------------------- wordsearch
started = start("wordsearch", {"category": "animals", "difficulty": "beginner"})
round_id = started["roundId"]
view = started["view"]
check("wordsearch builds a 10x10 grid", len(view["grid"]) == 10 and len(view["grid"][0]) == 10)
check("wordsearch lists the words", len(view["words"]) > 0)
check("wordsearch hides the placements", "row" not in json.dumps(view["words"][:1]))

# A hint hands back the cells of one unfound word; selecting its two ends
# must be accepted by the hidden placement table.
hinted = move("wordsearch", round_id, {"action": "hint"})
cells = hinted["view"]["hint"]["cells"]
first, last = cells[0], cells[-1]
found = move("wordsearch", round_id, {
    "action": "select",
    "r1": first["r"], "c1": first["c"],
    "r2": last["r"], "c2": last["c"],
})
check("wordsearch accepts the hinted word", found.get("correct") is True)
check("wordsearch marks that word", found["view"]["view"]["found"][hinted["view"]["hint"]["index"]] is True)

# A line that is not a word must not score.
wrong = move("wordsearch", round_id, {
    "action": "select", "r1": 0, "c1": 0, "r2": 9, "c2": 9,
})
check("wordsearch rejects a non-word line", wrong.get("correct") is False)

print("\nall checks passed")

# Story Machine — the tile words

**Status: applied.** `server/Oefenpad.Resources/Games/Data/reels.json` holds these words as of 2026-11-04.
The "Was" column is the wording they replaced, kept so the change is readable.

Two tiles were dropped rather than reworded: `lost` (verdwaald) and `empty` (met lege
handen). Neither is a thing a picture can show. `het nest` and `de ster` took their
places, so every reel holds 12. Nothing in `script.js` assumes a reel length.

English nouns take `the` and verbs take `to`, so the column says which part of speech a
tile is. Verbs are infinitives in both languages (`to run` / `rennen`): a tile names an
action, and the player conjugates it aloud.

Drafted 2026-11-04. The rules this implements are in `story-machine.md` → **The words**.
The art each tile needs is in `story-machine-art.md`.

## What changes

| | Tiles |
|---|---|
| Article or preposition fixed, word unchanged | 57 |
| Word itself replaced | 13 |
| Dropped, and replaced by a new tile | 2 |
| **Total, before and after** | **72** |

## The reels

`id` is the art filename, per `story-machine.md`. A changed id means the art file is
named for the new word. Ids are not persisted anywhere, so renaming is safe.

### who — Who / Wie

| id | English | Was | Now | |
|---|---|---|---|---|
| `fox` | the fox | de vos | **de vos** |  |
| `owl` | the owl | de uil | **de uil** |  |
| `child` | the child | het kind | **het kind** |  |
| `robot` | the robot | de robot | **de robot** |  |
| `ghost` | the ghost | het spook | **het spook** |  |
| `king` | the king | de koning | **de koning** |  |
| `fish` | the fish | de vis | **de vis** |  |
| `dog` | the dog | de hond | **de hond** |  |
| `bird` | the bird | de vogel | **de vogel** |  |
| `granny` → `oma` | the grandmother | de oude vrouw | **de oma** | **new word** |
| `cat` | the cat | de kat | **de kat** |  |
| `bear` | the bear | de beer | **de beer** |  |

### does — Does what / Doet wat

| id | English | Was | Now | |
|---|---|---|---|---|
| `runs` | to run | rent | **rennen** |  |
| `hides` → `shelters` | to shelter | verstopt zich | **schuilen** | **new word** |
| `digs` | to dig | graaft | **graven** |  |
| `flies` | to fly | vliegt | **vliegen** |  |
| `sleeps` | to sleep | slaapt | **slapen** |  |
| `sings` | to sing | zingt | **zingen** |  |
| `steals` | to steal | steelt | **stelen** |  |
| `builds` | to build | bouwt | **bouwen** |  |
| `seeks` | to search | zoekt | **zoeken** |  |
| `falls` | to fall | valt | **vallen** |  |
| `opens` | to open | opent | **openen** |  |
| `follows` → `climbs` | to climb | volgt | **klimmen** | **new word** |

### where — Where / Waar

| id | English | Was | Now | |
|---|---|---|---|---|
| `forest` | the forest | in het bos | **het bos** |  |
| `boat` | the boat | op een boot | **de boot** |  |
| `tower` | the tower | in een toren | **de toren** |  |
| `bridge` | the bridge | op een brug | **de brug** |  |
| `island` | the island | op een eiland | **het eiland** |  |
| `market` | the market | op de markt | **de markt** |  |
| `moon` | the moon | op de maan | **de maan** |  |
| `desert` | the desert | in de woestijn | **de woestijn** |  |
| `river` | the river | bij de rivier | **de rivier** |  |
| `attic` | the attic | op zolder | **de zolder** |  |
| `castle` | the castle | in een kasteel | **het kasteel** |  |
| `cave` | the cave | in een grot | **de grot** |  |

### with — With what / Waarmee

| id | English | Was | Now | |
|---|---|---|---|---|
| `key` | the key | een sleutel | **de sleutel** |  |
| `rope` | the rope | een touw | **het touw** |  |
| `lamp` | the lamp | een lamp | **de lamp** |  |
| `book` | the book | een boek | **het boek** |  |
| `egg` | the egg | een ei | **het ei** |  |
| `mirror` | the mirror | een spiegel | **de spiegel** |  |
| `bell` | the bell | een bel | **de bel** |  |
| `coin` | the coin | een munt | **de munt** |  |
| `ladder` | the ladder | een ladder | **de ladder** |  |
| `umbrella` | the umbrella | een paraplu | **de paraplu** |  |
| `sword` | the sword | een zwaard | **het zwaard** |  |
| `seed` | the seed | een zaadje | **het zaadje** |  |

### but — But then / Maar dan

| id | English | Was | Now | |
|---|---|---|---|---|
| `storm` | the storm | een storm | **de storm** |  |
| `door` → `lock` | the lock | een deur op slot | **het slot** | **new word** |
| `hole` | the hole | een gat | **het gat** |  |
| `eye` | the eye | iemand kijkt | **het oog** | **new word** |
| `fire` | the fire | vuur | **het vuur** |  |
| `crash` → `wall` | the wall | een klap | **de muur** | **new word** |
| `fog` | the fog | mist | **de mist** |  |
| `stranger` | the stranger | een vreemdeling | **de vreemdeling** |  |
| `snake` | the snake | een slang | **de slang** |  |
| `time` → `clock` | the clock | de tijd raakt op | **de klok** | **new word** |
| `crowd` | the crowd | een menigte | **de menigte** |  |
| `shadow` | the shadow | een schaduw | **de schaduw** |  |

### end — And in the end / En uiteindelijk

| id | English | Was | Now | |
|---|---|---|---|---|
| `laughing` → `smile` | the smile | lachen | **de glimlach** | **new word** |
| `crying` → `tear` | the tear | huilen | **de traan** | **new word** |
| `asleep` → `bed` | the bed | in slaap | **het bed** | **new word** |
| `home` → `house` | the house | weer thuis | **het huis** | **new word** |
| `nest` | the nest | — | **het nest** | **added** |
| `lost` | — | verdwaald | *dropped* | **removed** |
| `friends` → `friend` | the friend | vrienden | **de vriend** | **new word** |
| `treasure` | the treasure | een schat | **de schat** |  |
| `balloon` | the balloon | wegzwevend | **de ballon** | **new word** |
| `rainbow` | the rainbow | een regenboog | **de regenboog** |  |
| `star` | the star | — | **de ster** | **added** |
| `sunrise` | the sunrise | zonsopgang | **de zonsopgang** |  |
| `empty` | — | met lege handen | *dropped* | **removed** |
| `party` | the party | een feest | **het feest** |  |

## Dropped: two endings, and what replaced them

`lost` (verdwaald) and `empty` (met lege handen) are gone. Both are endings that nothing
concrete carries, and rewording either would have changed its sense rather than kept it.

`het nest` and `de ster` took the two slots. The nest keeps the reel's article mix from
drifting all one way — it is the fourth `het` against eight `de` — and the star is the one
candidate no other tile could be confused with at silhouette size. Six others were
considered and rejected on art grounds: `de koffer` reads as `het boek` at 64px, `de zee`
as `de rivier`, `de kus` as `de vriend`, and `de deur` sits too close to `het slot` in the
same reel.

## Verified genders

Every article above comes from the Woordenlijst Nederlandse Taal (the Groene Boekje),
published by the Nederlandse Taalunie, at woordenlijst.org, checked 2026-11-03.
Labels (m), (v) and (m/v) mean `de`; (o) means `het`.

**de zonsopgang** is included — looked up 2026-11-04, "zelfstandig naamwoord (m)", so `de`.
No article in this document is unverified.

<details>
<summary>61 nouns, with the senses where the list gives more than one</summary>

| Noun | Article | Note |
|---|---|---|
| vos | de | animal sense; het vos is the colour |
| uil | de |  |
| kind | het |  |
| robot | de |  |
| spook | het |  |
| koning | de |  |
| vis | de |  |
| hond | de | animal sense; het hond is a land measure |
| vogel | de |  |
| oma | de | (v) |
| kat | de | animal sense |
| beer | de |  |
| bos | het | FOREST sense (woud); de bos is a bunch |
| boot | de |  |
| toren | de |  |
| brug | de |  |
| eiland | het |  |
| markt | de |  |
| maan | de |  |
| woestijn | de |  |
| rivier | de |  |
| zolder | de |  |
| kasteel | het |  |
| grot | de |  |
| sleutel | de |  |
| touw | het |  |
| lamp | de |  |
| boek | het |  |
| ei | het |  |
| spiegel | de |  |
| bel | de |  |
| munt | de | coin sense; het munt is the colour |
| ladder | de |  |
| paraplu | de |  |
| zwaard | het |  |
| zaadje | het | diminutive |
| storm | de |  |
| slot | het | lock/castle/ending; de slot is a slot machine |
| gat | het |  |
| oog | het |  |
| vuur | het |  |
| muur | de |  |
| mist | de |  |
| vreemdeling | de |  |
| slang | de | animal sense; het slang is jargon |
| klok | de |  |
| menigte | de |  |
| nest | het | (o), checked 2026-11-04 |
| ster | de | (m/v), checked 2026-11-04 |
| schaduw | de |  |
| glimlach | de |  |
| traan | de |  |
| bed | het |  |
| huis | het |  |
| vriend | de |  |
| schat | de |  |
| ballon | de |  |
| regenboog | de |  |
| zonsopgang | de | (m), checked 2026-11-04 |
| zon | de |  |
| feest | het |  |

</details>

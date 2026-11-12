# Story Machine — art to create

72 tile images are needed; none are drawn yet. Every tile in
`server/Oefenpad.Resources/Games/Data/reels.json` still carries an emoji placeholder in its `art` field.
Replacing that string with a path is the only code change the game needs.

Generated 2026-11-04 from `reels.json`. Regenerate rather than hand-edit: `reels.json` is the spec.
The words are settled — see `story-machine-words.md`. Every tile below is safe to draw.

The shared drawing rules, generation prompt and checklist are in `game-art.md`.
This file lists the tiles; that file says how they are drawn.

## Where the files go

`assets/storymachine/art/<reel-id>/<tile-id>.svg`, so `art/who/fox.svg`. Tile ids are
stable and are the filenames, per `story-machine.md`.

Already drawn: `art/cardback_light.jpg` and `art/cardback_dark.jpg` — the BigToe
mascot card back, a placeholder until Quick Wins has its own.

## Rules for every tile

| Rule | Why |
|---|---|
| No text baked into the image, ever | One art set serves every language; words are drawn in HTML per locale |
| One idea per tile, readable as a silhouette at 64px | A phone reel tile is about that size |
| Vague beats specific — "a door", not "a red door with a letterbox" | The player supplies the story |
| Brush-drawn in cobalt, bold and sparse | `game-art.md`; reels are read while moving |
| No culture-specific symbols | The audience is not Dutch |

## who — Who / Wie

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/who/fox.svg` | the fox | de vos | 🦊 |
| `art/who/owl.svg` | the owl | de uil | 🦉 |
| `art/who/child.svg` | the child | het kind | 🧒 |
| `art/who/robot.svg` | the robot | de robot | 🤖 |
| `art/who/ghost.svg` | the ghost | het spook | 👻 |
| `art/who/king.svg` | the king | de koning | 🤴 |
| `art/who/fish.svg` | the fish | de vis | 🐟 |
| `art/who/dog.svg` | the dog | de hond | 🐕 |
| `art/who/bird.svg` | the bird | de vogel | 🐦 |
| `art/who/oma.svg` | the grandmother | de oma | 👵 |
| `art/who/cat.svg` | the cat | de kat | 🐈 |
| `art/who/bear.svg` | the bear | de beer | 🐻 |

## does — Does what / Doet wat

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/does/runs.svg` | to run | rennen | 🏃 |
| `art/does/shelters.svg` | to shelter | schuilen | 🫣 |
| `art/does/digs.svg` | to dig | graven | ⛏️ |
| `art/does/flies.svg` | to fly | vliegen | 🛫 |
| `art/does/sleeps.svg` | to sleep | slapen | 😴 |
| `art/does/sings.svg` | to sing | zingen | 🎤 |
| `art/does/steals.svg` | to steal | stelen | 🥷 |
| `art/does/builds.svg` | to build | bouwen | 🔨 |
| `art/does/seeks.svg` | to search | zoeken | 🔍 |
| `art/does/falls.svg` | to fall | vallen | 🤸 |
| `art/does/opens.svg` | to open | openen | 🔓 |
| `art/does/climbs.svg` | to climb | klimmen | 🧗 |

## where — Where / Waar

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/where/forest.svg` | the forest | het bos | 🌲 |
| `art/where/boat.svg` | the boat | de boot | ⛵ |
| `art/where/tower.svg` | the tower | de toren | 🗼 |
| `art/where/bridge.svg` | the bridge | de brug | 🌉 |
| `art/where/island.svg` | the island | het eiland | 🏝️ |
| `art/where/market.svg` | the market | de markt | 🏪 |
| `art/where/moon.svg` | the moon | de maan | 🌙 |
| `art/where/desert.svg` | the desert | de woestijn | 🏜️ |
| `art/where/river.svg` | the river | de rivier | 🏞️ |
| `art/where/attic.svg` | the attic | de zolder | 🏚️ |
| `art/where/castle.svg` | the castle | het kasteel | 🏰 |
| `art/where/cave.svg` | the cave | de grot | ⛰️ |

## with — With what / Waarmee

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/with/key.svg` | the key | de sleutel | 🔑 |
| `art/with/rope.svg` | the rope | het touw | 🪢 |
| `art/with/lamp.svg` | the lamp | de lamp | 🏮 |
| `art/with/book.svg` | the book | het boek | 📖 |
| `art/with/egg.svg` | the egg | het ei | 🥚 |
| `art/with/mirror.svg` | the mirror | de spiegel | 🪞 |
| `art/with/bell.svg` | the bell | de bel | 🔔 |
| `art/with/coin.svg` | the coin | de munt | 🪙 |
| `art/with/ladder.svg` | the ladder | de ladder | 🪜 |
| `art/with/umbrella.svg` | the umbrella | de paraplu | ☂️ |
| `art/with/sword.svg` | the sword | het zwaard | 🗡️ |
| `art/with/seed.svg` | the seed | het zaadje | 🌱 |

## but — But then / Maar dan

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/but/storm.svg` | the storm | de storm | ⛈️ |
| `art/but/lock.svg` | the lock | het slot | 🔒 |
| `art/but/hole.svg` | the hole | het gat | 🕳️ |
| `art/but/eye.svg` | the eye | het oog | 👁️ |
| `art/but/fire.svg` | the fire | het vuur | 🔥 |
| `art/but/wall.svg` | the wall | de muur | 🧱 |
| `art/but/fog.svg` | the fog | de mist | 🌫️ |
| `art/but/stranger.svg` | the stranger | de vreemdeling | 🕵️ |
| `art/but/snake.svg` | the snake | de slang | 🐍 |
| `art/but/clock.svg` | the clock | de klok | ⏰ |
| `art/but/crowd.svg` | the crowd | de menigte | 👥 |
| `art/but/shadow.svg` | the shadow | de schaduw | 🌑 |

## end — And in the end / En uiteindelijk

12 tiles.

| File | English | Nederlands | Placeholder |
|---|---|---|---|
| `art/end/smile.svg` | the smile | de glimlach | 😊 |
| `art/end/tear.svg` | the tear | de traan | 💧 |
| `art/end/bed.svg` | the bed | het bed | 🛏️ |
| `art/end/house.svg` | the house | het huis | 🏠 |
| `art/end/nest.svg` | the nest | het nest | 🪹 |
| `art/end/friend.svg` | the friend | de vriend | 🤝 |
| `art/end/treasure.svg` | the treasure | de schat | 💎 |
| `art/end/balloon.svg` | the balloon | de ballon | 🎈 |
| `art/end/rainbow.svg` | the rainbow | de regenboog | 🌈 |
| `art/end/star.svg` | the star | de ster | ⭐ |
| `art/end/sunrise.svg` | the sunrise | de zonsopgang | 🌅 |
| `art/end/party.svg` | the party | het feest | 🎉 |


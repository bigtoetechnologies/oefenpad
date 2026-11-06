/* =================================================================
   reels.js — the six reels of the story machine.

   Each reel is one grammatical slot, so any pull reads as a sentence
   skeleton rather than a handful of loose nouns. Reels are added in
   order: 2 reels is WHO + DOES WHAT, 6 reels is the whole arc.

   A tile is:

       { id: 'fox', art: '🦊', en: 'the fox', nl: 'de vos' }

   A reel may also carry a `join`, the words that would stitch it onto
   the sentence so far ("met", "maar dan"). Nothing renders these: the
   machine deliberately never writes the story out. They are kept for a
   read-aloud or print view, should one ever want them.

   `art` is a placeholder. When the drawn set exists it becomes a
   path, and nothing else in the game changes. Keep `id` stable —
   it is the filename the art will be keyed by.

   RULES for the words, from Docs/story-machine.md:
     1. One word per tile, a noun or a verb. A phrase has no picture.
     2. No prepositions. The reel's slot already supplies the sense.
     3. Dutch nouns carry `de` or `het`, never `een` — the article is
        the gender, and the gender is the thing worth learning. Every
        one is checked against woordenlijst.org (Nederlandse Taalunie).
     4. English nouns take `the`, English verbs take `to`, so the
        column says which part of speech a tile is.
     5. Verbs are infinitives in both languages — `to run` / `rennen`.
        A reel tile names an action; the player conjugates it aloud.

   RULES for the art, repeated from Docs/story-machine.md:
     1. No text baked into the image, ever. One set, every language.
     2. One idea per tile, readable as a silhouette at 64px.
     3. Vague beats specific. "A door", not "a red door with a
        letterbox" — the player supplies the story.
     4. Flat and bold. Reels are read while moving.

   `verdwaald` and `met lege handen` were dropped from the `end` reel
   because neither can be shown as a picture; `het nest` and `de ster`
   took their places. Nothing in script.js assumes a reel length.
   ================================================================= */

window.REELS = [
    {
        id: 'who',
        label: { en: 'Who', nl: 'Wie' },
        tiles: [
            { id: 'fox',     art: '🦊', en: 'the fox',         nl: 'de vos' },
            { id: 'owl',     art: '🦉', en: 'the owl',         nl: 'de uil' },
            { id: 'child',   art: '🧒', en: 'the child',       nl: 'het kind' },
            { id: 'robot',   art: '🤖', en: 'the robot',       nl: 'de robot' },
            { id: 'ghost',   art: '👻', en: 'the ghost',       nl: 'het spook' },
            { id: 'king',    art: '🤴', en: 'the king',        nl: 'de koning' },
            { id: 'fish',    art: '🐟', en: 'the fish',        nl: 'de vis' },
            { id: 'dog',     art: '🐕', en: 'the dog',         nl: 'de hond' },
            { id: 'bird',    art: '🐦', en: 'the bird',        nl: 'de vogel' },
            { id: 'oma',     art: '👵', en: 'the grandmother', nl: 'de oma' },
            { id: 'cat',     art: '🐈', en: 'the cat',         nl: 'de kat' },
            { id: 'bear',    art: '🐻', en: 'the bear',        nl: 'de beer' }
        ]
    },
    {
        id: 'does',
        label: { en: 'Does what', nl: 'Doet wat' },
        tiles: [
            { id: 'runs',     art: '🏃', en: 'to run',     nl: 'rennen' },
            { id: 'shelters', art: '🫣', en: 'to shelter', nl: 'schuilen' },
            { id: 'digs',     art: '⛏️', en: 'to dig',     nl: 'graven' },
            { id: 'flies',    art: '🛫', en: 'to fly',     nl: 'vliegen' },
            { id: 'sleeps',   art: '😴', en: 'to sleep',   nl: 'slapen' },
            { id: 'sings',    art: '🎤', en: 'to sing',    nl: 'zingen' },
            { id: 'steals',   art: '🥷', en: 'to steal',   nl: 'stelen' },
            { id: 'builds',   art: '🔨', en: 'to build',   nl: 'bouwen' },
            { id: 'seeks',    art: '🔍', en: 'to search',  nl: 'zoeken' },
            { id: 'falls',    art: '🤸', en: 'to fall',    nl: 'vallen' },
            { id: 'opens',    art: '🔓', en: 'to open',    nl: 'openen' },
            { id: 'climbs',   art: '🧗', en: 'to climb',   nl: 'klimmen' }
        ]
    },
    {
        id: 'where',
        label: { en: 'Where', nl: 'Waar' },
        tiles: [
            { id: 'forest',  art: '🌲', en: 'the forest',  nl: 'het bos' },
            { id: 'boat',    art: '⛵', en: 'the boat',    nl: 'de boot' },
            { id: 'tower',   art: '🗼', en: 'the tower',   nl: 'de toren' },
            { id: 'bridge',  art: '🌉', en: 'the bridge',  nl: 'de brug' },
            { id: 'island',  art: '🏝️', en: 'the island',  nl: 'het eiland' },
            { id: 'market',  art: '🏪', en: 'the market',  nl: 'de markt' },
            { id: 'moon',    art: '🌙', en: 'the moon',    nl: 'de maan' },
            { id: 'desert',  art: '🏜️', en: 'the desert',  nl: 'de woestijn' },
            { id: 'river',   art: '🏞️', en: 'the river',   nl: 'de rivier' },
            { id: 'attic',   art: '🏚️', en: 'the attic',   nl: 'de zolder' },
            { id: 'castle',  art: '🏰', en: 'the castle',  nl: 'het kasteel' },
            { id: 'cave',    art: '⛰️', en: 'the cave',    nl: 'de grot' }
        ]
    },
    {
        id: 'with',
        label: { en: 'With what', nl: 'Waarmee' },
        join: { en: 'with', nl: 'met', comma: false },
        tiles: [
            { id: 'key',      art: '🔑', en: 'the key',      nl: 'de sleutel' },
            { id: 'rope',     art: '🪢', en: 'the rope',     nl: 'het touw' },
            { id: 'lamp',     art: '🏮', en: 'the lamp',     nl: 'de lamp' },
            { id: 'book',     art: '📖', en: 'the book',     nl: 'het boek' },
            { id: 'egg',      art: '🥚', en: 'the egg',      nl: 'het ei' },
            { id: 'mirror',   art: '🪞', en: 'the mirror',   nl: 'de spiegel' },
            { id: 'bell',     art: '🔔', en: 'the bell',     nl: 'de bel' },
            { id: 'coin',     art: '🪙', en: 'the coin',     nl: 'de munt' },
            { id: 'ladder',   art: '🪜', en: 'the ladder',   nl: 'de ladder' },
            { id: 'umbrella', art: '☂️', en: 'the umbrella', nl: 'de paraplu' },
            { id: 'sword',    art: '🗡️', en: 'the sword',    nl: 'het zwaard' },
            { id: 'seed',     art: '🌱', en: 'the seed',     nl: 'het zaadje' }
        ]
    },
    {
        id: 'but',
        label: { en: 'But then', nl: 'Maar dan' },
        join: { en: 'but then', nl: 'maar dan', comma: true },
        tiles: [
            { id: 'storm',     art: '⛈️', en: 'the storm',     nl: 'de storm' },
            { id: 'lock',      art: '🔒', en: 'the lock',      nl: 'het slot' },
            { id: 'hole',      art: '🕳️', en: 'the hole',      nl: 'het gat' },
            { id: 'eye',       art: '👁️', en: 'the eye',       nl: 'het oog' },
            { id: 'fire',      art: '🔥', en: 'the fire',      nl: 'het vuur' },
            { id: 'wall',      art: '🧱', en: 'the wall',      nl: 'de muur' },
            { id: 'fog',       art: '🌫️', en: 'the fog',       nl: 'de mist' },
            { id: 'stranger',  art: '🕵️', en: 'the stranger',  nl: 'de vreemdeling' },
            { id: 'snake',     art: '🐍', en: 'the snake',     nl: 'de slang' },
            { id: 'clock',     art: '⏰', en: 'the clock',     nl: 'de klok' },
            { id: 'crowd',     art: '👥', en: 'the crowd',     nl: 'de menigte' },
            { id: 'shadow',    art: '🌑', en: 'the shadow',    nl: 'de schaduw' }
        ]
    },
    {
        id: 'end',
        label: { en: 'And in the end', nl: 'En uiteindelijk' },
        join: { en: 'and in the end', nl: 'en uiteindelijk', comma: true },
        wildcard: true,
        tiles: [
            { id: 'smile',    art: '😊', en: 'the smile',    nl: 'de glimlach' },
            { id: 'tear',     art: '💧', en: 'the tear',     nl: 'de traan' },
            { id: 'bed',      art: '🛏️', en: 'the bed',      nl: 'het bed' },
            { id: 'house',    art: '🏠', en: 'the house',    nl: 'het huis' },
            { id: 'nest',     art: '🪹', en: 'the nest',     nl: 'het nest' },
            { id: 'friend',   art: '🤝', en: 'the friend',   nl: 'de vriend' },
            { id: 'treasure', art: '💎', en: 'the treasure', nl: 'de schat' },
            { id: 'balloon',  art: '🎈', en: 'the balloon',  nl: 'de ballon' },
            { id: 'rainbow',  art: '🌈', en: 'the rainbow',  nl: 'de regenboog' },
            { id: 'star',     art: '⭐', en: 'the star',     nl: 'de ster' },
            { id: 'sunrise',  art: '🌅', en: 'the sunrise',  nl: 'de zonsopgang' },
            { id: 'party',    art: '🎉', en: 'the party',    nl: 'het feest' }
        ]
    }
];

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

   RULES for the art, repeated from Docs/story-machine.md:
     1. No text baked into the image, ever. One set, every language.
     2. One idea per tile, readable as a silhouette at 64px.
     3. Vague beats specific. "A door", not "a red door with a
        letterbox" — the player supplies the story.
     4. Flat and bold. Reels are read while moving.
   ================================================================= */

window.REELS = [
    {
        id: 'who',
        label: { en: 'Who', nl: 'Wie' },
        tiles: [
            { id: 'fox',     art: '🦊', en: 'the fox',       nl: 'de vos' },
            { id: 'owl',     art: '🦉', en: 'the owl',       nl: 'de uil' },
            { id: 'child',   art: '🧒', en: 'the child',     nl: 'het kind' },
            { id: 'robot',   art: '🤖', en: 'the robot',     nl: 'de robot' },
            { id: 'ghost',   art: '👻', en: 'the ghost',     nl: 'het spook' },
            { id: 'king',    art: '🤴', en: 'the king',      nl: 'de koning' },
            { id: 'fish',    art: '🐟', en: 'the fish',      nl: 'de vis' },
            { id: 'dog',     art: '🐕', en: 'the dog',       nl: 'de hond' },
            { id: 'bird',    art: '🐦', en: 'the bird',      nl: 'de vogel' },
            { id: 'granny',  art: '👵', en: 'the old woman', nl: 'de oude vrouw' },
            { id: 'cat',     art: '🐈', en: 'the cat',       nl: 'de kat' },
            { id: 'bear',    art: '🐻', en: 'the bear',      nl: 'de beer' }
        ]
    },
    {
        id: 'does',
        label: { en: 'Does what', nl: 'Doet wat' },
        tiles: [
            { id: 'runs',    art: '🏃', en: 'runs',   nl: 'rent' },
            { id: 'hides',   art: '🙈', en: 'hides',  nl: 'verstopt zich' },
            { id: 'digs',    art: '⛏️', en: 'digs',   nl: 'graaft' },
            { id: 'flies',   art: '🛫', en: 'flies',  nl: 'vliegt' },
            { id: 'sleeps',  art: '😴', en: 'sleeps', nl: 'slaapt' },
            { id: 'sings',   art: '🎤', en: 'sings',  nl: 'zingt' },
            { id: 'steals',  art: '🥷', en: 'steals', nl: 'steelt' },
            { id: 'builds',  art: '🔨', en: 'builds', nl: 'bouwt' },
            { id: 'seeks',   art: '🔍', en: 'searches', nl: 'zoekt' },
            { id: 'falls',   art: '🤸', en: 'falls',  nl: 'valt' },
            { id: 'opens',   art: '🔓', en: 'opens',  nl: 'opent' },
            { id: 'follows', art: '👣', en: 'follows', nl: 'volgt' }
        ]
    },
    {
        id: 'where',
        label: { en: 'Where', nl: 'Waar' },
        tiles: [
            { id: 'forest',  art: '🌲', en: 'in the forest',  nl: 'in het bos' },
            { id: 'boat',    art: '⛵', en: 'on a boat',      nl: 'op een boot' },
            { id: 'tower',   art: '🗼', en: 'in a tower',     nl: 'in een toren' },
            { id: 'bridge',  art: '🌉', en: 'on a bridge',    nl: 'op een brug' },
            { id: 'island',  art: '🏝️', en: 'on an island',   nl: 'op een eiland' },
            { id: 'market',  art: '🏪', en: 'at the market',  nl: 'op de markt' },
            { id: 'moon',    art: '🌙', en: 'on the moon',    nl: 'op de maan' },
            { id: 'desert',  art: '🏜️', en: 'in the desert',  nl: 'in de woestijn' },
            { id: 'river',   art: '🏞️', en: 'by the river',   nl: 'bij de rivier' },
            { id: 'attic',   art: '🏚️', en: 'in the attic',   nl: 'op zolder' },
            { id: 'castle',  art: '🏰', en: 'in a castle',    nl: 'in een kasteel' },
            { id: 'cave',    art: '⛰️', en: 'in a cave',      nl: 'in een grot' }
        ]
    },
    {
        id: 'with',
        label: { en: 'With what', nl: 'Waarmee' },
        join: { en: 'with', nl: 'met', comma: false },
        tiles: [
            { id: 'key',      art: '🔑', en: 'a key',      nl: 'een sleutel' },
            { id: 'rope',     art: '🪢', en: 'a rope',     nl: 'een touw' },
            { id: 'lamp',     art: '🏮', en: 'a lamp',     nl: 'een lamp' },
            { id: 'book',     art: '📖', en: 'a book',     nl: 'een boek' },
            { id: 'egg',      art: '🥚', en: 'an egg',     nl: 'een ei' },
            { id: 'mirror',   art: '🪞', en: 'a mirror',   nl: 'een spiegel' },
            { id: 'bell',     art: '🔔', en: 'a bell',     nl: 'een bel' },
            { id: 'coin',     art: '🪙', en: 'a coin',     nl: 'een munt' },
            { id: 'ladder',   art: '🪜', en: 'a ladder',   nl: 'een ladder' },
            { id: 'umbrella', art: '☂️', en: 'an umbrella', nl: 'een paraplu' },
            { id: 'sword',    art: '🗡️', en: 'a sword',    nl: 'een zwaard' },
            { id: 'seed',     art: '🌱', en: 'a seed',     nl: 'een zaadje' }
        ]
    },
    {
        id: 'but',
        label: { en: 'But then', nl: 'Maar dan' },
        join: { en: 'but then', nl: 'maar dan', comma: true },
        tiles: [
            { id: 'storm',     art: '⛈️', en: 'a storm',        nl: 'een storm' },
            { id: 'door',      art: '🚪', en: 'a locked door',  nl: 'een deur op slot' },
            { id: 'hole',      art: '🕳️', en: 'a hole',         nl: 'een gat' },
            { id: 'eye',       art: '👁️', en: 'someone watching', nl: 'iemand kijkt' },
            { id: 'fire',      art: '🔥', en: 'fire',           nl: 'vuur' },
            { id: 'crash',     art: '💥', en: 'a crash',        nl: 'een klap' },
            { id: 'fog',       art: '🌫️', en: 'fog',            nl: 'mist' },
            { id: 'stranger',  art: '🕵️', en: 'a stranger',     nl: 'een vreemdeling' },
            { id: 'snake',     art: '🐍', en: 'a snake',        nl: 'een slang' },
            { id: 'time',      art: '⏳', en: 'time runs out',  nl: 'de tijd raakt op' },
            { id: 'crowd',     art: '👥', en: 'a crowd',        nl: 'een menigte' },
            { id: 'shadow',    art: '🌑', en: 'a shadow',       nl: 'een schaduw' }
        ]
    },
    {
        id: 'end',
        label: { en: 'And in the end', nl: 'En uiteindelijk' },
        join: { en: 'and in the end', nl: 'en uiteindelijk', comma: true },
        wildcard: true,
        tiles: [
            { id: 'laughing', art: '😂', en: 'laughing',     nl: 'lachen' },
            { id: 'crying',   art: '😢', en: 'crying',       nl: 'huilen' },
            { id: 'asleep',   art: '💤', en: 'fast asleep',  nl: 'in slaap' },
            { id: 'home',     art: '🏠', en: 'home again',   nl: 'weer thuis' },
            { id: 'lost',     art: '❓', en: 'lost',         nl: 'verdwaald' },
            { id: 'friends',  art: '🤝', en: 'friends',      nl: 'vrienden' },
            { id: 'treasure', art: '💎', en: 'treasure',     nl: 'een schat' },
            { id: 'balloon',  art: '🎈', en: 'floating away', nl: 'wegzwevend' },
            { id: 'rainbow',  art: '🌈', en: 'a rainbow',    nl: 'een regenboog' },
            { id: 'sunrise',  art: '🌅', en: 'sunrise',      nl: 'zonsopgang' },
            { id: 'empty',    art: '🤲', en: 'empty handed', nl: 'met lege handen' },
            { id: 'party',    art: '🎉', en: 'a party',      nl: 'een feest' }
        ]
    }
];

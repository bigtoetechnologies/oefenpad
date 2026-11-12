/* =================================================================
   extract-game-data.mjs — one-shot migration of the browser data
   banks into server-side JSON resources.

   Run once from the repo root:

       node tools/extract-game-data.mjs

   It reads the old `src/*.js` files, strips every Ukrainian (`uk`)
   field — the interface uses English glosses only, per
   Docs/decisions.md — normalises the Dutch field names of the source
   objects to English, and writes:

       server/Oefenpad.Resources/Games/Data/*.json

   These files are embedded in Oefenpad.Resources and are never
   served to the browser. They are the canonical copy now: the old
   `src/` folders were removed when the games became React pages, so
   this script can no longer run. It is kept for provenance. Edit the
   JSON under Data/ directly.
   ================================================================= */

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.env.OEFENPAD_ROOT
    ? path.resolve(process.env.OEFENPAD_ROOT)
    : process.cwd();
const outDir = path.join(root, 'server/Oefenpad.Resources/Games/Data');

function read(rel) {
    return fs.readFileSync(path.join(root, rel), 'utf8');
}

function loadWindow(rel) {
    const window = {};
    const ctx = vm.createContext({ window, console });
    vm.runInContext(read(rel), ctx, { filename: rel });
    return window;
}

/* Balanced-brace scanner that understands strings and comments, so an
   object literal can be lifted out of a script without a parser. */
function balancedEnd(src, start) {
    const open = src[start];
    const close = open === '{' ? '}' : ']';
    let depth = 0;
    let i = start;
    let quote = null;

    while (i < src.length) {
        const c = src[i];
        if (quote) {
            if (c === '\\') { i += 2; continue; }
            if (c === quote) quote = null;
            i++;
            continue;
        }
        if (c === "'" || c === '"' || c === '`') { quote = c; i++; continue; }
        if (c === '/' && src[i + 1] === '/') {
            while (i < src.length && src[i] !== '\n') i++;
            continue;
        }
        if (c === '/' && src[i + 1] === '*') {
            i += 2;
            while (i < src.length && !(src[i] === '*' && src[i + 1] === '/')) i++;
            i += 2;
            continue;
        }
        if (c === open) depth++;
        else if (c === close) {
            depth--;
            if (depth === 0) return i;
        }
        i++;
    }
    throw new Error('unbalanced literal starting at ' + start);
}

function extractLiteral(rel, name) {
    const src = read(rel);
    const re = new RegExp('(?:const|let|var)\\s+' + name + '\\s*=\\s*');
    const m = re.exec(src);
    if (!m) return null;
    const start = m.index + m[0].length;
    if (src[start] !== '{' && src[start] !== '[') return null;
    const end = balancedEnd(src, start);
    return vm.runInNewContext('(' + src.slice(start, end + 1) + ')', {});
}

/* Remove the Ukrainian column everywhere. It is a translation aid,
   not an interface language; the site promises English glosses only. */
function stripUk(value) {
    if (Array.isArray(value)) return value.map(stripUk);
    if (value && typeof value === 'object') {
        const out = {};
        for (const [k, v] of Object.entries(value)) {
            if (k === 'uk') continue;
            out[k] = stripUk(v);
        }
        return out;
    }
    return value;
}

/* The source data objects use Dutch property names. Code and wire
   fields are English, so translate the keys once here instead of
   teaching every consumer two vocabularies. Content stays Dutch. */
function englishPrepositions(source) {
    return {
        scenes: stripUk(source.scenes),
        frames: source.frames.map((f) => {
            const out = {
                id: f.id,
                frame: f.frame,
                en: f.en,
                scene: f.scene,
                contrast: f.contrast ?? null,
                focus: f.focus ?? [],
                example: f.example,
                build: f.bouw ?? [],
                concept: (f.concept ?? []).map((c) => ({
                    question: c.q,
                    answer: c.a
                }))
            };
            if (f.separable) out.separable = true;
            if (f.prefix) out.prefix = f.prefix;
            if (f.pronominal) out.pronominal = f.pronominal;
            if (f.pronominalScene) out.pronominalScene = f.pronominalScene;
            if (f.ontdekOnly) out.discoverOnly = true;
            return out;
        }),
        levels: source.levels.map((l) => {
            const out = { id: l.id, name: l.naam, frames: l.frames };
            if (l.extra) out.extra = l.extra;
            return out;
        })
    };
}

function write(name, value) {
    const file = path.join(outDir, name);
    fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', 'utf8');
    console.log('wrote', path.relative(root, file));
}

/* ---------- word banks and the image manifest ---------- */
const wordsWin = loadWindow('src/shared/words.js');
const imagesWin = loadWindow('src/shared/wordimages.js');
const words = stripUk(wordsWin.OEFENPAD_WORDS);
const wordImages = imagesWin.OEFENPAD_WORD_IMAGES;

write('words.json', words);
write('wordimages.json', wordImages);

/* ---------- prepositions ---------- */
const prepWin = loadWindow('src/voorzetselpaden/data.js');
const prepositions = englishPrepositions(
    prepWin.OEFENPAD_VOORZETSELS ?? prepWin.VOORZETSELS
);
write('prepositions.json', prepositions);

/* ---------- story machine ---------- */
const reelsWin = loadWindow('src/storymachine/reels.js');
write('reels.json', stripUk(reelsWin.REELS));

/* ---------- per-game interface strings ----------
   Only the Dutch column is kept: the games are Dutch-only, and the
   English text in the source tables was never shown. */
const games = {
    galgje: 'hangman',
    geheugen: 'memory',
    koppelen: 'matching',
    woordzoeker: 'wordsearch'
};
for (const [sourceName, gameName] of Object.entries(games)) {
    const literal = extractLiteral(`src/${sourceName}/script.js`, 'TEXTS');
    if (!literal) {
        console.warn('no TEXTS found for', sourceName);
        continue;
    }
    const nl = {};
    for (const [key, value] of Object.entries(literal)) {
        nl[key] = value && (value.nl ?? value.en) ? (value.nl ?? value.en) : key;
    }
    write(`texts.${gameName}.json`, nl);
}

/* ---------- provenance / test fixture ---------- */
const categoryCount = Object.keys(words).length;
const wordCount = Object.values(words)
    .reduce((n, cat) => n + (cat.words ? cat.words.length : 0), 0);

write('meta.json', {
    generatedFrom: 'src/shared and src/voorzetselpaden and src/storymachine',
    categories: categoryCount,
    words: wordCount,
    wordImages: Object.keys(wordImages).length,
    scenes: Object.keys(prepositions.scenes).length,
    frames: prepositions.frames.length,
    levels: prepositions.levels.length,
    reels: reelsWin.REELS.length
});

console.log(`\n${categoryCount} categories, ${wordCount} words, ` +
    `${Object.keys(wordImages).length} images, ` +
    `${prepositions.frames.length} frames, ${prepositions.levels.length} levels, ` +
    `${reelsWin.REELS.length} reels.`);

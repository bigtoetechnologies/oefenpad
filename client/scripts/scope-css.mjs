/* =================================================================
   scope-css.mjs — turn the per-page game stylesheets into route-scoped
   sheets for the single-page app.

   The old pages each loaded their own style.css, so the same class
   names could mean different things on different pages (`.card` is a
   memory card on one page and a story card on another). One bundle
   loads every sheet, so each rule is prefixed with the game's root
   class. Page-level resets move to base.css instead.

       node scripts/scope-css.mjs
   ================================================================= */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const clientRoot = path.resolve(here, '..');
const repoRoot = path.resolve(clientRoot, '..');
const outDir = path.join(clientRoot, 'src/styles/games');

/* The unmodified per-page sheets live under src/styles/source/, vendored
   when the old src/<page>/ folders were removed from the repo. */
const games = [
    ['hangman', 'hangman'],
    ['memory', 'memory'],
    ['matching', 'matching'],
    ['wordsearch', 'wordsearch'],
    ['storymachine', 'storymachine'],
    ['prepositions', 'prepositions'],
    ['verbs', 'verbs'],
    ['separable', 'separable']
];

/* These belong to the shared page shell, not to one game. The universal
   reset is split on commas, so it arrives here as three selectors. */
const skipSelectors = new Set([
    'html',
    'body',
    'html,body',
    '*',
    '*::before',
    '*::after',
    '*,*::before,*::after',
    '*, *::before, *::after',
    'button',
    'button:focus-visible',
    ':focus-visible'
]);

function splitTopLevel(text) {
    const blocks = [];
    let start = 0;
    let depth = 0;
    let quote = null;

    for (let i = 0; i < text.length; i++) {
        const c = text[i];
        if (quote) {
            if (c === '\\') i++;
            else if (c === quote) quote = null;
            continue;
        }
        if (c === '"' || c === "'") { quote = c; continue; }
        if (c === '/' && text[i + 1] === '*') {
            const end = text.indexOf('*/', i + 2);
            i = end === -1 ? text.length : end + 1;
            continue;
        }
        if (c === '{') depth++;
        else if (c === '}') depth--;
        else if (c === ';' && depth === 0) {
            start = i + 1;
        }
        if (depth === 0 && c === '}' && start < i) {
            blocks.push(text.slice(start, i + 1).trim());
            start = i + 1;
        }
    }

    if (start < text.length && text.slice(start).trim()) {
        blocks.push(text.slice(start).trim());
    }
    return blocks;
}

function prefixSelector(selector, scope) {
    const trimmed = selector.trim();
    if (!trimmed) return null;

    /* A :root block that only repeats base.css is noise, but one that overrides
       a token is the game's own setting and dropping it silently changes the
       layout. Scope it to the game root instead: the variables still cascade to
       everything the game draws. */
    if (trimmed.replace(/\s+/g, '') === ':root') return scope;

    if (skipSelectors.has(trimmed.replace(/\s+/g, ''))) return null;
    return `${scope} ${trimmed}`;
}

function transform(css, scope) {
    const out = [];

    for (const block of splitTopLevel(css)) {
        if (!block.includes('{')) continue;

        const open = block.indexOf('{');
        const prelude = block.slice(0, open).trim();
        const body = block.slice(open + 1, block.lastIndexOf('}'));

        if (prelude.startsWith('@keyframes') || prelude.startsWith('@-webkit-keyframes')) {
            out.push(`${prelude}{${body}}`);
            continue;
        }

        if (prelude.startsWith('@media') || prelude.startsWith('@supports')) {
            const inner = transform(body, scope);
            if (inner) out.push(`${prelude}{\n${inner}\n}`);
            continue;
        }

        if (prelude.startsWith('@')) {
            out.push(`${prelude}{${body}}`);
            continue;
        }

        const selectors = prelude.split(',')
            .map((s) => prefixSelector(s, scope))
            .filter(Boolean);

        if (selectors.length) out.push(`${selectors.join(', ')} {${body}}`);
    }

    return out.join('\n');
}

for (const [source, game] of games) {
    const css = fs.readFileSync(
        path.join(clientRoot, 'src/styles/source', `${source}.css`), 'utf8')
        .replace(/\/\*[\s\S]*?\*\//g, '');
    const scoped = transform(css, `.game--${game}`);
    const header = `/* Generated from src/styles/source/${source}.css by scripts/scope-css.mjs.\n` +
        `   Scoped to .game--${game}; edit the source and rerun the script. */\n\n`;
    fs.writeFileSync(path.join(outDir, `${game}.css`), header + scoped + '\n', 'utf8');
    console.log('wrote', `src/styles/games/${game}.css`);
}

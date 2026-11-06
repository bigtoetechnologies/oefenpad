    /* =================================================================
       Woordzoeker — Oefenpad
       ================================================================= */

    // ---- Word Categories (shared bank, loaded from ../words.js) ----
    const CATEGORIES = window.OEFENPAD_WORDS || {};
    const IMAGES = window.OEFENPAD_WORD_IMAGES || {};

    // Default category on first visit
    const DEFAULT_CATEGORY = 'animals';

    // ---- Bilingual helpers & UI translations ----
    const I18N = window.I18N || { lang: 'en', t: function () { return null; }, register: function () {} };

    const TEXTS = {
        'found-label': { en: 'Found:', nl: 'Gevonden:', uk: 'Знайдено:' },
        'hints-label': { en: '💡 Hints:', nl: '💡 Hints:', uk: '💡 Підказки:' },
        'words-title': { en: 'Words to Find', nl: 'Te vinden woorden', uk: 'Слова для пошуку' },
        'btn-hint': { en: '💡 Hint', nl: '💡 Hint', uk: '💡 Підказка' },
        'btn-new': { en: '🎲 New Game', nl: '🎲 Nieuw spel', uk: '🎲 Нова гра' },
        'cele-title': { en: 'All Words Found!', nl: 'Alle woorden gevonden!', uk: 'Усі слова знайдено!' },
        'cele-msg': { en: 'Great job! You found every word.', nl: 'Goed gedaan! Je hebt alle woorden gevonden.', uk: 'Чудова робота! Ви знайшли всі слова.' },
        'time-label': { en: 'Time:', nl: 'Tijd:', uk: 'Час:' },
        'btn-close': { en: '✕ Close', nl: '✕ Sluiten', uk: '✕ Закрити' },
        'settings-title': { en: '⚙️ Settings', nl: '⚙️ Instellingen', uk: '⚙️ Налаштування' },
        'sound-effects': { en: '🔊 Sound Effects', nl: '🔊 Geluidseffecten', uk: '🔊 Звукові ефекти' },
        'translate-label': { en: '🌍 Translate words', nl: '🌍 Woorden vertalen', uk: '🌍 Перекладати слова' },
        'translate-off': { en: 'Off', nl: 'Uit', uk: 'Вимкнено' },
        'translate-hint': { en: 'Tap or hover a word in the list to see it in your language. Only words that have a translation are used.', nl: 'Tik op een woord in de lijst of houd de muis erboven om het in jouw taal te zien. Alleen woorden met een vertaling worden gebruikt.', uk: 'Торкніться слова у списку або наведіть на нього, щоб побачити його вашою мовою. Використовуються лише слова, які мають переклад.' },
        'close': { en: 'Close', nl: 'Sluiten', uk: 'Закрити' },
        'cat-title': { en: 'Choose a Category', nl: 'Kies een categorie', uk: 'Оберіть категорію' },
        'cat-subtitle': { en: 'Select a theme for your word search puzzle:', nl: 'Kies een thema voor je woordzoeker:', uk: 'Виберіть тему для пошуку слів:' },
        'cancel': { en: 'Cancel', nl: 'Annuleren', uk: 'Скасувати' },
        'random-cat': { en: 'Random Category', nl: 'Willekeurige categorie', uk: 'Випадкова категорія' },
        'about': { en: 'About', nl: 'Over dit spel', uk: 'Про гру' },
        'ws-title': { en: 'Word Search', nl: 'Woordzoeker', uk: 'Пошук слів' },
        'version': { en: 'Version 0.2.0', nl: 'Versie 0.2.0', uk: 'Версія 0.2.0' },
        'about-text': {
            en: 'Six difficulty levels from Beginner to Insane, with grid sizes from 10×10 to 20×20. Choose a word category and find every hidden Dutch word.',
            nl: 'Zes moeilijkheidsgraden, van Beginner tot Waanzinnig, met roosters van 10×10 tot 20×20. Kies een woordcategorie en zoek alle verborgen Nederlandse woorden.',
            uk: 'Шість рівнів складності — від Початківця до Божевільного, із сітками від 10×10 до 20×20. Оберіть категорію та знайдіть усі приховані нідерландські слова.'
        },
        'settings-tip': { en: 'Settings', nl: 'Instellingen', uk: 'Налаштування' },
        'splash-alt': { en: 'Word Search', nl: 'Woordzoeker', uk: 'Пошук слів' },
        'diff-beginner': { en: 'Beginner', nl: 'Beginner', uk: 'Початківець' },
        'diff-easy': { en: 'Easy', nl: 'Makkelijk', uk: 'Легкий' },
        'diff-medium': { en: 'Medium', nl: 'Gemiddeld', uk: 'Середній' },
        'diff-hard': { en: 'Hard', nl: 'Moeilijk', uk: 'Складний' },
        'diff-master': { en: 'Master', nl: 'Meester', uk: 'Майстер' },
        'diff-insane': { en: 'Insane', nl: 'Waanzinnig', uk: 'Божевільний' }
    };
    I18N.register('woordzoeker', TEXTS);

    function T(key, vars) { return I18N.t(key, vars) || (TEXTS[key] ? TEXTS[key].en : key); }
    function catLabel(cat) { return cat.label[I18N.lang] || cat.label.en; }

    // UK → US vocabulary variants in the shared English word lists.
    // (Spelling differences live in the i18n layer; these are whole-word
    // differences.) Applied only for US English and only when generating a
    // new puzzle — a puzzle in progress keeps the words it was made with.
    const WORD_VARIANTS_US = {
        'BOOKSHOP': 'BOOKSTORE',
        'RUCKSACK': 'BACKPACK'
    };
    // Word Search only ever uses single words (no spaces / punctuation),
    // the same rule OEFENPAD.words applies for { singleOnly: true }.
    const SINGLE_WORD = /^[\p{L}]+$/u;

    // Each word, paired with its translation into the player's chosen
    // language. In translation mode a word with no translation is dropped
    // from the pool, so every word in the puzzle can be looked up.
    function catPairs(cat) {
        const lang = wordsLang();
        const target = (translateTo && translateTo !== lang) ? translateTo : '';
        const pairs = [];
        for (const entry of OEFENPAD.entries(cat, lang)) {
            if (!SINGLE_WORD.test(entry[lang])) continue;
            if (target && !entry[target]) continue;
            let word = entry[lang];
            if (I18N.lang === 'en-us') word = WORD_VARIANTS_US[word] || word;
            pairs.push({
                word: word,
                translation: target ? entry[target] : '',
                img: IMAGES[entry.en] || ''
            });
        }
        return pairs;
    }
    function catWords(cat) {
        return catPairs(cat).map(function (p) { return p.word; });
    }
    function diffLabel(diff) { return diff.label[I18N.lang] || diff.label.en; }

    // Blocked words for filler-letter profanity filter (all caps)
    const BLOCKED_WORDS = [
        'ANAL','ANUS','ARSE','ASS','BASTARD','BITCH','BLOODY','BOLLOCKS','BONER','BUM',
        'BUTT','CLIT','COCK','COON','CRAP','CUM','CUNT','DAMN','DICK','DIKE',
        'DYKE','FAG','FART','FELCH','FUCK','GAY','GOOK','HELL','HOE','HOMO',
        'HORE','JAP','JERK','JIZZ','KNOB','KUNT','LICK','MUFF','NIG','NOB',
        'PEDO','PENIS','PISS','POOP','PORN','PRICK','PUBE','PUSSY','QUEER','RAPE',
        'RIM','SCHLONG','SCREW','SCUM','SEMEN','SEX','SHAG','SHIT','SKANK','SLUT',
        'SMEG','SPAZ','SPERM','SPIC','TIT','TURD','TWAT','VAG','VULVA','WANG',
        'WANK','WHORE','WOG','WOP','KUT','LUL','PIK','NEUK','NEUKEN','HOER',
        'SLOERIE','TYFUS','TERING','KOLERE','KLOTE','KLOTEN','GODVER','VERDOMME','STRONT','SCHIJT',
        'PIS','ZEIK','KONT','REET','SUKKEL','EIKEL','NEGER','MOF','PLEE','KAK',
        'FLIKKER','KLOOTZAK','HUFFER','SMEERLAP','MIETJE','PLEURIS','TIEFUS','POKKEN','KANKER','TRUT',
        'СРАКА','ДУПА','ЖОПА','ГІВНО','ГІМНО','ЛАЙНО','СРАТИ','СЦЯТИ','ПЕРДІТИ','БЗДІТИ',
        'ХУЙ','ХУЇ','ПІЗДА','ПИЗДА','ЇБАТИ','ЙОБАНИЙ','НАХУЙ','ПОХУЙ','ЗАЄБАЛО','ЗАЇБАЛО',
        'БЛЯДЬ','БЛЯ','КУРВА','ШЛЮХА','ПОВІЯ','СУКА','МУДАК','МУДЛО','ДЕБІЛ','ДОВБОЙОБ',
        'ПІДАР','ПІДОРАС','ГОМІК','СЕКС','ПОРНО','МАСТУРБ','ДРОЧИТИ','ЧЛЕН','ВАГІНА','ПОЦ'
    ];

    // Filler alphabet per language: Ukrainian puzzles get Cyrillic filler
    // letters so grids look native (and Latin blocked words can't form in them).
    const FILLER_ALPHABETS = { uk: 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ' };
    function fillerAlphabet() {
        return FILLER_ALPHABETS[I18N.lang] || 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    }

    // ---- Difficulty Configs ----
    const DIFFICULTIES = {
        beginner: {
            label: { en: 'Beginner', nl: 'Beginner' },
            gridSize: 10,
            wordCount: 6,
            directions: [[0, 1]],                          // right only
            minWordLen: 3, maxWordLen: 5,
            minOverlapPct: 30,
            avoidAdjacent: true
        },
        easy: {
            label: { en: 'Easy', nl: 'Makkelijk' },
            gridSize: 12,
            wordCount: 8,
            directions: [[0, 1], [1, 0]],                  // right, down only
            minWordLen: 3, maxWordLen: 6,
            minOverlapPct: 25,
            avoidAdjacent: true
        },
        medium: {
            label: { en: 'Medium', nl: 'Gemiddeld' },
            gridSize: 16,
            wordCount: 10,
            directions: [[0, 1], [0, -1], [1, 0], [-1, 0]], // horiz & vert, both ways
            minWordLen: 4, maxWordLen: 7,
            minOverlapPct: 25,
            avoidAdjacent: false
        },
        hard: {
            label: { en: 'Hard', nl: 'Moeilijk' },
            gridSize: 20,
            wordCount: 16,
            directions: [                                     // all 8
                [0, 1], [1, 0], [1, 1], [-1, 1],
                [0, -1], [-1, 0], [1, -1], [-1, -1]
            ],
            minWordLen: 4, maxWordLen: 10,
            minOverlapPct: 25,
            avoidAdjacent: false
        },
        master: {
            label: { en: 'Master', nl: 'Meester' },
            gridSize: 20,
            wordCount: 20,
            directions: [                                     // all 8
                [0, 1], [1, 0], [1, 1], [-1, 1],
                [0, -1], [-1, 0], [1, -1], [-1, -1]
            ],
            minWordLen: 4, maxWordLen: 13,
            minOverlapPct: 25,
            avoidAdjacent: false
        },
        insane: {
            label: { en: 'Insane', nl: 'Waanzinnig' },
            gridSize: 20,
            wordCount: 65,
            directions: [                                     // all 8
                [0, 1], [1, 0], [1, 1], [-1, 1],
                [0, -1], [-1, 0], [1, -1], [-1, -1]
            ],
            minWordLen: 4, maxWordLen: 13,
            minOverlapPct: 0,
            minDensity: 0.75,                                 // crossing-rich boards: density trades off against overlaps
            strictOverlap: true,                              // always pick max-overlap placements so words cross
            maxRegenerations: 5,
            avoidAdjacent: false
        }
    };

    // ---- State ----
    const SAVE_VERSION = 4;  // 4: Insane regenerated as crossing-rich boards (discard old diagonal saves)
    let currentDifficulty = 'beginner';
    let currentCategory = DEFAULT_CATEGORY;
    let gridSize = 20;
    let grid = [];
    let solution = [];
    let words = [];
    let foundWords = [];
    let foundRects = [];       // {r1,c1,r2,c2} for canvas rectangles around found words
    let hintsRemaining = 3;
    let hintTimer = null;      // timeout for clearing hint animation
    let gameSeconds = 0;
    let gameTimer = null;
    const fmtTime = OEFENPAD.fmtTime;   // shared helper, see common.js
    function startTimer() {
        stopTimer();
        gameTimer = setInterval(function() {
            gameSeconds++;
            document.getElementById('timerDisplay').textContent = '⏱ ' + fmtTime(gameSeconds);
        }, 1000);
    }
    function stopTimer() { if (gameTimer) { clearInterval(gameTimer); gameTimer = null; } }
    let hintWordIdx = -1;      // which word is currently being hinted
    let stats = { wins: 0, streak: 0, bestStreak: 0 };
    let settings = { soundEffects: true };

    // ---- Translation hints ----
    // Someone playing in a language they are learning can have each word
    // shown in a language they already know. '' means off; otherwise a
    // language code, always different from the puzzle's own language.
    let translateTo = '';
    let prevTranslateTo = '';          // restored if the player cancels the restart
    let pendingTranslateRevert = false;
    let translations = {};             // puzzle word -> word in translateTo

    // Selection state
    let selStart = null;
    let selEnd = null;
    let selCells = [];
    let pendingSelection = false;  // true between first click and second click / cancel
    let dragActive = false;
    let pointerIsDown = false;
    let dragStartR = -1, dragStartC = -1;
    let flashTimer = null;

    // ---- Word Search Generator ----
    function hasTouchingWord(word, row, col, dr, dc) {
        // For each cell of the candidate word, check all 4 orthogonal neighbours.
        // If a neighbour belongs to another word (not an overlap with us), reject.
        const ORTHO = [[-1,0],[1,0],[0,-1],[0,1]];

        for (let i = 0; i < word.length; i++) {
            const r = row + dr * i;
            const c = col + dc * i;

            for (const [odr, odc] of ORTHO) {
                const nr = r + odr;
                const nc = c + odc;
                if (nr < 0 || nr >= gridSize || nc < 0 || nc >= gridSize) continue;
                const neighbour = solution[nr][nc];
                if (neighbour === null || neighbour < 0) continue;

                // Is this neighbour part of the candidate word itself? (overlap)
                let isSelf = false;
                for (let j = 0; j < word.length; j++) {
                    if (row + dr * j === nr && col + dc * j === nc) {
                        isSelf = true;
                        break;
                    }
                }
                if (isSelf) continue;  // overlap is fine — they share a letter

                // Different words touching orthogonally — reject
                return true;
            }
        }
        return false;
    }

    function canPlace(word, row, col, dr, dc, avoidAdjacent) {
        // Check each cell of the word itself
        for (let i = 0; i < word.length; i++) {
            const r = row + dr * i;
            const c = col + dc * i;
            if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) return false;
            if (solution[r][c] !== null && solution[r][c] >= 0) {
                // Already occupied by another word — must match letter
                if (grid[r][c] !== word[i]) return false;
                // Must NOT be in the same direction (they'd merge, not intersect)
                const existing = words[solution[r][c]];
                if (existing.dr * dc === existing.dc * dr) return false;
            }
        }

        // Reject if another same-direction word sits immediately before us
        const beforeR = row - dr;
        const beforeC = col - dc;
        if (beforeR >= 0 && beforeR < gridSize && beforeC >= 0 && beforeC < gridSize) {
            const prev = solution[beforeR][beforeC];
            if (prev !== null && prev >= 0) {
                const pw = words[prev];
                if (pw.dr * dc === pw.dc * dr) return false;
            }
        }

        // Reject if another same-direction word sits immediately after us
        const afterR = row + dr * word.length;
        const afterC = col + dc * word.length;
        if (afterR >= 0 && afterR < gridSize && afterC >= 0 && afterC < gridSize) {
            const next = solution[afterR][afterC];
            if (next !== null && next >= 0) {
                const nw = words[next];
                if (nw.dr * dc === nw.dc * dr) return false;
            }
        }

        // Reject if another word touches us orthogonally without sharing a letter
        if (avoidAdjacent && hasTouchingWord(word, row, col, dr, dc)) return false;
        return true;
    }

    function placeWord(word, idx, row, col, dr, dc) {
        words.push({ word, row, col, dr, dc });
        for (let i = 0; i < word.length; i++) {
            const r = row + dr * i;
            const c = col + dc * i;
            grid[r][c] = word[i];
            solution[r][c] = idx;
        }
    }

    function countOverlaps(word, row, col, dr, dc) {
        let overlaps = 0;
        for (let i = 0; i < word.length; i++) {
            const r = row + dr * i;
            const c = col + dc * i;
            if (solution[r][c] !== null && solution[r][c] >= 0 && grid[r][c] === word[i]) {
                overlaps++;
            }
        }
        return overlaps;
    }

    function shuffleWordOrder() {
        // Randomize the word-list order so it doesn't reveal placement order.
        const order = words.map((_, i) => i);
        for (let i = order.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            const tmp = order[i]; order[i] = order[j]; order[j] = tmp;
        }
        const newIdx = new Array(order.length);
        order.forEach((oldIdx, newI) => { newIdx[oldIdx] = newI; });
        words = order.map(oldIdx => words[oldIdx]);
        for (let r = 0; r < gridSize; r++) {
            for (let c = 0; c < gridSize; c++) {
                const v = solution[r][c];
                if (v !== null && v >= 0) solution[r][c] = newIdx[v];
            }
        }
        foundWords = new Array(words.length).fill(false);
    }

    function generatePuzzle() {
        const diff = DIFFICULTIES[currentDifficulty];
        const MAX_REGENERATIONS = diff.maxRegenerations || 25;
        const dirs = diff.directions;
        const gs = diff.gridSize;
        gridSize = gs;

        // Filter category words by length for this difficulty
        const cat = CATEGORIES[currentCategory] || CATEGORIES[DEFAULT_CATEGORY];
        const pairs = catPairs(cat);
        const pairByWord = {};
        pairs.forEach(function (p) { pairByWord[p.word] = p; });
        const eligible = pairs
            .map(function (p) { return p.word; })
            .filter(w => w.length >= diff.minWordLen && w.length <= diff.maxWordLen);
        if (!eligible.length) {
            // Nothing fits this difficulty (translation mode can empty a
            // category). Fall back once — never recurse into the default.
            if (currentCategory === DEFAULT_CATEGORY) return;
            currentCategory = DEFAULT_CATEGORY;
            return generatePuzzle();
        }

        // minDensity mode (Insane): keep the best attempt and install it at the end
        let bestSnapshot = null;
        let bestDensity = -1;
        let overlapPct = 0;
        let density = 0;

        for (let regen = 0; regen < MAX_REGENERATIONS; regen++) {
            grid = Array.from({ length: gs }, () => Array(gs).fill(''));
            solution = Array.from({ length: gs }, () => Array(gs).fill(null));
            words = [];
            foundWords = [];

            const shuffled = [...eligible].sort(() => Math.random() - 0.5);

            // Build the word list, rejecting any word that is a substring
            // of (or contains as a substring) any already-selected word
            const selected = [];
            for (const w of shuffled) {
                if (selected.length >= diff.wordCount) break;
                const conflicts = selected.some(
                    existing => existing.includes(w) || w.includes(existing)
                );
                if (!conflicts) selected.push(w);
            }

            // If we couldn't get enough, pad with what we have
            if (selected.length < 2) {
                // Fallback: just take the first N without substring filtering
                selected.length = 0;
                for (const w of shuffled) {
                    if (selected.length >= diff.wordCount) break;
                    selected.push(w);
                }
            }

            // Safety net: remove any accidental duplicates within the selection
            const seen = new Set();
            for (let i = selected.length - 1; i >= 0; i--) {
                if (seen.has(selected[i])) {
                    selected.splice(i, 1);
                } else {
                    seen.add(selected[i]);
                }
            }

            selected.sort((a, b) => b.length - a.length);  // longest first

            let totalWordLetters = 0;

            for (let idx = 0; idx < selected.length; idx++) {
                const word = selected[idx];
                const candidates = [];
                const maxAttempts = 500;

                for (let attempt = 0; attempt < maxAttempts; attempt++) {
                    const dir = dirs[Math.floor(Math.random() * dirs.length)];
                    const row = Math.floor(Math.random() * gs);
                    const col = Math.floor(Math.random() * gs);

                    if (canPlace(word, row, col, dir[0], dir[1], diff.avoidAdjacent)) {
                        const ov = countOverlaps(word, row, col, dir[0], dir[1]);
                        candidates.push({ row, col, dr: dir[0], dc: dir[1], overlaps: ov });
                    }
                }

                if (candidates.length > 0) {
                    candidates.sort((a, b) => b.overlaps - a.overlaps);
                    let pick;
                    if (diff.strictOverlap) {
                        // Insane: always pick among the maximum-overlap candidates
                        // so words cross each other as much as possible.
                        const maxOv = candidates[0].overlaps;
                        const top = candidates.filter(c => c.overlaps === maxOv);
                        pick = top[Math.floor(Math.random() * top.length)];
                    } else {
                        const maxOv = candidates[0].overlaps;
                        let poolSize = Math.max(1, Math.ceil(candidates.length * 0.3));
                        while (poolSize < candidates.length && candidates[poolSize].overlaps === maxOv) {
                            poolSize++;
                        }
                        pick = candidates[Math.floor(Math.random() * poolSize)];
                    }
                    placeWord(word, words.length, pick.row, pick.col, pick.dr, pick.dc);
                    totalWordLetters += word.length;
                }
            }

            // Re-index words (some may have been skipped)
            const actualWords = [];
            const wordMap = [];
            for (let i = 0; i < words.length; i++) {
                actualWords.push(words[i]);
                wordMap.push(i);
            }
            words = actualWords;
            // Keep the picture (and translation) attached through regeneration.
            words.forEach(function (w) {
                const p = pairByWord[w.word];
                if (p) w.img = p.img;
            });
            foundWords = new Array(words.length).fill(false);

            for (let r = 0; r < gs; r++) {
                for (let c = 0; c < gs; c++) {
                    if (solution[r][c] !== null && solution[r][c] >= 0) {
                        const oldIdx = solution[r][c];
                        const newIdx = wordMap.indexOf(oldIdx);
                        solution[r][c] = newIdx >= 0 ? newIdx : null;
                    }
                }
            }

            // Compute overlap and density
            let uniqueCells = 0;
            for (let r = 0; r < gs; r++) {
                for (let c = 0; c < gs; c++) {
                    if (solution[r][c] !== null && solution[r][c] >= 0) uniqueCells++;
                }
            }
            overlapPct = totalWordLetters > 0
                ? ((totalWordLetters - uniqueCells) / totalWordLetters) * 100
                : 0;
            density = uniqueCells / (gs * gs);

            if (diff.minDensity) {
                if (density > bestDensity) {
                    bestDensity = density;
                    bestSnapshot = {
                        grid: grid.map(row => row.slice()),
                        solution: solution.map(row => row.slice()),
                        words: words.slice(),
                        foundWords: foundWords.slice()
                    };
                }
                if (density >= diff.minDensity) break;
                continue;
            }

            if (overlapPct >= diff.minOverlapPct) break;
        }

        // minDensity mode: install the best attempt found
        if (diff.minDensity && bestSnapshot) {
            grid = bestSnapshot.grid;
            solution = bestSnapshot.solution;
            words = bestSnapshot.words;
            foundWords = bestSnapshot.foundWords;
            shuffleWordOrder();
        }

        // Fill remaining cells with safe random letters
        const ABC = fillerAlphabet();
        for (let r = 0; r < gs; r++) {
            for (let c = 0; c < gs; c++) {
                if (grid[r][c] === '') {
                    grid[r][c] = ABC[Math.floor(Math.random() * ABC.length)];
                }
            }
        }

        // Profanity scan — replace any filler letter that creates a blocked word
        sanitizeFillerWords(gs);

        console.log('[' + diffLabel(diff) + '] ' + catLabel(cat) + ' — ' + (diff.minDensity ? (bestDensity * 100).toFixed(1) + '% density' : overlapPct.toFixed(1) + '% overlap') + ' (' + words.length + ' words)');
    }

    // ---- Profanity Filter ----
    function sanitizeFillerWords(gs) {
        // Scan all 8 directions for blocked words formed entirely or partially by filler letters.
        // If found, replace one of the filler letters in that sequence.
        const dirs = [[0,1],[1,0],[1,1],[-1,1],[0,-1],[-1,0],[1,-1],[-1,-1]];
        const ABC = fillerAlphabet();
        let changed = true;
        let passes = 0;

        while (changed && passes < 20) {
            changed = false;
            passes++;

            for (let r = 0; r < gs; r++) {
                for (let c = 0; c < gs; c++) {
                    for (const [dr, dc] of dirs) {
                        // Build string in this direction up to 8 chars
                        let str = '';
                        let cells = [];
                        let rr = r, cc = c;
                        while (rr >= 0 && rr < gs && cc >= 0 && cc < gs && str.length < 8) {
                            str += grid[rr][cc];
                            cells.push({ r: rr, c: cc });
                            rr += dr;
                            cc += dc;
                        }

                        // Check every substring of the built string
                        for (let len = 3; len <= str.length; len++) {
                            for (let start = 0; start + len <= str.length; start++) {
                                const sub = str.substring(start, start + len);
                                if (BLOCKED_WORDS.includes(sub)) {
                                    // Replace a filler letter in the offending sequence
                                    for (let k = start; k < start + len; k++) {
                                        const cell = cells[k];
                                        if (solution[cell.r][cell.c] === null || solution[cell.r][cell.c] < 0) {
                                            grid[cell.r][cell.c] = ABC[Math.floor(Math.random() * ABC.length)];
                                            changed = true;
                                            break;
                                        }
                                    }
                                    if (changed) break;
                                }
                            }
                            if (changed) break;
                        }
                        if (changed) break;
                    }
                    if (changed) break;
                }
                if (changed) break;
            }
        }
    }

    // ---- Rendering ----
    function A11Y(key, vars, fallback) {
        const s = I18N.t(key, vars);
        return s === null ? fallback : s;
    }

    function renderGrid() {
        const gridEl = document.getElementById('grid');
        gridEl.innerHTML = '';
        gridEl.setAttribute('role', 'grid');
        gridEl.setAttribute('aria-label', A11Y('a11y-board', null, 'Puzzle board'));

        // Set dynamic grid sizing
        const maxWidth = Math.min(window.innerWidth - 200, 500);
        const cellSize = Math.max(16, Math.min(36, Math.floor(maxWidth / gridSize)));
        const fontSize = cellSize > 28 ? 15 : cellSize > 22 ? 13 : cellSize > 18 ? 11 : 9;
        gridEl.style.gridTemplateColumns = 'repeat(' + gridSize + ', ' + cellSize + 'px)';
        gridEl.style.gridTemplateRows = 'repeat(' + gridSize + ', ' + cellSize + 'px)';

        // Size the selection canvas to match the grid
        const canvas = document.getElementById('selectionCanvas');
        const totalW = gridSize * cellSize + (gridSize - 1) * 1; // 1px gap
        canvas.width = totalW;
        canvas.height = totalW;
        canvas.style.width = totalW + 'px';
        canvas.style.height = totalW + 'px';

        for (let r = 0; r < gridSize; r++) {
            for (let c = 0; c < gridSize; c++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.setAttribute('role', 'gridcell');
                // Cells are drag-selected, not individually clicked, so they
                // aren't focus targets — but the board should still be
                // readable letter by letter with a screen-reader cursor.
                cell.setAttribute('aria-label',
                    A11Y('a11y-cell', { row: r + 1, col: c + 1, value: grid[r][c] },
                         'Row ' + (r + 1) + ', column ' + (c + 1) + ', ' + grid[r][c]));
                cell.textContent = grid[r][c];
                cell.style.width = cellSize + 'px';
                cell.style.height = cellSize + 'px';
                cell.style.fontSize = fontSize + 'px';
                cell.dataset.row = r;
                cell.dataset.col = c;

                if (solution[r][c] !== null && solution[r][c] >= 0 && foundWords[solution[r][c]]) {
                    cell.classList.add('found');
                }

                gridEl.appendChild(cell);
            }
        }
    }

    // Translations are looked up by word, not stored in the puzzle, so a
    // saved game picks them up too.
    function buildTranslations() {
        translations = {};
        if (!translateTo) return;
        const cat = CATEGORIES[currentCategory] || CATEGORIES[DEFAULT_CATEGORY];
        for (const p of catPairs(cat)) {
            if (p.translation) translations[p.word] = p.translation;
        }
    }

    function renderWordList() {
        const listEl = document.getElementById('wordList');
        listEl.innerHTML = '';
        buildTranslations();

        for (let i = 0; i < words.length; i++) {
            const li = document.createElement('li');
            // A picture beside the word ties the letters to a meaning while
            // the player scans the grid. Words without an image just show
            // their letters, as before.
            if (words[i].img) {
                const thumb = document.createElement('img');
                thumb.className = 'word-thumb';
                thumb.src = '../../assets/wordimages/' + words[i].img;
                thumb.alt = '';
                li.appendChild(thumb);
            }
            const label = document.createElement('span');
            label.className = 'word-text';
            label.textContent = words[i].word;
            li.appendChild(label);
            const translation = translations[words[i].word];
            if (translation) {
                li.classList.add('has-translation');
                const span = document.createElement('span');
                span.className = 'word-translation';
                span.textContent = translation;
                span.lang = translateTo;
                li.appendChild(span);
            }
            if (foundWords[i]) {
                li.classList.add('found');
            }
            listEl.appendChild(li);
        }

        document.getElementById('totalCount').textContent = words.length;
        updateFoundCount();
    }

    function updateFoundCount() {
        const count = foundWords.filter(Boolean).length;
        document.getElementById('foundCount').textContent = count;
    }

    function renderAll() {
        renderGrid();
        renderWordList();
    }

    // ---- Cell Selection ----
    function getCellEl(r, c) {
        const gridEl = document.getElementById('grid');
        return gridEl.children[r * gridSize + c];
    }

    function clearSelection() {
        // Clear start marker
        if (selStart) {
            const startEl = getCellEl(selStart.r, selStart.c);
            if (startEl) startEl.classList.remove('start-marker');
        }
        // Clear all selected cells
        for (const cell of selCells) {
            const el = getCellEl(cell.r, cell.c);
            if (el) {
                el.classList.remove('selecting', 'selected', 'error');
                // Re-apply found class if this cell belongs to a found word
                if (solution[cell.r][cell.c] !== null && solution[cell.r][cell.c] >= 0 && foundWords[solution[cell.r][cell.c]]) {
                    el.classList.add('found');
                }
            }
        }
        selCells = [];
    }

    function highlightSelection() {
        clearSelection();

        if (!selStart || !selEnd) return;

        const dr = selEnd.r - selStart.r;
        const dc = selEnd.c - selStart.c;

        // Determine direction — must be horizontal, vertical, or diagonal
        let stepR = 0, stepC = 0;
        if (dr === 0 && dc !== 0) { stepR = 0; stepC = dc > 0 ? 1 : -1; }
        else if (dc === 0 && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = 0; }
        else if (Math.abs(dr) === Math.abs(dc) && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = dc > 0 ? 1 : -1; }
        else return; // Not a valid straight line

        let r = selStart.r;
        let c = selStart.c;
        while (true) {
            if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) break;
            selCells.push({ r, c });
            const el = getCellEl(r, c);
            if (el) {
                if (solution[r][c] !== null && solution[r][c] >= 0 && foundWords[solution[r][c]]) {
                    el.classList.add('found');
                } else {
                    el.classList.add('selecting');
                }
            }
            if (r === selEnd.r && c === selEnd.c) break;
            r += stepR;
            c += stepC;
        }
    }

    function checkSelection() {
        // Returns true if a word was found, false otherwise
        if (!selStart || !selEnd) return false;

        const dr = selEnd.r - selStart.r;
        const dc = selEnd.c - selStart.c;

        let stepR = 0, stepC = 0;
        if (dr === 0 && dc !== 0) { stepR = 0; stepC = dc > 0 ? 1 : -1; }
        else if (dc === 0 && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = 0; }
        else if (Math.abs(dr) === Math.abs(dc) && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = dc > 0 ? 1 : -1; }
        else return false;

        // Build selected word
        let selectedWord = '';
        const cellsInLine = [];
        let r = selStart.r;
        let c = selStart.c;
        while (true) {
            if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) break;
            selectedWord += grid[r][c];
            cellsInLine.push({ r, c });
            if (r === selEnd.r && c === selEnd.c) break;
            r += stepR;
            c += stepC;
        }

        // Check forward and reverse against word list
        for (let i = 0; i < words.length; i++) {
            if (foundWords[i]) continue;
            const w = words[i].word;
            if (selectedWord === w || selectedWord === w.split('').reverse().join('')) {
                // Found!
                foundWords[i] = true;
                markFound(i);
                updateFoundCount();
                playCorrectSound();
                checkWin();
                return true;
            }
        }
        return false;
    }

    function markFound(wordIdx) {
        // If this is the currently hinted word, stop the hint animation
        if (wordIdx === hintWordIdx) clearHint();

        const w = words[wordIdx];
        // Mark cells in the grid
        for (let i = 0; i < w.word.length; i++) {
            const r = w.row + w.dr * i;
            const c = w.col + w.dc * i;
            const el = getCellEl(r, c);
            if (el) {
                el.classList.add('found');
                el.classList.remove('selecting', 'selected');
            }
        }
        // Mark word in list
        const listItems = document.getElementById('wordList').children;
        if (listItems[wordIdx]) {
            listItems[wordIdx].classList.add('found');
        }
        // Store rectangle for canvas drawing
        const lastIdx = w.word.length - 1;
        foundRects.push({
            r1: w.row, c1: w.col,
            r2: w.row + w.dr * lastIdx, c2: w.col + w.dc * lastIdx
        });
        redrawCanvas();
    }

    function drawAllFoundRects() {
        const canvas = document.getElementById('selectionCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        if (foundRects.length === 0) return;

        const gridEl = document.getElementById('grid');
        const canvasRect = canvas.getBoundingClientRect();

        // Get the actual cell size from the first cell
        const firstCell = gridEl.children[0];
        if (!firstCell) return;
        const cellRect = firstCell.getBoundingClientRect();
        const cellW = cellRect.width;
        const cellH = cellRect.height;

        const pad = Math.min(cellW, cellH) * 0.10;
        const radius = Math.min(cellW, cellH) * 0.28;

        ctx.strokeStyle = '#2E7D32';
        ctx.lineWidth = 3;
        ctx.lineJoin = 'round';

        for (const rect of foundRects) {
            const rMin = Math.min(rect.r1, rect.r2);
            const rMax = Math.max(rect.r1, rect.r2);
            const cMin = Math.min(rect.c1, rect.c2);
            const cMax = Math.max(rect.c1, rect.c2);
            const isDiagonal = (rect.r1 !== rect.r2 && rect.c1 !== rect.c2);

            if (isDiagonal) {
                // For diagonals: draw a rotated rectangle hugging the word's slant
                const first = gridEl.children[rect.r1 * gridSize + rect.c1];
                const last = gridEl.children[rect.r2 * gridSize + rect.c2];
                if (!first || !last) continue;

                const f = first.getBoundingClientRect();
                const l = last.getBoundingClientRect();

                // Centers of first and last cells (canvas coords)
                const cx1 = f.left + f.width / 2 - canvasRect.left;
                const cy1 = f.top + f.height / 2 - canvasRect.top;
                const cx2 = l.left + l.width / 2 - canvasRect.left;
                const cy2 = l.top + l.height / 2 - canvasRect.top;

                // Midpoint of the diagonal line
                const mx = (cx1 + cx2) / 2;
                const my = (cy1 + cy2) / 2;

                // Distance from first center to last center
                const dx = cx2 - cx1;
                const dy = cy2 - cy1;
                const dist = Math.sqrt(dx * dx + dy * dy);
                const angle = Math.atan2(dy, dx);

                const wordLen = Math.abs(rect.r2 - rect.r1) + 1;
                const cellDim = Math.min(cellW, cellH);
                const rw = dist + cellDim - pad * 2;   // rectangle width
                const rh = cellDim - pad * 2;            // rectangle height

                ctx.save();
                ctx.translate(mx, my);
                ctx.rotate(angle);
                ctx.beginPath();
                ctx.moveTo(-rw / 2 + radius, -rh / 2);
                ctx.lineTo(rw / 2 - radius, -rh / 2);
                ctx.arcTo(rw / 2, -rh / 2, rw / 2, -rh / 2 + radius, radius);
                ctx.lineTo(rw / 2, rh / 2 - radius);
                ctx.arcTo(rw / 2, rh / 2, rw / 2 - radius, rh / 2, radius);
                ctx.lineTo(-rw / 2 + radius, rh / 2);
                ctx.arcTo(-rw / 2, rh / 2, -rw / 2, rh / 2 - radius, radius);
                ctx.lineTo(-rw / 2, -rh / 2 + radius);
                ctx.arcTo(-rw / 2, -rh / 2, -rw / 2 + radius, -rh / 2, radius);
                ctx.closePath();
                ctx.stroke();
                ctx.restore();
            } else {
                // Horizontal or vertical: simple axis-aligned bounding box
                const topLeft = gridEl.children[rMin * gridSize + cMin];
                const bottomRight = gridEl.children[rMax * gridSize + cMax];
                if (!topLeft || !bottomRight) continue;

                const tl = topLeft.getBoundingClientRect();
                const br = bottomRight.getBoundingClientRect();

                const x = tl.left - canvasRect.left + pad;
                const y = tl.top - canvasRect.top + pad;
                const w = br.right - tl.left - pad * 2;
                const h = br.bottom - tl.top - pad * 2;

                ctx.beginPath();
                ctx.moveTo(x + radius, y);
                ctx.lineTo(x + w - radius, y);
                ctx.arcTo(x + w, y, x + w, y + radius, radius);
                ctx.lineTo(x + w, y + h - radius);
                ctx.arcTo(x + w, y + h, x + w - radius, y + h, radius);
                ctx.lineTo(x + radius, y + h);
                ctx.arcTo(x, y + h, x, y + h - radius, radius);
                ctx.lineTo(x, y + radius);
                ctx.arcTo(x, y, x + radius, y, radius);
                ctx.closePath();
                ctx.stroke();
            }
        }
    }

    function redrawCanvas() {
        const canvas = document.getElementById('selectionCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawAllFoundRects();
    }

    function flashError() {
        // Cancel any pending flash cleanup
        if (flashTimer) { clearTimeout(flashTimer); flashTimer = null; }

        // Add error class to all selected cells
        for (const cell of selCells) {
            const el = getCellEl(cell.r, cell.c);
            if (el) {
                // Remove selecting, add error (preserve found if applicable)
                el.classList.remove('selecting', 'selected');
                if (!(solution[cell.r][cell.c] !== null && solution[cell.r][cell.c] >= 0 && foundWords[solution[cell.r][cell.c]])) {
                    el.classList.add('error');
                }
            }
        }

        // After 3 flashes (0.35s * 3 = 1.05s), clean up
        flashTimer = setTimeout(() => {
            clearSelection();
            selStart = null;
            selEnd = null;
            flashTimer = null;
        }, 1100);
    }

    // ---- Grid-level Pointer Helpers ----
    function cellFromPoint(e) {
        const gridEl = document.getElementById('grid');
        const rect = gridEl.getBoundingClientRect();
        const cellSize = rect.width / gridSize;
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const c = Math.floor(x / cellSize);
        const r = Math.floor(y / cellSize);
        if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) return null;
        return { r, c };
    }

    function lineIsValid(start, end) {
        const dr = end.r - start.r;
        const dc = end.c - start.c;
        return (dr === 0 && dc !== 0) || (dc === 0 && dr !== 0) || (Math.abs(dr) === Math.abs(dc) && dr !== 0);
    }

    // ---- Selection Canvas Drawing ----
    function clearSelectionLine() {
        redrawCanvas();
    }

    function drawSelectionLine(e) {
        const canvas = document.getElementById('selectionCanvas');
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawAllFoundRects();

        if (!selStart) return;
        if (!pendingSelection && !dragActive) return;

        const gridEl = document.getElementById('grid');
        const gridRect = gridEl.getBoundingClientRect();
        const cellSize = gridRect.width / gridSize;

        // Start cell center in canvas coords
        const sx = selStart.c * cellSize + cellSize / 2;
        const sy = selStart.r * cellSize + cellSize / 2;

        // Pointer position in canvas coords
        const ex = e.clientX - gridRect.left;
        const ey = e.clientY - gridRect.top;

        ctx.strokeStyle = 'rgba(255, 179, 0, 0.85)';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([6, 4]);
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(sx, sy);
        ctx.lineTo(ex, ey);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw a small dot at the start cell center
        ctx.fillStyle = 'rgba(255, 179, 0, 0.85)';
        ctx.beginPath();
        ctx.arc(sx, sy, 3, 0, Math.PI * 2);
        ctx.fill();
    }

    // ---- Selection Helpers ----
    function cancelSelection() {
        clearSelection();
        clearSelectionLine();
        selStart = null;
        selEnd = null;
        pendingSelection = false;
        dragActive = false;
        pointerIsDown = false;
    }

    function finalizeSelection() {
        if (!selStart || !selEnd) return;

        const dr = selEnd.r - selStart.r;
        const dc = selEnd.c - selStart.c;
        const isH = (dr === 0 && dc !== 0);
        const isV = (dc === 0 && dr !== 0);
        const isD = (Math.abs(dr) === Math.abs(dc) && dr !== 0);

        if (isH || isV || isD) {
            highlightSelection();
            const found = checkSelection();
            if (found) {
                clearSelection();
                clearSelectionLine();
            } else {
                clearSelectionLine();
                flashError();
            }
        } else {
            clearSelection();
            clearSelectionLine();
        }

        selStart = null;
        selEnd = null;
        pendingSelection = false;
        dragActive = false;
        pointerIsDown = false;
    }

    // ---- Grid-level Pointer Events ----
    function onGridPointerDown(e) {
        e.preventDefault();
        const gridEl = document.getElementById('grid');
        gridEl.setPointerCapture(e.pointerId);

        if (flashTimer) { clearTimeout(flashTimer); flashTimer = null; }

        const cell = cellFromPoint(e);
        if (!cell) return;
        const { r, c } = cell;

        pointerIsDown = true;
        dragActive = false;
        dragStartR = r;
        dragStartC = c;

        if (pendingSelection && selStart) {
            // Second click — finalize
            if (selStart.r === r && selStart.c === c) {
                // Same cell — cancel
                cancelSelection();
            } else {
                selEnd = { r, c };
                if (lineIsValid(selStart, selEnd)) {
                    finalizeSelection();
                } else {
                    // Invalid line — move start
                    clearSelection();
                    clearSelectionLine();
                    selStart = { r, c };
                    selEnd = null;
                    getCellEl(r, c).classList.add('start-marker');
                }
            }
        } else {
            // First click — set start
            clearSelection();
            clearSelectionLine();
            selStart = { r, c };
            selEnd = null;
            pendingSelection = true;
            getCellEl(r, c).classList.add('start-marker');
        }
    }

    function onGridPointerMove(e) {
        const cell = cellFromPoint(e);

        if (pendingSelection && selStart) {
            // Show line indicator and preview highlight
            drawSelectionLine(e);

            if (cell) {
                const { r, c } = cell;
                if (selStart.r !== r || selStart.c !== c) {
                    if (lineIsValid(selStart, { r, c })) {
                        selEnd = { r, c };
                        highlightCellsInLine(selStart, selEnd);
                    } else {
                        clearCellHighlights();
                        selEnd = null;
                    }
                } else {
                    // Cursor back on start cell — clear any lingering highlights
                    clearCellHighlights();
                    selEnd = null;
                }
            }
        }

        if (pointerIsDown && cell) {
            const { r, c } = cell;
            if (!dragActive && (dragStartR !== r || dragStartC !== c)) {
                dragActive = true;
                // Clear tap start-marker since we're dragging
                if (selStart) {
                    const el = getCellEl(selStart.r, selStart.c);
                    if (el) el.classList.remove('start-marker');
                }
                pendingSelection = false;
            }
            if (dragActive) {
                selEnd = { r, c };
                drawSelectionLine(e);
                if (lineIsValid(selStart, selEnd)) {
                    highlightSelection();
                } else {
                    clearSelection();
                }
            }
        }
    }

    function onGridPointerUp(e) {
        if (!pointerIsDown) return;
        pointerIsDown = false;

        if (dragActive) {
            // Drag ended — finalize
            const cell = cellFromPoint(e);
            if (cell) {
                selEnd = { r: cell.r, c: cell.c };
            }
            finalizeSelection();
            return;
        }

        // Tap — already handled in pointerdown; nothing to do here
    }

    // ---- Cell Highlight Helpers ----
    function clearCellHighlights() {
        for (const cell of selCells) {
            const el = getCellEl(cell.r, cell.c);
            if (el) {
                el.classList.remove('selecting', 'selected', 'error');
                if (solution[cell.r][cell.c] !== null && solution[cell.r][cell.c] >= 0 && foundWords[solution[cell.r][cell.c]]) {
                    el.classList.add('found');
                }
            }
        }
        selCells = [];
    }

    function highlightCellsInLine(start, end) {
        if (!start || !end) return;

        // Clear any previous preview highlights first
        clearCellHighlights();

        const dr = end.r - start.r;
        const dc = end.c - start.c;
        let stepR = 0, stepC = 0;
        if (dr === 0 && dc !== 0) { stepR = 0; stepC = dc > 0 ? 1 : -1; }
        else if (dc === 0 && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = 0; }
        else if (Math.abs(dr) === Math.abs(dc) && dr !== 0) { stepR = dr > 0 ? 1 : -1; stepC = dc > 0 ? 1 : -1; }
        else return;

        let r = start.r, c = start.c;
        while (true) {
            if (r < 0 || r >= gridSize || c < 0 || c >= gridSize) break;
            selCells.push({ r, c });
            const el = getCellEl(r, c);
            if (el) {
                if (solution[r][c] !== null && solution[r][c] >= 0 && foundWords[solution[r][c]]) {
                    el.classList.add('found');
                } else {
                    el.classList.add('selecting');
                }
            }
            if (r === end.r && c === end.c) break;
            r += stepR;
            c += stepC;
        }
    }

    // ---- Game Logic ----
    function setDifficulty(diff) {
        if (currentDifficulty === diff) return;
        currentDifficulty = diff;
        // Update difficulty bar
        document.querySelectorAll('.diff-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.diff === diff);
        });
        saveSettings();
        startNewGame();
    }

    function newGame() {
        // Ask for category first, then start
        openCategoryPicker();
    }

    function startNewGame() {
        generatePuzzle();
        foundRects = [];
        hintsRemaining = (currentDifficulty === 'insane') ? 0 : 3;
        hintWordIdx = -1;
        gameSeconds = 0;
        document.getElementById('timerDisplay').textContent = '⏱ 0:00';
        startTimer();
        if (hintTimer) { clearTimeout(hintTimer); hintTimer = null; }
        renderAll();
        updateHintDisplay();
        selStart = null;
        selEnd = null;
        selCells = [];
        pendingSelection = false;
        dragActive = false;
        pointerIsDown = false;
        if (flashTimer) { clearTimeout(flashTimer); flashTimer = null; }
        clearSelectionLine();
        saveGame();
    }

    function checkWin() {
        if (foundWords.every(Boolean)) {
            stats.wins++;
            stats.streak++;
            if (stats.streak > stats.bestStreak) stats.bestStreak = stats.streak;
            saveStats();
            showCelebration();
        }
    }

    function clearHint() {
        if (hintTimer) { clearTimeout(hintTimer); hintTimer = null; }
        if (hintWordIdx < 0) return;
        const w = words[hintWordIdx];
        if (w) {
            for (let i = 0; i < w.word.length; i++) {
                const r = w.row + w.dr * i;
                const c = w.col + w.dc * i;
                const el = getCellEl(r, c);
                if (el) {
                    el.classList.remove('hint');
                    if (solution[r][c] !== null && solution[r][c] >= 0 && foundWords[solution[r][c]]) {
                        el.classList.add('found');
                    }
                }
            }
        }
        hintWordIdx = -1;
    }

    function useHint() {
        if (currentDifficulty === 'insane') return;  // hints are disabled on Insane
        if (hintsRemaining <= 0) return;
        if (hintTimer) return;  // hint already active

        // Find unfound words
        const unfound = [];
        for (let i = 0; i < words.length; i++) {
            if (!foundWords[i]) unfound.push(i);
        }
        if (unfound.length === 0) return;

        // Pick a random unfound word
        const idx = unfound[Math.floor(Math.random() * unfound.length)];
        const w = words[idx];
        hintWordIdx = idx;

        // Flash its cells with the hint animation
        for (let i = 0; i < w.word.length; i++) {
            const r = w.row + w.dr * i;
            const c = w.col + w.dc * i;
            const el = getCellEl(r, c);
            if (el) {
                el.classList.add('hint');
            }
        }

        hintsRemaining--;
        updateHintDisplay();
        saveGame();

        // Clear hint after 5 seconds
        hintTimer = setTimeout(() => {
            clearHint();
        }, 5100);
    }

    function updateHintDisplay() {
        const insane = currentDifficulty === 'insane';
        document.getElementById('hintsLeft').textContent = insane ? 0 : hintsRemaining;
        document.getElementById('hintCount').textContent = insane ? 0 : hintsRemaining;
        const btn = document.getElementById('btnHint');
        if (btn) btn.disabled = insane || hintsRemaining <= 0;
    }

    function showCelebration() {
        stopTimer();
        document.getElementById('celeTime').textContent = fmtTime(gameSeconds);
        document.getElementById('celebrationOverlay').classList.remove('hidden');
        spawnConfetti();
        playFanfare();
    }

    function closeCelebration() {
        document.getElementById('celebrationOverlay').classList.add('hidden');
    }

    function spawnConfetti() {
        OEFENPAD.spawnConfetti({
            container: 'confettiContainer',
            colors: ['#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', '#FF8C42', '#C084FC', '#F472B6'],
            count: 80,
            duration: [2, 4],
            delay: [0, 0.8],
            top: [-25, -5],
            topUnit: '%'
        });
    }

    // ---- Persistence ----
    function saveGame() {
        try {
            const data = {
                v: SAVE_VERSION,
                grid,
                solution,
                words,
                foundWords,
                foundRects,
                hintsRemaining,
                difficulty: currentDifficulty,
                category: currentCategory,
                gridSize
            };
            localStorage.setItem('oefenpad-woordzoeker-game', JSON.stringify(data));
        } catch (e) { /* quota exceeded, ignore */ }
    }

    function loadGame() {
        try {
            const raw = localStorage.getItem('oefenpad-woordzoeker-game');
            if (!raw) return false;
            const data = JSON.parse(raw);
            if (data.v !== SAVE_VERSION) return false;
            if (data.difficulty && data.difficulty !== currentDifficulty) return false;
            if (data.category && data.category !== currentCategory) return false;
            grid = data.grid;
            solution = data.solution;
            words = data.words;
            foundWords = data.foundWords || new Array(words.length).fill(false);
            foundRects = data.foundRects || [];
            hintsRemaining = (data.hintsRemaining !== undefined) ? data.hintsRemaining : 3;
            gridSize = data.gridSize || grid.length;
            return true;
        } catch (e) {
            return false;
        }
    }

    function saveStats() {
        try {
            localStorage.setItem('oefenpad-woordzoeker-stats', JSON.stringify(stats));
        } catch (e) { /* ignore */ }
    }

    function loadStats() {
        try {
            const raw = localStorage.getItem('oefenpad-woordzoeker-stats');
            if (raw) {
                const saved = JSON.parse(raw);
                stats.wins = saved.wins || 0;
                stats.streak = saved.streak || 0;
                stats.bestStreak = saved.bestStreak || 0;
            }
        } catch (e) { /* ignore */ }
    }

    function saveSettings() {
        try {
            const data = Object.assign({}, settings, {
                difficulty: currentDifficulty,
                category: currentCategory
            });
            localStorage.setItem('oefenpad-woordzoeker-settings', JSON.stringify(data));
        } catch (e) { /* ignore */ }
    }

    function loadSettings() {
        try {
            const raw = localStorage.getItem('oefenpad-woordzoeker-settings');
            if (raw) {
                const saved = JSON.parse(raw);
                settings.soundEffects = saved.soundEffects !== false;
                if (typeof saved.translateTo === 'string') {
                    settings.translateTo = saved.translateTo;
                    translateTo = saved.translateTo;
                }
                if (saved.difficulty && DIFFICULTIES[saved.difficulty]) {
                    currentDifficulty = saved.difficulty;
                }
                if (saved.category && CATEGORIES[saved.category]) {
                    currentCategory = saved.category;
                }
            }
        } catch (e) { /* ignore */ }
    }

    // ---- Settings ----
    function openSettings() {
        document.getElementById('settingsOverlay').classList.remove('hidden');
        document.getElementById('settingSoundEffects').checked = settings.soundEffects;
        buildTranslateSelect();
    }

    // The puzzle's own language is never offered as a translation, so the
    // options depend on the current language and are rebuilt each time.
    const TRANSLATE_LANGS = [
        { code: 'en', name: 'English' },
        { code: 'nl', name: 'Nederlands' },
        { code: 'uk', name: 'Українська' }
    ];
    function buildTranslateSelect() {
        const sel = document.getElementById('settingTranslateTo');
        if (!sel) return;
        sel.innerHTML = '';
        const off = document.createElement('option');
        off.value = '';
        off.textContent = T('translate-off');
        sel.appendChild(off);
        for (const l of TRANSLATE_LANGS) {
            if (l.code === wordsLang()) continue;
            const o = document.createElement('option');
            o.value = l.code;
            o.textContent = l.name;
            o.lang = l.code;
            sel.appendChild(o);
        }
        sel.value = translateTo;
    }

    function closeSettings() {
        document.getElementById('settingsOverlay').classList.add('hidden');
    }

    function showAbout() {
        closeSettings();
        document.getElementById('aboutOverlay').classList.remove('hidden');
    }

    function closeAbout() {
        document.getElementById('aboutOverlay').classList.add('hidden');
    }

    // ---- Category Picker ----
    function buildCategoryGrid() {
        const grid = document.getElementById('categoryGrid');
        grid.innerHTML = '';

        const available = Object.keys(CATEGORIES).filter(k => catWords(CATEGORIES[k]).length > 0);
        if (available.indexOf(currentCategory) === -1 && available.length) {
            currentCategory = DEFAULT_CATEGORY;
        }

        for (const key of available) {
            const cat = CATEGORIES[key];
            const btn = document.createElement('button');
            btn.className = 'cat-btn';
            btn.innerHTML = cat.icon + '<span>' + catLabel(cat) + '</span>';
            btn.addEventListener('click', () => selectCategory(key));
            grid.appendChild(btn);
        }

        // Random button
        const randBtn = document.createElement('button');
        randBtn.className = 'cat-btn random-btn';
        randBtn.innerHTML = '🎲<span>' + T('random-cat') + '</span>';
        randBtn.addEventListener('click', () => {
            if (available.length) {
                selectCategory(available[Math.floor(Math.random() * available.length)]);
            }
        });
        grid.appendChild(randBtn);
    }

    function selectCategory(key) {
        if (!CATEGORIES[key]) return;
        currentCategory = key;
        saveSettings();
        closeCategoryPicker();
        startNewGame();
    }

    function openCategoryPicker() {
        document.getElementById('categoryOverlay').classList.remove('hidden');
    }

    function closeCategoryPicker() {
        document.getElementById('categoryOverlay').classList.add('hidden');
    }

    function updateSetting(key, value) {
        settings[key] = value;
        saveSettings();
    }

    // Translation mode only uses words that have a translation, so the word
    // pool — and with it the puzzle — changes. Warn first if the player has
    // already found something, the same way a language change does.
    function setTranslateTo(value) {
        if (value === translateTo) return;
        prevTranslateTo = translateTo;
        translateTo = value;
        settings.translateTo = value;
        saveSettings();
        if (foundWords.some(Boolean)) {
            pendingTranslateRevert = true;
            document.getElementById('langConfirmOverlay').classList.remove('hidden');
        } else {
            buildCategoryGrid();   // a category with no translations drops out
            startNewGame();
        }
    }

    // ---- Audio ----
    // Shared AudioContext (created lazily, resumed on each access).
    const getAudioContext = OEFENPAD.audioContext;

    function playCorrectSound() {
        if (!settings.soundEffects) return;
        try {
            const ctx = getAudioContext();
            const now = ctx.currentTime;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(523, now);
            osc.frequency.setValueAtTime(659, now + 0.1);
            osc.frequency.setValueAtTime(784, now + 0.2);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.4);
        } catch (e) { /* ignore */ }
    }

    function playFanfare() {
        if (!settings.soundEffects) return;
        try {
            const ctx = getAudioContext();
            const notes = [523, 659, 784, 1047];
            const startTime = ctx.currentTime;
            notes.forEach((freq, i) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, startTime + i * 0.15);
                gain.gain.setValueAtTime(0.12, startTime + i * 0.15);
                gain.gain.exponentialRampToValueAtTime(0.01, startTime + i * 0.15 + 0.3);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(startTime + i * 0.15);
                osc.stop(startTime + i * 0.15 + 0.3);
            });
        } catch (e) { /* ignore */ }
    }

    // ---- Splash Screen ----
    function hideSplash() { OEFENPAD.hideSplash('splashScreen', 500); }

    // ---- Init ----
    function init() {
        loadSettings();
        loadStats();
        buildCategoryGrid();

        // Highlight the active difficulty button
        document.querySelectorAll('.diff-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.diff === currentDifficulty);
            btn.addEventListener('click', () => setDifficulty(btn.dataset.diff));
        });

        const hasVisited = localStorage.getItem('oefenpad-woordzoeker-visited');
        if (!hasVisited) {
            localStorage.setItem('oefenpad-woordzoeker-visited', '1');
            // First visit — show category picker after splash
            setTimeout(() => {
                hideSplash();
                setTimeout(() => openCategoryPicker(), 300);
            }, 2000);
        }

        const loaded = loadGame();
        if (!loaded) {
            generatePuzzle();
        } else {
            // Redraw found rectangles from loaded state
            setTimeout(() => redrawCanvas(), 100);
        }
        renderAll();
        updateHintDisplay();

        // Tap a word to show its translation; hovering does the same in CSS.
        document.getElementById('wordList').addEventListener('click', (e) => {
            const li = e.target.closest ? e.target.closest('li.has-translation') : null;
            if (li) li.classList.toggle('revealed');
        });

        // Grid-level pointer events
        const gridEl = document.getElementById('grid');
        gridEl.addEventListener('pointerdown', onGridPointerDown);
        gridEl.addEventListener('pointermove', onGridPointerMove);
        gridEl.addEventListener('pointerup', onGridPointerUp);
        gridEl.addEventListener('contextmenu', (e) => { e.preventDefault(); if (pendingSelection) cancelSelection(); });

        // Global pointerup for release outside grid
        document.addEventListener('pointerup', () => {
            if (pointerIsDown && dragActive) {
                finalizeSelection();
            }
        });

        // ESC to cancel
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && pendingSelection) {
                cancelSelection();
            }
        });

        // Splash screen
        const splash = document.getElementById('splashScreen');
        splash.addEventListener('click', hideSplash);
        setTimeout(hideSplash, 2500);

        // Warn before leaving the page with a puzzle in progress
        window.addEventListener('beforeunload', (e) => {
            if (foundWords.some(Boolean)) { e.preventDefault(); e.returnValue = ''; }
        });
    }

    // Language switch: rebuild labels; if a game is in progress (at least one word
    // found), warn before regenerating the puzzle in the new language.
    // The English word lists are shared by UK and US English, so switching between
    // them only rebuilds labels — only a change to/from a language with different
    // word lists (Dutch or Ukrainian) restarts the puzzle.
    function wordsLang() { return (I18N.lang === 'en' || I18N.lang === 'en-us') ? 'en' : I18N.lang; }
    let lastWordsLang = wordsLang();
    document.addEventListener('i18nchange', function () {
        if (translateTo === wordsLang()) {
            translateTo = '';
            settings.translateTo = '';
            saveSettings();
        }
        buildTranslateSelect();
        buildCategoryGrid();
        if (wordsLang() === lastWordsLang) return;
        lastWordsLang = wordsLang();
        if (foundWords.some(Boolean)) {
            document.getElementById('langConfirmOverlay').classList.remove('hidden');
        } else {
            startNewGame();
        }
    });

    function confirmLangChange() {
        document.getElementById('langConfirmOverlay').classList.add('hidden');
        pendingTranslateRevert = false;
        buildCategoryGrid();
        startNewGame();
    }

    function cancelLangChange() {
        document.getElementById('langConfirmOverlay').classList.add('hidden');
        if (!pendingTranslateRevert) return;
        // Keep playing: put the translation setting back as it was.
        pendingTranslateRevert = false;
        translateTo = prevTranslateTo;
        settings.translateTo = translateTo;
        saveSettings();
        buildTranslateSelect();
        renderWordList();
    }

    document.addEventListener('DOMContentLoaded', init);

// DEV-ONLY-START
// Dev shortcut: Ctrl+Alt+W instantly completes the game (Insane level only).
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.altKey && (e.key === 'w' || e.key === 'W')) {
        e.preventDefault();
        if (currentDifficulty !== 'insane') return;
        for (let i = 0; i < words.length; i++) {
            if (!foundWords[i]) markFound(i);
        }
        updateFoundCount();
        renderWordList();
        checkWin();
    }
});
// DEV-ONLY-END

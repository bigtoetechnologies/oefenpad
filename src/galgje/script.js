    /* =================================================================
       Galgje — Oefenpad
       ================================================================= */

    const I18N = window.I18N || { lang: 'nl', t: function () { return null; }, register: function () {} };
    const WORDS = window.OEFENPAD_WORDS || {};
    const IMAGES = window.OEFENPAD_WORD_IMAGES || {};

    const TEXTS = {
        'page-title':    { en: 'Galgje — Oefenpad', nl: 'Galgje — Oefenpad', uk: 'Шибениця — Oefenpad' },
        'splash-title':  { en: 'Hangman', nl: 'Galgje', uk: 'Шибениця' },
        'app-title':     { en: 'Hangman', nl: 'Galgje', uk: 'Шибениця' },
        'settings-title':{ en: '⚙️ Settings', nl: '⚙️ Instellingen', uk: '⚙️ Налаштування' },
        'sound-effects': { en: '🔊 Sound Effects', nl: '🔊 Geluidseffecten', uk: '🔊 Звукові ефекти' },
        'translate-label': { en: '🌍 Translate words', nl: '🌍 Woorden vertalen', uk: '🌍 Перекладати слова' },
        'translate-off': { en: 'Off', nl: 'Uit', uk: 'Вимкнено' },
        'translate-hint': { en: 'Tap the word to show its translation. Only words that have a translation are used.', nl: 'Tik op het woord om de vertaling te zien. Alleen woorden met een vertaling worden gebruikt.', uk: 'Торкніться слова, щоб побачити переклад. Використовуються лише слова, які мають переклад.' },
        'translate-aria': { en: 'Press Enter to show the translation', nl: 'Druk op Enter om de vertaling te tonen', uk: 'Натисніть Enter, щоб побачити переклад' },
        'close':         { en: 'Close', nl: 'Sluiten', uk: 'Закрити' },
        'diff-easy':     { en: 'Easy', nl: 'Makkelijk', uk: 'Легкий' },
        'diff-medium':   { en: 'Medium', nl: 'Gemiddeld', uk: 'Середній' },
        'diff-hard':     { en: 'Hard', nl: 'Moeilijk', uk: 'Складний' },
        'cat-title':     { en: 'Choose a Category', nl: 'Kies een categorie', uk: 'Оберіть категорію' },
        'cat-subtitle':  { en: 'Select a theme for your word:', nl: 'Kies een thema voor je woord:', uk: 'Виберіть тему для слова:' },
        'random-cat':    { en: 'Random Category', nl: 'Willekeurige categorie', uk: 'Випадкова категорія' },
        'btn-hint':      { en: '💡 Hint', nl: '💡 Hint', uk: '💡 Підказка' },
        'btn-new':       { en: '🎲 New Game', nl: '🎲 Nieuw spel', uk: '🎲 Нова гра' },
        'cele-title':    { en: 'You Saved Him!', nl: 'Je hebt hem gered!', uk: 'Ти його врятував!' },
        'cele-msg':      { en: 'Great job! You guessed the word.', nl: 'Goed gedaan! Je hebt het woord geraden.', uk: 'Чудова робота! Ти вгадав слово.' },
        'time-label':    { en: 'Time:', nl: 'Tijd:', uk: 'Час:' },
        'streak-label':  { en: '🔥 Streak:', nl: '🔥 Reeks:', uk: '🔥 Серія:' },
        'lose-title':    { en: 'Game Over', nl: 'Game over', uk: 'Кінець гри' },
        'lose-msg':      { en: 'The word was:', nl: 'Het woord was:', uk: 'Слово було:' },
        'btn-close':     { en: '✕ Close', nl: '✕ Sluiten', uk: '✕ Закрити' },
        'confirm-new-title': { en: 'Start a New Game?', nl: 'Nieuw spel starten?', uk: 'Почати нову гру?' },
        'confirm-new-msg':   { en: 'This will start a new game. Your current progress will be lost.', nl: 'Dit start een nieuw spel. Je huidige voortgang gaat verloren.', uk: 'Це почне нову гру. Поточний прогрес буде втрачено.' },
        'confirm-ok':        { en: 'Start New Game', nl: 'Nieuw spel starten', uk: 'Почати нову гру' },
        'cancel':        { en: 'Cancel', nl: 'Annuleren', uk: 'Скасувати' },
        'version':       { en: 'Version 0.1.0', nl: 'Versie 0.1.0', uk: 'Версія 0.1.0' }
    };
    I18N.register('galgje', TEXTS);

    function T(key, vars) { return I18N.t(key, vars) || (TEXTS[key] ? TEXTS[key].en : key); }
    function wordsLang() { return (I18N.lang === 'en' || I18N.lang === 'en-us') ? 'en' : I18N.lang; }
    function catLabel(cat) { return cat.label[I18N.lang] || cat.label.en; }

    // ---- Per-language alphabets & keyboard layouts ----
    const ALPHABETS = {
        en: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        nl: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        uk: 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    };
    const KEYBOARD_ROWS = {
        en: ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'],
        nl: ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'],
        uk: ['ЙЦУКЕНГШЩЗХЇ', 'ФІВАПРОЛДЖЄ', 'ЯЧСМИТЬБЮ']
    };

    const DIFFICULTIES = {
        easy:   { maxLen: 5 },
        medium: { maxLen: 8 },
        hard:   { maxLen: 99 }
    };
    const MAX_WRONG = 10;

    // ---- Game state ----
    let state = {
        category: 'animals',
        difficulty: 'medium',
        word: '',
        wordLang: 'en',
        guessed: [],
        wrong: 0,
        hintsLeft: 2,
        status: 'playing',   // playing | won | lost
        seconds: 0
    };
    let lastWord = '';
    let timerInterval = null;
    let settings = { soundEffects: true, translateTo: '' };
    let stats = { wins: 0, losses: 0, streak: 0, bestStreak: 0 };

    // Translation hint. The player can choose a language they already know;
    // tapping the word row then reveals what the hidden word means. Only
    // words that have a translation are picked while this is on.
    let translateTo = '';
    let translationShown = false;

    // ---------- Utilities ----------
    function lettersOnly(w) { return w.replace(/[^\p{L}]/gu, ''); }

    // Shared helpers live in src/shared/common.js
    function shuffle(arr) { return OEFENPAD.shuffle(arr); }

    function availableCategories() {
        const lang = wordsLang();
        return Object.keys(WORDS).filter(function (k) {
            return catEntries(k, lang).length > 0;
        });
    }

    // Entries in the current language. In translation mode, entries without a
    // translation are dropped, the same rule Word Search follows, so every
    // word picked can be looked up in the player's own language.
    function catEntries(key, lang) {
        const cat = WORDS[key];
        if (!cat) return [];
        const entries = OEFENPAD.entries(cat, lang);
        if (!translateTo || translateTo === lang) return entries;
        return entries.filter(function (e) { return !!e[translateTo]; });
    }

    function translationFor(word) {
        if (!word || !translateTo || translateTo === wordsLang()) return '';
        const lang = state.wordLang || wordsLang();
        const entries = OEFENPAD.entries(WORDS[state.category] || {}, lang);
        for (let i = 0; i < entries.length; i++) {
            if (entries[i][lang] === word) return entries[i][translateTo] || '';
        }
        return '';
    }

    // The picture clue for the current word, as '<category>/<slug>.jpg'.
    // Only categories that have word images (animals, food, household)
    // return anything; the clue element simply stays hidden otherwise.
    function imageForWord(word) {
        const lang = state.wordLang || wordsLang();
        const entries = OEFENPAD.entries(WORDS[state.category] || {}, lang);
        for (let i = 0; i < entries.length; i++) {
            if (entries[i][lang] !== word) continue;
            return IMAGES[entries[i].en] || '';
        }
        return '';
    }

    function renderClue() {
        const el = document.getElementById('wordClue');
        if (!el) return;
        const img = imageForWord(state.word);
        if (img) {
            el.innerHTML = '<img src="../../assets/wordimages/' + img + '" alt="">';
            el.classList.remove('hidden');
        } else {
            el.innerHTML = '';
            el.classList.add('hidden');
        }
    }

    function setPopupImage(id, word) {
        const el = document.getElementById(id);
        if (!el) return;
        const img = imageForWord(word);
        if (img) {
            el.src = '../../assets/wordimages/' + img;
            el.classList.remove('hidden');
        } else {
            el.removeAttribute('src');
            el.classList.add('hidden');
        }
    }

    function fmtTime(seconds) { return OEFENPAD.fmtTime(seconds); }

    // ---------- Word picking ----------
    function pickWord() {
        const lang = wordsLang();
        const entries = catEntries(state.category, lang);
        if (!entries.length) return '';
        const maxLen = DIFFICULTIES[state.difficulty].maxLen;
        let eligible = entries.filter(function (e) {
            const n = lettersOnly(e[lang]).length;
            return n >= 3 && n <= maxLen;
        });
        // Prefer words with a picture clue; the whole point of the clue is
        // that the meaning is visible while the spelling is not. Categories
        // without images simply keep every word.
        const withImage = eligible.filter(function (e) { return !!IMAGES[e.en]; });
        if (withImage.length) eligible = withImage;
        if (!eligible.length) return entries[0][lang];
        let word = eligible[Math.floor(Math.random() * eligible.length)][lang];
        if (word === lastWord && eligible.length > 1) {
            word = eligible[Math.floor(Math.random() * eligible.length)][lang];
        }
        lastWord = word;
        return word;
    }

    function startGame() {
        stopTimer();
        state.word = pickWord();
        state.wordLang = wordsLang();
        state.guessed = [];
        state.wrong = 0;
        state.hintsLeft = 2;
        state.status = 'playing';
        state.seconds = 0;
        translationShown = false;
        renderClue();
        renderWordTiles();
        renderKeyboard();
        renderStatus();
        updateHintButton();
        draw();
        startTimer();
        saveGame();
        hideLose();
        closeCelebration();
    }

    function newGame() { startGame(); }

    // ---------- Rendering ----------
    function renderWordTiles() {
        const el = document.getElementById('wordTiles');
        el.innerHTML = '';
        el.setAttribute('role', 'img');
        el.setAttribute('aria-live', 'polite');
        const translation = translationFor(state.word);
        el.setAttribute('aria-label', spokenWord() + (translation ? '. ' + T('translate-aria') : ''));
        if (translation) {
            el.setAttribute('tabindex', '0');
            el.setAttribute('title', T('translate-hint'));
        } else {
            el.removeAttribute('tabindex');
            el.removeAttribute('title');
        }
        for (let i = 0; i < state.word.length; i++) {
            const ch = state.word[i];
            if (ch === ' ') {
                const gap = document.createElement('div');
                gap.className = 'word-gap';
                el.appendChild(gap);
                continue;
            }
            const isLetter = /^\p{L}$/u.test(ch);
            const tile = document.createElement('div');
            tile.className = 'word-tile';
            if (!isLetter || state.guessed.indexOf(ch) !== -1) {
                tile.textContent = ch;
                tile.classList.add('revealed');
            }
            el.appendChild(tile);
        }
        renderTranslation();
    }

    // The translation stays hidden until the word row is tapped, then the same
    // tap hides it again, exactly like a word in Word Search's list.
    function renderTranslation() {
        const tiles = document.getElementById('wordTiles');
        const box = document.getElementById('wordTranslation');
        const translation = translationFor(state.word);
        if (tiles) tiles.classList.toggle('has-translation', !!translation);
        if (!translation) translationShown = false;
        if (!box) return;
        if (translation) {
            box.textContent = translation;
            box.setAttribute('lang', translateTo);
        } else {
            box.textContent = '';
            box.removeAttribute('lang');
        }
        box.classList.toggle('show', !!translation && translationShown);
    }

    function toggleTranslation() {
        if (!translationFor(state.word)) return;
        translationShown = !translationShown;
        renderTranslation();
    }

    // "H, blank, N, G, M, A, N" — the puzzle as it currently stands.
    function spokenWord() {
        const blank = I18N.t('a11y-blank');
        const parts = [];
        for (let i = 0; i < state.word.length; i++) {
            const ch = state.word[i];
            if (ch === ' ') { parts.push(I18N.t('a11y-space') || 'space'); continue; }
            const isLetter = /^\p{L}$/u.test(ch);
            if (!isLetter || state.guessed.indexOf(ch) !== -1) parts.push(ch);
            else parts.push(blank || 'blank');
        }
        return parts.join(', ');
    }

    function renderKeyboard() {
        const el = document.getElementById('keyboard');
        el.setAttribute('role', 'group');
        el.setAttribute('aria-label', I18N.t('a11y-keyboard') || 'Letters');
        const lang = wordsLang();
        const rows = KEYBOARD_ROWS[lang] || KEYBOARD_ROWS.en;
        el.innerHTML = '';
        rows.forEach(function (row) {
            const rowEl = document.createElement('div');
            rowEl.className = 'key-row';
            for (let i = 0; i < row.length; i++) {
                const ch = row[i];
                const btn = document.createElement('button');
                btn.className = 'key-btn';
                btn.textContent = ch;
                btn.dataset.letter = ch;
                const idx = state.guessed.indexOf(ch);
                if (idx !== -1) {
                    btn.disabled = true;
                    const hit = state.word.indexOf(ch) !== -1;
                    btn.classList.add(hit ? 'correct' : 'wrong');
                    btn.setAttribute('aria-label',
                        (I18N.t(hit ? 'a11y-key-hit' : 'a11y-key-miss', { letter: ch })
                         || (ch + (hit ? ', correct' : ', not in the word'))));
                }
                btn.addEventListener('click', function () { guess(ch); });
                rowEl.appendChild(btn);
            }
            el.appendChild(rowEl);
        });
    }

    function renderStatus() {
        const cat = WORDS[state.category];
        document.getElementById('categoryEmoji').textContent = cat ? cat.icon : '';
        document.getElementById('categoryName').textContent = cat ? catLabel(cat) : '';
        document.getElementById('wrongCount').textContent = '❌ ' + state.wrong + '/' + MAX_WRONG;
        document.getElementById('timerDisplay').textContent = '⏱ ' + fmtTime(state.seconds);
        document.getElementById('hintCount').textContent = state.hintsLeft;
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.classList.toggle('active', btn.dataset.diff === state.difficulty);
        });
    }

    function updateHintButton() {
        const btn = document.getElementById('btnHint');
        btn.disabled = state.status !== 'playing' || state.hintsLeft <= 0;
    }

    // ---------- Canvas drawing ----------
    function draw() {
        const canvas = document.getElementById('hangmanCanvas');
        const ctx = canvas.getContext('2d');
        const dark = document.documentElement.classList.contains('dark');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = dark ? '#E0E0E0' : '#455A64';
        ctx.fillStyle = dark ? '#E0E0E0' : '#455A64';
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';

        const wrong = state.wrong;

        // Ground (always visible)
        ctx.beginPath();
        ctx.moveTo(30, 240); ctx.lineTo(120, 240);          // base
        ctx.stroke();

        if (wrong >= 1) { // 1. gallows pole
            ctx.beginPath();
            ctx.moveTo(60, 240); ctx.lineTo(60, 40);
            ctx.stroke();
        }
        if (wrong >= 2) { // 2. crossbar
            ctx.beginPath();
            ctx.moveTo(60, 40);  ctx.lineTo(185, 40);
            ctx.stroke();
        }
        if (wrong >= 3) { // 3. rope
            ctx.beginPath();
            ctx.moveTo(185, 40); ctx.lineTo(185, 75);
            ctx.stroke();
        }
        if (wrong >= 4) { // 4. head
            ctx.beginPath();
            ctx.arc(185, 97, 22, 0, Math.PI * 2);
            ctx.stroke();
        }
        if (wrong >= 5) { // 5. body
            ctx.beginPath();
            ctx.moveTo(185, 119); ctx.lineTo(185, 185);
            ctx.stroke();
        }
        if (wrong >= 6) { // 6. left arm
            ctx.beginPath();
            ctx.moveTo(185, 135); ctx.lineTo(150, 165);
            ctx.stroke();
        }
        if (wrong >= 7) { // 7. right arm
            ctx.beginPath();
            ctx.moveTo(185, 135); ctx.lineTo(220, 165);
            ctx.stroke();
        }
        if (wrong >= 8) { // 8. left leg
            ctx.beginPath();
            ctx.moveTo(185, 185); ctx.lineTo(160, 222);
            ctx.stroke();
        }
        if (wrong >= 9) { // 9. right leg
            ctx.beginPath();
            ctx.moveTo(185, 185); ctx.lineTo(210, 222);
            ctx.stroke();
        }
        if (wrong >= 10) { // 10. X eyes — the man is done for
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(172, 88); ctx.lineTo(182, 98);
            ctx.moveTo(182, 88); ctx.lineTo(172, 98);
            ctx.moveTo(188, 88); ctx.lineTo(198, 98);
            ctx.moveTo(198, 88); ctx.lineTo(188, 98);
            ctx.stroke();
        }
    }

    // ---------- Guessing ----------
    function guess(letter) {
        if (state.status !== 'playing') return;
        if (state.guessed.indexOf(letter) !== -1) return;
        const alphabet = ALPHABETS[wordsLang()] || ALPHABETS.en;
        if (alphabet.indexOf(letter) === -1) return;
        if (isOverlayOpen()) return;

        state.guessed.push(letter);
        if (state.word.indexOf(letter) !== -1) {
            playCorrectSound();
        } else {
            state.wrong++;
            playWrongSound();
        }
        renderWordTiles();
        renderKeyboard();
        renderStatus();
        draw();
        saveGame();

        const allFound = state.word.split('').every(function (ch) { return !/^\p{L}$/u.test(ch) || state.guessed.indexOf(ch) !== -1; });
        if (allFound) {
            winGame();
        } else if (state.wrong >= MAX_WRONG) {
            loseGame();
        }
    }

    function useHint() {
        if (state.status !== 'playing' || state.hintsLeft <= 0) return;
        const unguessed = [];
        for (let i = 0; i < state.word.length; i++) {
            const ch = state.word[i];
            if (/^\p{L}$/u.test(ch) && state.guessed.indexOf(ch) === -1 && unguessed.indexOf(ch) === -1) unguessed.push(ch);
        }
        if (!unguessed.length) return;
        const letter = unguessed[Math.floor(Math.random() * unguessed.length)];
        state.hintsLeft--;
        state.guessed.push(letter);
        renderWordTiles();
        renderKeyboard();
        renderStatus();
        updateHintButton();
        saveGame();

        const allFound = state.word.split('').every(function (ch) { return !/^\p{L}$/u.test(ch) || state.guessed.indexOf(ch) !== -1; });
        if (allFound) winGame();
    }

    function isOverlayOpen() {
        return ['celebrationOverlay', 'loseOverlay', 'settingsOverlay', 'categoryOverlay', 'confirmOverlay']
            .some(function (id) { return !document.getElementById(id).classList.contains('hidden'); });
    }

    // ---------- New-game confirmation ----------
    let pendingNewGame = null;
    let pendingNewGameCancel = null;
    function inProgress() {
        return state.status === 'playing' && state.guessed.length > 0;
    }
    function askNewGame(cb, onCancel) {
        pendingNewGame = cb;
        pendingNewGameCancel = onCancel || null;
        document.getElementById('confirmOverlay').classList.remove('hidden');
    }
    function confirmNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        const cb = pendingNewGame;
        pendingNewGame = null;
        pendingNewGameCancel = null;
        if (cb) cb();
    }
    function cancelNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        pendingNewGame = null;
        const cb = pendingNewGameCancel;
        pendingNewGameCancel = null;
        if (cb) cb();
    }

    // ---------- Win / lose ----------
    function setPopupTranslation(id, translation) {
        const el = document.getElementById(id);
        if (!el) return;
        if (translation) {
            el.textContent = translation;
            el.setAttribute('lang', translateTo);
        } else {
            el.textContent = '';
            el.removeAttribute('lang');
        }
        el.classList.toggle('show', !!translation);
    }

    function winGame() {
        stopTimer();
        state.status = 'won';
        stats.wins++;
        stats.streak++;
        if (stats.streak > stats.bestStreak) stats.bestStreak = stats.streak;
        saveStats();
        saveGame();
        document.getElementById('celeWord').textContent = state.word;
        setPopupImage('celeImage', state.word);
        setPopupTranslation('celeTranslation', translationFor(state.word));
        document.getElementById('celeTime').textContent = fmtTime(state.seconds);
        document.getElementById('celeStreak').textContent = stats.streak;
        document.getElementById('celebrationOverlay').classList.remove('hidden');
        spawnConfetti();
        playFanfare();
    }

    function loseGame() {
        stopTimer();
        state.status = 'lost';
        stats.losses++;
        stats.streak = 0;
        saveStats();
        saveGame();
        document.getElementById('loseWord').textContent = state.word;
        setPopupImage('loseImage', state.word);
        setPopupTranslation('loseTranslation', translationFor(state.word));
        document.getElementById('loseOverlay').classList.remove('hidden');
    }

    function closeCelebration() { document.getElementById('celebrationOverlay').classList.add('hidden'); }
    function closeLose() { document.getElementById('loseOverlay').classList.add('hidden'); }
    function hideLose() { closeLose(); }

    // ---------- Timer ----------
    function startTimer() {
        stopTimer();
        timerInterval = setInterval(function () {
            if (state.status === 'playing') {
                state.seconds++;
                document.getElementById('timerDisplay').textContent = '⏱ ' + fmtTime(state.seconds);
            }
        }, 1000);
    }
    function stopTimer() {
        if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    }

    // ---------- Category picker ----------
    function buildCategoryGrid() {
        const grid = document.getElementById('categoryGrid');
        grid.innerHTML = '';
        const cats = availableCategories();
        if (cats.indexOf(state.category) === -1 && cats.length) state.category = cats[0];
        cats.forEach(function (key) {
            const cat = WORDS[key];
            const btn = document.createElement('button');
            btn.className = 'cat-btn';
            btn.innerHTML = '<span>' + cat.icon + '</span><span>' + catLabel(cat) + '</span>';
            btn.addEventListener('click', function () {
                closeCategoryPicker();
                const apply = function () { state.category = key; startGame(); };
                if (inProgress()) askNewGame(apply);
                else apply();
            });
            grid.appendChild(btn);
        });
        const randBtn = document.createElement('button');
        randBtn.className = 'cat-btn random-btn';
        randBtn.innerHTML = '<span>🎲</span><span data-i18n="random-cat">' + T('random-cat') + '</span>';
        randBtn.addEventListener('click', function () {
            const apply = function () {
                state.category = cats[Math.floor(Math.random() * cats.length)];
                startGame();
            };
            closeCategoryPicker();
            if (inProgress()) askNewGame(apply);
            else apply();
        });
        grid.appendChild(randBtn);
    }

    function openCategoryPicker() { document.getElementById('categoryOverlay').classList.remove('hidden'); }
    function closeCategoryPicker() { document.getElementById('categoryOverlay').classList.add('hidden'); }

    // ---------- Settings ----------
    const TRANSLATE_LANGS = [
        { code: 'en', name: 'English' },
        { code: 'nl', name: 'Nederlands' },
        { code: 'uk', name: 'Українська' }
    ];

    // The game's own language is never offered as a translation, so the list
    // is rebuilt whenever it could have changed.
    function buildTranslateSelect() {
        const sel = document.getElementById('settingTranslateTo');
        if (!sel) return;
        sel.innerHTML = '';
        const off = document.createElement('option');
        off.value = '';
        off.textContent = T('translate-off');
        sel.appendChild(off);
        for (let i = 0; i < TRANSLATE_LANGS.length; i++) {
            const l = TRANSLATE_LANGS[i];
            if (l.code === wordsLang()) continue;
            const o = document.createElement('option');
            o.value = l.code;
            o.textContent = l.name;
            o.setAttribute('lang', l.code);
            sel.appendChild(o);
        }
        sel.value = translateTo;
    }

    // Translation mode only picks words that have a translation, so turning
    // it on changes the pool and the current word cannot be kept. Turning it
    // off does not: translated words are a subset of all words, so just hide
    // the hint and carry on.
    function setTranslateTo(value) {
        if (value === translateTo) return;
        const prev = translateTo;
        translateTo = value;
        settings.translateTo = value;
        saveSettings();
        if (!value) {
            buildCategoryGrid();
            renderWordTiles();
            return;
        }
        if (inProgress()) {
            askNewGame(function () {
                buildCategoryGrid();
                startGame();
            }, function () {
                translateTo = prev;
                settings.translateTo = prev;
                saveSettings();
                buildTranslateSelect();
            });
        } else {
            buildCategoryGrid();
            startGame();
        }
    }

    function openSettings() {
        document.getElementById('settingSoundEffects').checked = settings.soundEffects;
        buildTranslateSelect();
        document.getElementById('settingsOverlay').classList.remove('hidden');
    }
    function closeSettings() { document.getElementById('settingsOverlay').classList.add('hidden'); }
    function updateSetting(key, value) {
        settings[key] = value;
        saveSettings();
    }
    function saveSettings() {
        try { localStorage.setItem('oefenpad-galgje-settings', JSON.stringify(settings)); } catch (e) {}
    }
    function loadSettings() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-galgje-settings') || 'null');
            if (saved) settings = Object.assign(settings, saved);
        } catch (e) {}
        // A saved language may no longer be valid (the site language changed,
        // or the setting predates this feature). Off is always safe.
        const valid = TRANSLATE_LANGS.some(function (l) { return l.code === settings.translateTo; });
        translateTo = (valid && settings.translateTo !== wordsLang()) ? settings.translateTo : '';
        settings.translateTo = translateTo;
    }

    // ---------- Stats ----------
    function saveStats() {
        try { localStorage.setItem('oefenpad-galgje-stats', JSON.stringify(stats)); } catch (e) {}
    }
    function loadStats() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-galgje-stats') || 'null');
            if (saved) stats = Object.assign(stats, saved);
        } catch (e) {}
    }

    // ---------- Save / restore ----------
    function saveGame() {
        try {
            localStorage.setItem('oefenpad-galgje-save', JSON.stringify(state));
        } catch (e) {}
    }
    function loadGame() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-galgje-save') || 'null');
            if (saved && saved.word && saved.wordLang === wordsLang()) {
                state = Object.assign(state, saved);
                lastWord = saved.word;
                return true;
            }
        } catch (e) {}
        return false;
    }

    // ---------- Audio ----------
    // Tones and the shared AudioContext live in common.js.
    function playCorrectSound() { OEFENPAD.sfx.correct(settings.soundEffects); }
    function playWrongSound() { OEFENPAD.sfx.wrong(settings.soundEffects); }
    function playFanfare() { OEFENPAD.sfx.fanfare(settings.soundEffects); }

    // ---------- Confetti ----------
    function spawnConfetti() {
        OEFENPAD.spawnConfetti({
            container: 'confettiContainer',
            colors: ['#FFB300', '#009688', '#E57373', '#64B5F6', '#81C784', '#BA68C8'],
            count: 80,
            duration: [2, 4],
            delay: [0, 0.6],
            clear: false,
            removeAfter: 4600
        });
    }

    // ---------- Splash ----------
    function hideSplash() { OEFENPAD.hideSplash('splashScreen', 600); }

    // ---------- Language change ----------
    let lastLang = I18N.lang;
    document.addEventListener('i18nchange', function () {
        if (translateTo === wordsLang()) {
            translateTo = '';
            settings.translateTo = '';
            saveSettings();
        }
        buildTranslateSelect();
        buildCategoryGrid();
        renderStatus();
        if (I18N.lang === lastLang) {
            renderTranslation();
            return;
        }
        lastLang = I18N.lang;
        if (inProgress()) askNewGame(startGame);
        else startGame();
    });

    // ---------- Physical keyboard ----------
    document.addEventListener('keydown', function (e) {
        if (e.key && e.key.length === 1) {
            const letter = e.key.toUpperCase();
            const alphabet = ALPHABETS[wordsLang()] || ALPHABETS.en;
            if (alphabet.indexOf(letter) !== -1) guess(letter);
        }
    });

    // ---------- Init ----------
    function init() {
        loadSettings();
        loadStats();
        buildCategoryGrid();
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const key = btn.dataset.diff;
                if (key === state.difficulty) return;
                const apply = function () { state.difficulty = key; renderStatus(); startGame(); };
                if (inProgress()) askNewGame(apply);
                else apply();
            });
        });
        if (!loadGame()) {
            startGame();
        } else {
            renderWordTiles();
            renderKeyboard();
            renderStatus();
            updateHintButton();
            draw();
            if (state.status === 'playing') startTimer();
        }
        const wordTilesEl = document.getElementById('wordTiles');
        wordTilesEl.addEventListener('click', toggleTranslation);
        wordTilesEl.addEventListener('keydown', function (e) {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            if (!translationFor(state.word)) return;
            e.preventDefault();
            toggleTranslation();
        });
        const splash = document.getElementById('splashScreen');
        splash.addEventListener('click', hideSplash);
        setTimeout(hideSplash, 2500);
        document.addEventListener('themechange', draw);
        window.addEventListener('beforeunload', function (e) {
            if (inProgress()) { e.preventDefault(); e.returnValue = ''; }
        });
    }
    init();

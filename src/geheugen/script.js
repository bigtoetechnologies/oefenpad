    /* =================================================================
       Geheugen — Oefenpad
       Each pair is a Dutch word and the picture it names. Find both.
       ================================================================= */

    const I18N = window.I18N || { lang: 'en', t: function () { return null; }, register: function () {} };

    const TEXTS = {
        'page-title':    { en: 'Geheugen — Oefenpad', nl: 'Geheugen — Oefenpad', uk: 'Меморі — Oefenpad' },
        'splash-title':  { en: 'Geheugen', nl: 'Geheugen', uk: 'Меморі' },
        'app-title':     { en: 'Geheugen', nl: 'Geheugen', uk: 'Меморі' },
        'settings-title':{ en: '⚙️ Settings', nl: '⚙️ Instellingen', uk: '⚙️ Налаштування' },
        'sound-effects': { en: '🔊 Sound Effects', nl: '🔊 Geluidseffecten', uk: '🔊 Звукові ефекти' },
        'show-labels':   { en: '🏷️ Show word labels on pictures', nl: '🏷️ Toon woorden bij plaatjes', uk: '🏷️ Показувати слова на малюнках' },
        'close':         { en: 'Close', nl: 'Sluiten', uk: 'Закрити' },
        'diff-4x4':      { en: '4×4', nl: '4×4', uk: '4×4' },
        'diff-6x6':      { en: '6×6', nl: '6×6', uk: '6×6' },
        'diff-8x8':      { en: '8×8', nl: '8×8', uk: '8×8' },
        'diff-10x10':    { en: '10×10', nl: '10×10', uk: '10×10' },
        'moves-label':   { en: '🎯 Moves:', nl: '🎯 Zetten:', uk: '🎯 Ходи:' },
        'pairs-label':   { en: '🃏 Pairs:', nl: '🃏 Paren:', uk: '🃏 Пари:' },
        'time-label':    { en: '⏱ Time:', nl: '⏱ Tijd:', uk: '⏱ Час:' },
        'best-label':    { en: '🏆 Best:', nl: '🏆 Beste:', uk: '🏆 Рекорд:' },
        'btn-new':       { en: '🎲 New Game', nl: '🎲 Nieuw spel', uk: '🎲 Нова гра' },
        'cele-title':    { en: 'All Pairs Found!', nl: 'Alle paren gevonden!', uk: 'Усі пари знайдено!' },
        'cele-msg':      { en: 'Great job! You found every pair.', nl: 'Goed gedaan! Je hebt alle paren gevonden.', uk: 'Чудова робота! Ти знайшов усі пари.' },
        'btn-close':     { en: '✕ Close', nl: '✕ Sluiten', uk: '✕ Закрити' },
        'cat-title':     { en: 'Choose a Category', nl: 'Kies een categorie', uk: 'Оберіть категорію' },
        'cat-subtitle':  { en: 'Select a theme for your memory game:', nl: 'Kies een thema voor je memoryspel:', uk: 'Виберіть тему для гри:' },
        'cat-all':       { en: 'All', nl: 'Alles', uk: 'Усі' },
        'cancel':        { en: 'Cancel', nl: 'Annuleren', uk: 'Скасувати' },
        'confirm-new-title': { en: 'Start a New Game?', nl: 'Nieuw spel starten?', uk: 'Почати нову гру?' },
        'confirm-new-msg':   { en: 'This will start a new game. Your current progress will be lost.', nl: 'Dit start een nieuw spel. Je huidige voortgang gaat verloren.', uk: 'Це почне нову гру. Поточний прогрес буде втрачено.' },
        'confirm-ok':        { en: 'Start New Game', nl: 'Nieuw spel starten', uk: 'Почати нову гру' },
        'version':       { en: 'Version 0.1.0', nl: 'Versie 0.1.0', uk: 'Версія 0.1.0' }
    };
    I18N.register('geheugen', TEXTS);

    function T(key, vars) { return I18N.t(key, vars) || (TEXTS[key] ? TEXTS[key].en : key); }
    function catLabel(cat) { return cat.label[I18N.lang] || cat.label.en; }

    // ---- Levels ----
    const LEVELS = {
        4:  { size: 4,  pairs: 8 },
        6:  { size: 6,  pairs: 18 },
        8:  { size: 8,  pairs: 32 },
        10: { size: 10, pairs: 50 }
    };

    // ---- Symbols (fallback when no word images exist — real art takes priority) ----
    const SYMBOLS = [
        '🐶','🐱','🦊','🐼','🐸','🦁','🐮','🐷','🐵','🐔',
        '🐧','🦆','🦅','🦉','🦇','🐺','🐗','🐴','🦄','🐝',
        '🐛','🦋','🐌','🐞','🐢','🐙','🦀','🐠','🐬','🐳',
        '🦈','🐊','🦕','🦖','🍎','🍌','🍓','🍕','🍩','🎈',
        '⚽','🚀','🌈','⭐','🌙','☀️','🌸','🍀','🔥','🎵'
    ];

    // ---- Word images (../wordimages.js) — the primary card faces -------
    //      Values are '<category>/<slug>.jpg' (e.g. 'food/apple.jpg').
    const IMAGES = window.OEFENPAD_WORD_IMAGES || {};
    const WORDS = window.OEFENPAD_WORDS || {};   // category labels/icons only

    // ---- State ----
    let levelKey = 6;
    let categoryKey = 'all';   // 'all' or an image-category key (animals, food, ...)
    let cards = [];
    let firstCard = null;
    let lock = false;
    let moves = 0;
    let matchedCount = 0;
    let seconds = 0;
    let timerInterval = null;
    let timerStarted = false;
    let settings = { soundEffects: true, showLabels: true };
    let best = {};

    // ---------- Utilities ----------
    // Shared helpers live in src/shared/common.js
    function shuffle(arr) { return OEFENPAD.shuffle(arr); }

    function fmtTime(seconds) { return OEFENPAD.fmtTime(seconds); }

    // ---------- Game flow ----------
    function imagePool(catKey) {
        const values = Object.values(IMAGES);
        const seen = {};
        const unique = [];
        values.forEach(function (v) {
            const cat = v.indexOf('/') !== -1 ? v.split('/')[0] : '';
            if (catKey && catKey !== 'all' && cat !== catKey) return;
            if (!seen[v]) { seen[v] = true; unique.push(v); }
        });
        return unique;
    }

    function imageCategories() {
        const cats = {};
        Object.values(IMAGES).forEach(function (v) {
            if (v.indexOf('/') !== -1) cats[v.split('/')[0]] = true;
        });
        return Object.keys(cats).sort();
    }

    function categoryName(key) {
        if (key === 'all') return T('cat-all');
        const cat = WORDS[key];
        return cat ? catLabel(cat) : key;
    }

    function renderCategoryChip() {
        const cat = WORDS[categoryKey];
        document.getElementById('categoryEmoji').textContent = cat ? cat.icon : '🖼️';
        document.getElementById('categoryName').textContent = categoryName(categoryKey);
    }

    function syncLevelButtons() {
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.classList.toggle('active', Number(btn.dataset.level) === levelKey);
        });
    }

    function updateLevelButtons() {
        const unique = imagePool(categoryKey);
        if (!unique.length) return; // emoji fallback mode: all levels playable
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            const lvl = LEVELS[Number(btn.dataset.level)];
            btn.disabled = unique.length < lvl.pairs;
        });
    }

    function ensurePlayableLevel() {
        const unique = imagePool(categoryKey);
        if (!unique.length) return; // emoji fallback mode
        if (LEVELS[levelKey].pairs <= unique.length) return;
        for (const k of [10, 8, 6, 4]) {
            if (LEVELS[k].pairs <= unique.length) { levelKey = k; break; }
        }
    }

    // ---------- Category picker ----------
    function buildCategoryGrid() {
        const grid = document.getElementById('categoryGrid');
        if (!grid) return;
        grid.innerHTML = '';
        const need = LEVELS[levelKey].pairs;
        ['all'].concat(imageCategories()).forEach(function (key) {
            const btn = document.createElement('button');
            btn.className = 'cat-btn';
            const pool = imagePool(key).length;
            const enabled = pool >= need;
            btn.disabled = !enabled;
            const cat = WORDS[key];
            btn.innerHTML = '<span>' + (cat ? cat.icon : '🖼️') + '</span>' +
                '<span>' + categoryName(key) + (enabled ? '' : ' (' + pool + ')') + '</span>';
            btn.addEventListener('click', function () {
                closeCategoryPicker();
                const apply = function () {
                    categoryKey = key;
                    ensurePlayableLevel();
                    syncLevelButtons();
                    deal();
                    renderCategoryChip();
                };
                if (inProgress()) askNewGame(apply);
                else apply();
            });
            grid.appendChild(btn);
        });
    }

    function openCategoryPicker() { document.getElementById('categoryOverlay').classList.remove('hidden'); }
    function closeCategoryPicker() { document.getElementById('categoryOverlay').classList.add('hidden'); }

    function deal() {
        const level = LEVELS[levelKey];
        const unique = imagePool(categoryKey);
        const items = unique.length
            ? shuffle(unique).slice(0, level.pairs)
            : shuffle(SYMBOLS).slice(0, level.pairs);
        // One picture card and one Dutch-word card per item.
        const deck = shuffle(
            items.map(function (item) { return { item: item, kind: 'image' }; })
                .concat(items.map(function (item) { return { item: item, kind: 'word' }; }))
        );
        cards = deck.map(function (card) {
            return { item: card.item, kind: card.kind, matched: false };
        });
        firstCard = null;
        lock = false;
        moves = 0;
        matchedCount = 0;
        seconds = 0;
        timerStarted = false;
        stopTimer();
        resetPop();
        renderGrid();
        renderStatus();
        updateLevelButtons();
    }

    function newGame() {
        closeCelebration();
        deal();
    }

    function setLevel(key) {
        if (key === levelKey) return;
        const apply = function () {
            levelKey = key;
            syncLevelButtons();
            buildCategoryGrid(); // re-enable categories now possible at this size
            deal();
        };
        if (inProgress()) askNewGame(apply);
        else apply();
    }

    // ---------- New-game confirmation ----------
    let pendingNewGame = null;
    function inProgress() {
        return moves > 0 || matchedCount > 0 || firstCard !== null;
    }
    function askNewGame(cb) {
        pendingNewGame = cb;
        document.getElementById('confirmOverlay').classList.remove('hidden');
    }
    function confirmNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        const cb = pendingNewGame;
        pendingNewGame = null;
        if (cb) cb();
    }
    function cancelNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        pendingNewGame = null;
    }

    // ---------- Rendering ----------
    function renderGrid() {
        const grid = document.getElementById('memoryGrid');
        const level = LEVELS[levelKey];
        grid.style.gridTemplateColumns = 'repeat(' + level.size + ', 1fr)';
        grid.innerHTML = '';
        cards.forEach(function (card, i) {
            const btn = document.createElement('button');
            btn.className = 'card';
            btn.dataset.index = i;
            const isImg = card.kind !== 'word' && /\.(jpg|jpeg|png|webp)$/i.test(card.item);
            const face = card.kind === 'word'
                ? '<span class="card-word">' + wordForItem(card.item) + '</span>'
                : (isImg
                    ? '<img src="../../assets/wordimages/' + card.item + '" alt="">'
                    : card.item);
            btn.innerHTML =
                '<div class="card-inner">' +
                    '<div class="card-back"></div>' +
                    '<div class="card-face" aria-hidden="true">' + face + '</div>' +
                '</div>';
            // The face is in the DOM from the start, only rotated out of view,
            // so it stays aria-hidden until the card is actually flipped —
            // otherwise a screen reader simply reads out the whole board.
            labelCard(btn, i);
            btn.addEventListener('click', function () { flipCard(i, btn); });
            grid.appendChild(btn);
        });
        updateSymbolSize();
    }

    function A11Y(key, vars, fallback) {
        const s = I18N.t(key, vars);
        return s === null ? fallback : s;
    }

    // Keeps a card's accessible name in step with its face-up/face-down state.
    function labelCard(btn, i) {
        const card = cards[i];
        if (!card) return;
        const faceUp = btn.classList.contains('flipped');
        const faceEl = btn.querySelector('.card-face');
        if (faceEl) faceEl.setAttribute('aria-hidden', faceUp ? 'false' : 'true');

        if (!faceUp) {
            btn.setAttribute('aria-label',
                A11Y('a11y-card-down', { i: i + 1 }, 'Card ' + (i + 1) + ', face down'));
            return;
        }
        const what = card.kind === 'word'
            ? wordForItem(card.item)
            : (/\.(jpg|jpeg|png|webp)$/i.test(card.item)
                ? (wordForItem(card.item) || '')
                : card.item);
        const key = card.matched ? 'a11y-card-matched' : 'a11y-card-up';
        btn.setAttribute('aria-label',
            A11Y(key, { i: i + 1, what: what },
                 'Card ' + (i + 1) + ', ' + what + (card.matched ? ', matched' : '')));
    }

    function relabelCards() {
        const grid = document.getElementById('memoryGrid');
        if (!grid) return;
        grid.querySelectorAll('.card').forEach(function (btn) {
            labelCard(btn, Number(btn.dataset.index));
        });
    }

    function updateSymbolSize() {
        // Emoji faces scale by cell size; images fill the face via CSS.
        const grid = document.getElementById('memoryGrid');
        if (!imagePool().length) {
            const level = LEVELS[levelKey];
            const cellW = Math.floor(grid.clientWidth / level.size);
            const px = Math.max(16, Math.floor(cellW * 0.5));
            grid.style.fontSize = px + 'px';
        } else {
            grid.style.fontSize = '';
        }
    }

    function renderStatus() {
        document.getElementById('movesCount').textContent = moves;
        document.getElementById('pairsCount').textContent =
            (matchedCount / 2) + '/' + LEVELS[levelKey].pairs;
        document.getElementById('timerDisplay').textContent = fmtTime(seconds);
        const key = levelKey + 'x' + levelKey;
        const b = best[key];
        document.getElementById('bestDisplay').textContent = b ? (b.moves + ' 🎯') : '—';
    }

    // ---------- Card zoom ----------
    let popActive = false;
    let popOnDone = null;
    let popHoldTimer = null;
    let popOutTimer = null;

    // Image path -> first English word that uses it (aliases share one image)
    const IMG_TO_WORD = (function () {
        const map = {};
        Object.keys(IMAGES).forEach(function (w) {
            if (!map[IMAGES[w]]) map[IMAGES[w]] = w;
        });
        return map;
    })();

    function localizedWord(enWord) {
        const lang = (I18N.lang === 'en' || I18N.lang === 'en-us') ? 'en' : I18N.lang;
        const cats = Object.keys(WORDS);
        for (let i = 0; i < cats.length; i++) {
            const list = WORDS[cats[i]].words || [];
            for (let j = 0; j < list.length; j++) {
                if (list[j].en === enWord) return list[j][lang] || enWord;
            }
        }
        return enWord;
    }

    function wordForItem(item) {
        if (!/\.(jpg|jpeg|png|webp)$/i.test(item)) return '';
        return localizedWord(IMG_TO_WORD[item] || '');
    }

    function fillZoomCard(card, content, isImg, word) {
        if (isImg) {
            card.className = 'zoom-card';
            card.innerHTML = '<img src="' + content + '" alt="">';
            if (word) {
                const w = document.createElement('div');
                w.className = 'zoom-word';
                w.textContent = word;
                card.appendChild(w);
            }
        } else {
            card.className = 'zoom-card zoom-text';
            card.textContent = content;
        }
    }

    function openZoom(content, isImg, word) {
        if (popActive) return;
        const card = document.getElementById('zoomCard');
        fillZoomCard(card, content, isImg, word);
        document.getElementById('zoomOverlay').classList.remove('hidden');
    }
    function closeZoom() {
        if (popActive) return;
        document.getElementById('zoomOverlay').classList.add('hidden');
    }

    function beginPopOut() {
        if (!popActive) return;
        clearTimeout(popHoldTimer);
        clearTimeout(popOutTimer);
        const card = document.getElementById('zoomCard');
        card.classList.remove('zoom-pop');
        card.classList.add('zoom-pop-out');
        popOutTimer = setTimeout(function () {
            document.getElementById('zoomOverlay').classList.add('hidden');
            card.classList.remove('zoom-pop-out');
            popActive = false;
            const cb = popOnDone;
            popOnDone = null;
            if (cb) cb();
        }, 500);
    }

    // Tear the popup down immediately, dropping any pending callback. Called
    // when a new game is dealt (the board the callback closed over is gone)
    // and at the top of autoPop, so a second pop can never leave the first
    // one's hold timer running — that timer would fire early and resolve the
    // *new* pop ahead of time.
    function resetPop() {
        clearTimeout(popHoldTimer);
        clearTimeout(popOutTimer);
        popHoldTimer = null;
        popOutTimer = null;
        popActive = false;
        popOnDone = null;
        const card = document.getElementById('zoomCard');
        if (card) card.classList.remove('zoom-pop', 'zoom-pop-out');
        const overlay = document.getElementById('zoomOverlay');
        if (overlay) overlay.classList.add('hidden');
    }

    // Esc or a click sends the popup back to normal size early.
    function dismissPop() { if (popActive) beginPopOut(); }

    // Auto pop: the just-flipped card spins up to full size, holds ~1s,
    // then spins back down to its proper size on the board.
    function autoPop(btn, onDone) {
        resetPop();
        popActive = true;
        popOnDone = onDone;
        const face = btn.querySelector('.card-face');
        const img = face ? face.querySelector('img') : null;
        const flipped = cards[Number(btn.dataset.index)];
        const item = flipped.item;
        const card = document.getElementById('zoomCard');
        card.className = '';
        if (flipped.kind === 'word') {
            fillZoomCard(card, wordForItem(item), false);
        } else {
            fillZoomCard(card, img ? img.getAttribute('src') : '', !!img,
                settings.showLabels ? wordForItem(item) : '');
        }
        card.classList.add('zoom-pop');
        document.getElementById('zoomOverlay').classList.remove('hidden');
        popHoldTimer = setTimeout(beginPopOut, 1400);
    }

    // ---------- Flip logic ----------
    function flipCard(index, btn) {
        // Face-up cards zoom their content instead of flipping.
        if (btn.classList.contains('flipped')) {
            const card = cards[index];
            const item = card.item;
            if (card.kind === 'word') {
                openZoom(wordForItem(item), false);
            } else if (/\.(jpg|jpeg|png|webp)$/i.test(item)) {
                openZoom('../../assets/wordimages/' + item, true, settings.showLabels ? wordForItem(item) : '');
            } else {
                openZoom(item, false);
            }
            return;
        }
        if (lock) return;

        if (!timerStarted) {
            timerStarted = true;
            startTimer();
        }

        btn.classList.add('flipped');
        labelCard(btn, index);
        playFlipSound();

        if (!firstCard) {
            firstCard = btn;
            autoPop(btn);
            return;
        }

        // second card flipped
        const firstIndex = Number(firstCard.dataset.index);
        const secondIndex = index;
        moves++;
        renderStatus();

        // A match is the word card and the picture card for the same item.
        if (cards[firstIndex].item === cards[secondIndex].item &&
                cards[firstIndex].kind !== cards[secondIndex].kind) {
            cards[firstIndex].matched = true;
            cards[secondIndex].matched = true;
            firstCard.classList.add('matched');
            btn.classList.add('matched');
            relabelCards();
            matchedCount += 2;
            firstCard = null;
            renderStatus();
            playCorrectSound();
            const isWin = matchedCount === cards.length;
            lock = true;
            autoPop(btn, function () {
                lock = false;
                if (isWin) winGame();
            });
        } else {
            lock = true;
            const prev = firstCard;
            firstCard = null;
            autoPop(btn, function () {
                prev.classList.add('wrong');
                btn.classList.add('wrong');
                playWrongSound();
                setTimeout(function () {
                    prev.classList.remove('flipped', 'wrong');
                    btn.classList.remove('flipped', 'wrong');
                    relabelCards();
                    lock = false;
                }, 350);
            });
        }
    }

    // ---------- Win ----------
    function winGame() {
        stopTimer();
        const key = levelKey + 'x' + levelKey;
        const prev = best[key];
        if (!prev || moves < prev.moves || (moves === prev.moves && seconds < prev.seconds)) {
            best[key] = { moves: moves, seconds: seconds };
            saveBest();
        }
        document.getElementById('celeMoves').textContent = moves;
        document.getElementById('celeTime').textContent = fmtTime(seconds);
        document.getElementById('celebrationOverlay').classList.remove('hidden');
        spawnConfetti();
        playFanfare();
        renderStatus();
    }

    function closeCelebration() {
        document.getElementById('celebrationOverlay').classList.add('hidden');
    }

    // ---------- Timer ----------
    function startTimer() {
        stopTimer();
        timerInterval = setInterval(function () {
            seconds++;
            document.getElementById('timerDisplay').textContent = fmtTime(seconds);
        }, 1000);
    }
    function stopTimer() {
        if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    }

    // ---------- Settings ----------
    function openSettings() {
        document.getElementById('settingSoundEffects').checked = settings.soundEffects;
        document.getElementById('settingShowLabels').checked = settings.showLabels;
        document.getElementById('settingsOverlay').classList.remove('hidden');
    }
    function closeSettings() { document.getElementById('settingsOverlay').classList.add('hidden'); }
    function updateSetting(key, value) {
        settings[key] = value;
        saveSettings();
    }
    function saveSettings() {
        try { localStorage.setItem('oefenpad-geheugen-settings', JSON.stringify(settings)); } catch (e) {}
    }
    function loadSettings() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-geheugen-settings') || 'null');
            if (saved) settings = Object.assign(settings, saved);
        } catch (e) {}
    }
    function saveBest() {
        try { localStorage.setItem('oefenpad-geheugen-best', JSON.stringify(best)); } catch (e) {}
    }
    function loadBest() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-geheugen-best') || 'null');
            if (saved) best = saved;
        } catch (e) {}
    }

    // ---------- Audio ----------
    // Tones and the shared AudioContext live in common.js.
    function playFlipSound() { OEFENPAD.sfx.flip(settings.soundEffects); }
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

    // ---------- Init ----------
    function init() {
        loadSettings();
        loadBest();
        ensurePlayableLevel();
        syncLevelButtons();
        buildCategoryGrid();
        renderCategoryChip();
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.addEventListener('click', function () { setLevel(Number(btn.dataset.level)); });
        });
        document.addEventListener('i18nchange', function () {
            buildCategoryGrid();
            renderCategoryChip();
            renderStatus();
        });
        deal();
        document.getElementById('zoomOverlay').addEventListener('click', function () {
            if (popActive) dismissPop(); else closeZoom();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { if (popActive) dismissPop(); else closeZoom(); }
        });
        const splash = document.getElementById('splashScreen');
        splash.addEventListener('click', hideSplash);
        setTimeout(hideSplash, 2500);
        window.addEventListener('resize', updateSymbolSize);
        window.addEventListener('beforeunload', function (e) {
            if (inProgress()) { e.preventDefault(); e.returnValue = ''; }
        });
    }
    init();

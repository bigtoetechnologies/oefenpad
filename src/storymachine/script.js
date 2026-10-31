/* =================================================================
   script.js — the story machine.

   Reels are positional: reel 0 is always WHO, reel 1 always DOES
   WHAT. That is the whole reason this is a machine and not a bag of
   dice, so the reel order in reels.js is load-bearing for the
   sentence, not decoration.

   A reel spins by building a tall strip that ends on the chosen
   tile, then translating the strip up to it. Held reels keep their
   tile and never rebuild.
   ================================================================= */

(function () {
    'use strict';

    var REELS = window.REELS;
    var SPIN_BASE = 900;        // ms for the first reel to settle
    var SPIN_STAGGER = 260;     // each later reel settles this much after
    var STRIP_LEN = 26;         // tiles in the spinning strip

    var windowEl = document.getElementById('window');
    var lever = document.getElementById('lever');
    var announce = document.getElementById('announce');
    var countInput = document.getElementById('reel-count');
    var countOut = document.getElementById('reel-count-out');
    var cardsEl = document.getElementById('cards');
    var langNl = document.getElementById('lang-nl');

    var reels = [];             // one state object per visible reel
    var spinning = false;

    function reduceMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function pick(list) {
        return list[Math.floor(Math.random() * list.length)];
    }

    /* The sixth reel is a wildcard: usually an ending, sometimes
       anything at all, so the last line can still surprise you.

       Reel pools are disjoint, so only a wildcard draw can repeat a
       tile already on screen — "and in the end, fire" under a reel
       that already says fire. `avoid` rejects those. */
    function drawTile(reelIndex, avoid) {
        var reel = REELS[reelIndex];
        var tile;

        for (var tries = 0; tries < 12; tries++) {
            tile = (reel.wildcard && Math.random() > 0.6)
                ? pick(pick(REELS).tiles)
                : pick(reel.tiles);
            if (!avoid || avoid.indexOf(tile.id) === -1) return tile;
        }
        return tile;
    }

    function shownIds(except) {
        return reels.filter(function (r) { return r !== except; })
                    .map(function (r) { return r.tile && r.tile.id; });
    }

    function lang() {
        return langNl.checked ? 'nl' : 'en';
    }

    function tileHeight() {
        var raw = getComputedStyle(document.documentElement).getPropertyValue('--tile');
        return parseInt(raw, 10) || 104;
    }

    function buildTile(tile) {
        var el = document.createElement('div');
        el.className = 'tile';

        var art = document.createElement('span');
        art.className = 'tile-art';
        art.textContent = tile.art;
        el.appendChild(art);

        return el;
    }

    /* ---- the word cards ------------------------------------------ */

    /* One face-down card per reel. The word is only revealed by the
       player turning it over, never by the machine. */
    function buildCard(state) {
        var card = document.createElement('button');
        card.className = 'card';
        card.type = 'button';
        card.setAttribute('aria-pressed', 'false');

        var inner = document.createElement('span');
        inner.className = 'card-inner';

        var back = document.createElement('span');
        back.className = 'card-face card-back';

        var front = document.createElement('span');
        front.className = 'card-face card-front';

        var word = document.createElement('span');
        word.className = 'card-word';
        front.appendChild(word);

        inner.appendChild(back);
        inner.appendChild(front);
        card.appendChild(inner);

        card.addEventListener('click', function () {
            turn(state, !state.turned);
        });

        state.card = card;
        state.word = word;
        state.turned = false;
        faceDown(state);

        return card;
    }

    function turn(state, open) {
        state.turned = open;
        state.card.classList.toggle('turned', open);
        state.card.setAttribute('aria-pressed', open ? 'true' : 'false');
        if (open) state.word.textContent = state.tile[lang()];
        state.card.setAttribute('aria-label',
            REELS[state.index].label.en + (open ? ': ' + state.tile[lang()] : ': turn for the word'));
    }

    function faceDown(state) {
        turn(state, false);
        state.word.textContent = '';
    }

    /* ---- building the visible reels ------------------------------ */

    function build(count) {
        windowEl.textContent = '';
        cardsEl.textContent = '';
        reels = [];

        for (var i = 0; i < count; i++) {
            var btn = document.createElement('button');
            btn.className = 'reel';
            btn.type = 'button';
            btn.setAttribute('aria-label', REELS[i].label.en + ' — tap to hold');

            var strip = document.createElement('div');
            strip.className = 'strip';
            btn.appendChild(strip);

            var state = { index: i, el: btn, strip: strip, tile: null, held: false };
            state.tile = drawTile(i, shownIds());
            reels.push(state);

            btn.addEventListener('click', toggleHold.bind(null, state));
            windowEl.appendChild(btn);
            cardsEl.appendChild(buildCard(state));

            settle(state);
        }

        tell();
    }

    function settle(state) {
        state.strip.style.transition = 'none';
        state.strip.style.transform = 'translateY(0)';
        state.strip.textContent = '';
        state.strip.appendChild(buildTile(state.tile));
    }

    function toggleHold(state) {
        if (spinning) return;
        state.held = !state.held;
        state.el.classList.toggle('held', state.held);
    }

    /* ---- spinning ------------------------------------------------ */

    function spinReel(state, duration) {
        var h = tileHeight();
        var strip = state.strip;

        strip.textContent = '';
        for (var i = 0; i < STRIP_LEN; i++) {
            strip.appendChild(buildTile(i === STRIP_LEN - 1 ? state.tile : drawTile(state.index)));
        }

        strip.style.transition = 'none';
        strip.style.transform = 'translateY(0)';
        state.el.classList.add('spinning');

        // Force the browser to accept the reset before animating away from it.
        void strip.offsetHeight;

        strip.style.transition = 'transform ' + duration + 'ms cubic-bezier(.17,.67,.21,1)';
        strip.style.transform = 'translateY(' + (-(STRIP_LEN - 1) * h) + 'px)';
    }

    function pull() {
        if (spinning) return;

        var live = reels.filter(function (r) { return !r.held; });
        if (!live.length) return;

        spinning = true;
        lever.disabled = true;
        lever.classList.add('pulled');
        announce.textContent = '';

        live.forEach(function (r) { r.tile = drawTile(r.index, shownIds(r)); });
        reels.forEach(faceDown);

        if (reduceMotion()) {
            live.forEach(settle);
            finish();
            return;
        }

        var last = 0;
        live.forEach(function (r, n) {
            var duration = SPIN_BASE + n * SPIN_STAGGER;
            last = Math.max(last, duration);
            spinReel(r, duration);
        });

        setTimeout(finish, last + 80);
    }

    function finish() {
        spinning = false;
        lever.disabled = false;
        lever.classList.remove('pulled');
        reels.forEach(function (r) { r.el.classList.remove('spinning'); });
        tell();
    }

    /* ---- announcing ---------------------------------------------- */

    /* Nothing on screen spells the story out; the pictures are the
       prompt. This is the screen-reader equivalent of looking at the
       reels — the tiles, listed, not a sentence. */
    function tell() {
        announce.textContent = reels.map(function (r) {
            return r.tile[lang()];
        }).join(', ');
    }

    /* ---- wiring -------------------------------------------------- */

    lever.addEventListener('click', pull);

    countInput.addEventListener('input', function () {
        countOut.textContent = countInput.value;
        build(parseInt(countInput.value, 10));
    });

    langNl.addEventListener('change', function () {
        reels.forEach(settle);
        reels.forEach(function (r) {
            if (r.turned) r.word.textContent = r.tile[lang()];
        });
        tell();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === ' ' || e.key === 'Enter') {
            if (document.activeElement === document.body) {
                e.preventDefault();
                pull();
            }
        }
    });

    build(parseInt(countInput.value, 10));
    countOut.textContent = countInput.value;
}());

/* =================================================================
   common.js — shared Oefenpad game layer
   ---------------------------------------------------------------
   Load on EVERY game page, AFTER i18n.js and BEFORE the page's own
   script. Holds the helpers the four ported games have in common:
   shuffle, timer formatting, confetti, splash fade-out, sound and
   aria-pressed syncing.

   Everything hangs off window.OEFENPAD.
   ================================================================= */
(function () {
    'use strict';

    var OEFENPAD = window.OEFENPAD = window.OEFENPAD || {};

    /* =============================================================
       Word-image safety net
       -------------------------------------------------------------
       wordimages.js is generated from a folder of pictures, so an
       entry can outlive its file. A missing file would otherwise
       leave a broken-image icon in the middle of a game. Catch the
       error (it does not bubble, hence the capture phase), hide the
       picture, and hide its container too when the picture was all
       it held — galgje's clue box, for one. Words keep their text.

       Several games reuse one <img> across rounds, so the matching
       load handler undoes the hiding; without it, one absent file
       would blank that element for the rest of the session.
       ============================================================= */
    function wordImage(ev) {
        var img = ev.target;
        if (!img || img.tagName !== 'IMG') return null;
        if ((img.getAttribute('src') || '').indexOf('assets/wordimages/') === -1) return null;
        return img;
    }

    function soleChild(img) {
        var parent = img.parentNode;
        if (!parent || parent.nodeType !== 1) return null;
        if (parent.children.length !== 1) return null;
        if ((parent.textContent || '').trim()) return null;
        return parent;
    }

    document.addEventListener('error', function (ev) {
        var img = wordImage(ev);
        if (!img) return;
        img.style.display = 'none';
        img.setAttribute('aria-hidden', 'true');
        var parent = soleChild(img);
        if (parent) parent.style.display = 'none';
    }, true);

    document.addEventListener('load', function (ev) {
        var img = wordImage(ev);
        if (!img) return;
        if (img.style.display === 'none') img.style.display = '';
        img.removeAttribute('aria-hidden');
        var parent = soleChild(img);
        if (parent && parent.style.display === 'none') parent.style.display = '';
    }, true);

    function onReady(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    /* =============================================================
       Accessibility strings (no visible counterpart)
       ============================================================= */
    if (window.I18N) {
        I18N.register('a11y', {
            'a11y-difficulty': { en: 'Difficulty', nl: 'Moeilijkheidsgraad' },
            'a11y-language':   { en: 'Change language', nl: 'Taal wijzigen' },
            'a11y-pencil':     { en: 'Pencil marks', nl: 'Pengenotities' },
            'a11y-board':      { en: 'Puzzle board', nl: 'Puzzelbord' },
            'a11y-cell':       { en: 'Row {row}, column {col}, {value}',
                                 nl: 'Rij {row}, kolom {col}, {value}' },
            'a11y-empty':      { en: 'empty', nl: 'leeg' },
            'a11y-given':      { en: 'given {n}', nl: 'gegeven {n}' },
            'a11y-notes':      { en: 'notes {list}', nl: 'notities {list}' },
            'a11y-num-left':   { en: '{n}, {count} left', nl: '{n}, {count} over' },
            'a11y-card-down':  { en: 'Card {i}, face down', nl: 'Kaart {i}, dicht' },
            'a11y-card-up':    { en: 'Card {i}, {what}', nl: 'Kaart {i}, {what}' },
            'a11y-card-matched': { en: 'Card {i}, {what}, matched',
                                   nl: 'Kaart {i}, {what}, gevonden' },
            'a11y-blank':      { en: 'blank', nl: 'leeg' },
            'a11y-space':      { en: 'space', nl: 'spatie' },
            'a11y-keyboard':   { en: 'Letters', nl: 'Letters' },
            'a11y-key-hit':    { en: '{letter}, correct', nl: '{letter}, goed' },
            'a11y-key-miss':   { en: '{letter}, not in the word',
                                 nl: '{letter}, niet in het woord' }
        });
    }

    /* Keep aria-pressed in step with the .active class. */
    OEFENPAD.syncPressedState = function (root) {
        var els = (root || document).querySelectorAll('[aria-pressed]');
        if (!els.length) return;

        function sync(el) {
            el.setAttribute('aria-pressed', el.classList.contains('active') ? 'true' : 'false');
        }
        for (var i = 0; i < els.length; i++) sync(els[i]);

        if (!window.MutationObserver) return;
        var obs = new MutationObserver(function (records) {
            for (var r = 0; r < records.length; r++) sync(records[r].target);
        });
        for (i = 0; i < els.length; i++) {
            obs.observe(els[i], { attributes: true, attributeFilter: ['class'] });
        }
    };
    onReady(function () { OEFENPAD.syncPressedState(document); });

    /* =============================================================
       Game helpers
       ============================================================= */

    // Fisher-Yates on a copy — the caller's array is untouched.
    OEFENPAD.shuffle = function (arr) {
        var a = arr.slice();
        for (var i = a.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
        }
        return a;
    };

    // Fisher-Yates in place, for callers that want the array mutated.
    OEFENPAD.shuffleInPlace = function (arr) {
        for (var i = arr.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
        }
        return arr;
    };

    // Seconds -> "m:ss".
    OEFENPAD.fmtTime = function (seconds) {
        var s = Math.max(0, Math.floor(seconds) || 0);
        return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
    };

    function randIn(range, fallbackMin, fallbackMax) {
        var min = range ? range[0] : fallbackMin;
        var max = range ? range[1] : fallbackMax;
        return min + Math.random() * (max - min);
    }

    /* Confetti burst. Each game keeps its own palette and timing by
       passing options; the DOM churn lives here. */
    OEFENPAD.spawnConfetti = function (opts) {
        opts = opts || {};
        var container = typeof opts.container === 'string'
            ? document.getElementById(opts.container)
            : (opts.container || document.getElementById('confettiContainer'));
        if (!container) return;

        if (opts.clear !== false) container.innerHTML = '';

        var colors = opts.colors || ['#E8601F', '#2B50C8', '#15307F', '#7E9BE0', '#C44A12'];
        var count = opts.count || 80;
        var unit = opts.topUnit || 'px';

        for (var i = 0; i < count; i++) {
            var piece = document.createElement('div');
            piece.className = 'confetti-piece';
            piece.style.left = Math.random() * 100 + '%';
            piece.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            piece.style.animationDuration = randIn(opts.duration, 2, 4).toFixed(2) + 's';
            piece.style.animationDelay = randIn(opts.delay, 0, 0.6).toFixed(2) + 's';
            if (opts.top) piece.style.top = randIn(opts.top).toFixed(1) + unit;
            if (opts.width) piece.style.width = randIn(opts.width).toFixed(1) + 'px';
            if (opts.height) piece.style.height = randIn(opts.height).toFixed(1) + 'px';
            container.appendChild(piece);
            if (opts.removeAfter) {
                (function (p) {
                    setTimeout(function () { p.remove(); }, opts.removeAfter);
                })(piece);
            }
        }
    };

    // Fade the splash screen out, then take it out of the layout.
    OEFENPAD.hideSplash = function (id, delay) {
        var splash = document.getElementById(id || 'splashScreen');
        if (!splash) return;
        splash.classList.add('fade-out');
        setTimeout(function () { splash.classList.add('hidden'); }, delay || 600);
    };

    /* ---------- Audio ----------
       One lazily created AudioContext per page. Browsers start it
       suspended until a user gesture, so resume on every access. */
    var audioCtx = null;

    OEFENPAD.audioContext = function () {
        if (!audioCtx) {
            var AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return null;
            try { audioCtx = new AC(); } catch (e) { return null; }
        }
        if (audioCtx.state === 'suspended') audioCtx.resume();
        return audioCtx;
    };

    // One oscillator with an exponential decay. steps: [[freqHz, offsetS], ...]
    function tone(type, steps, peak, dur, startAt) {
        var ctx = OEFENPAD.audioContext();
        if (!ctx) return;
        var now = (startAt === undefined ? ctx.currentTime : startAt);
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = type;
        for (var i = 0; i < steps.length; i++) {
            osc.frequency.setValueAtTime(steps[i][0], now + steps[i][1]);
        }
        gain.gain.setValueAtTime(peak, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(now); osc.stop(now + dur);
    }
    OEFENPAD.tone = tone;

    /* The card-game sound set. Each call is a no-op when the game's
       sound setting is off, so callers pass their own flag. */
    OEFENPAD.sfx = {
        flip: function (enabled) {
            if (!enabled) return;
            tone('sine', [[420, 0]], 0.08, 0.08);
        },
        correct: function (enabled) {
            if (!enabled) return;
            tone('sine', [[523, 0], [659, 0.08]], 0.18, 0.25);
        },
        wrong: function (enabled) {
            if (!enabled) return;
            tone('sawtooth', [[180, 0], [120, 0.12]], 0.12, 0.22);
        },
        fanfare: function (enabled) {
            if (!enabled) return;
            var ctx = OEFENPAD.audioContext();
            if (!ctx) return;
            var notes = [523, 659, 784, 1047];
            var start = ctx.currentTime;
            for (var i = 0; i < notes.length; i++) {
                tone('sine', [[notes[i], 0]], 0.18, 0.4, start + i * 0.14);
            }
        }
    };
})();

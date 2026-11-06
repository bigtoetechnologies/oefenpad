/* =================================================================
   i18n.js — shared language layer for Oefenpad
   ---------------------------------------------------------------
   The Oefenpad interface is Dutch-only (see Docs/decisions.md), so
   this is a deliberately small version of the BigToe language layer:
   no detection, no switcher, no persistence. `I18N.lang` is always
   'nl'.

   Pages still register their strings with
       I18N.register('page', { key: { en: '...', nl: '...' } })
   and the Dutch string is used. English is kept in the tables as a
   fallback for rare keys that have not been translated yet.

   Static HTML is translated via attributes:
       <button data-i18n="new-game">Nieuw spel</button>
       <input data-i18n-placeholder="search">
       <span data-i18n-title="hint-tip">…</span>
       <img data-i18n-alt="logo-alt">
       <button data-i18n-aria-label="settings-title">⚙️</button>

   Dynamic text uses:  I18N.t('key')  (or I18N.t('key', {name: x}))
   ================================================================= */
(function () {
    'use strict';

    var dicts = {};      // page name -> { key -> { en, nl } }
    var order = [];      // page names, in registration order
    var lang = 'nl';
    var applied = false;
    var reapplyQueued = false;

    function register(page, dict) {
        if (!dicts[page]) order.push(page);
        dicts[page] = dict;

        if (applied && !reapplyQueued) {
            reapplyQueued = true;
            setTimeout(function () { reapplyQueued = false; apply(); }, 0);
        }
    }

    // Reverse registration order: a page's own strings win over the
    // shared 'site' dictionary registered below.
    function findEntry(key) {
        for (var i = order.length - 1; i >= 0; i--) {
            var d = dicts[order[i]];
            if (d && d[key]) return d[key];
        }
        return null;
    }

    // Returns the Dutch string, or null when the key is unknown.
    function t(key, vars) {
        var entry = findEntry(key);
        if (!entry) return null;
        var s = entry.nl || entry.en || key;
        if (vars) {
            for (var k in vars) {
                s = s.split('{' + k + '}').join(String(vars[k]));
            }
        }
        return s;
    }

    function apply(root) {
        root = root || document;

        var els = root.querySelectorAll('[data-i18n]');
        for (var i = 0; i < els.length; i++) {
            var s = t(els[i].getAttribute('data-i18n'));
            if (s !== null) els[i].textContent = s;
        }
        els = root.querySelectorAll('[data-i18n-title]');
        for (i = 0; i < els.length; i++) {
            var st = t(els[i].getAttribute('data-i18n-title'));
            if (st !== null) els[i].setAttribute('title', st);
        }
        els = root.querySelectorAll('[data-i18n-placeholder]');
        for (i = 0; i < els.length; i++) {
            var sp = t(els[i].getAttribute('data-i18n-placeholder'));
            if (sp !== null) els[i].setAttribute('placeholder', sp);
        }
        els = root.querySelectorAll('[data-i18n-alt]');
        for (i = 0; i < els.length; i++) {
            var sa = t(els[i].getAttribute('data-i18n-alt'));
            if (sa !== null) els[i].setAttribute('alt', sa);
        }
        els = root.querySelectorAll('[data-i18n-aria-label]');
        for (i = 0; i < els.length; i++) {
            var sl = t(els[i].getAttribute('data-i18n-aria-label'));
            if (sl !== null) els[i].setAttribute('aria-label', sl);
        }

        if (document.documentElement) document.documentElement.lang = 'nl';
    }

    function init() {
        applied = true;
        apply();
    }

    register('site', {
        'back-to-home': { en: 'Back to Oefenpad', nl: 'Terug naar Oefenpad' },
        'settings-title': { en: 'Settings', nl: 'Instellingen' },
        'close': { en: 'Close', nl: 'Sluiten' },
        'cancel': { en: 'Cancel', nl: 'Annuleren' },
        'btn-new': { en: 'New Game', nl: 'Nieuw spel' },
        'btn-close': { en: 'Close', nl: 'Sluiten' },
        'time-label': { en: 'Time', nl: 'Tijd' },
        'moves-label': { en: 'Moves', nl: 'Zetten' },
        'sound-effects': { en: 'Sound effects', nl: 'Geluidseffecten' }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.I18N = {
        register: register,
        t: t,
        apply: apply,
        get lang() { return lang; }
    };
})();

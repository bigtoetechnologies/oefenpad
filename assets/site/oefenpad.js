/* Oefenpad — geschilderde vlakken.
   Zet achter elk element met data-verf een SVG met een geschilderd vlak in
   de gevraagde kleur. Zonder JS blijft de egale achtergrondkleur staan, dus
   de pagina werkt ook als dit bestand niet laadt. */
(function () {
  'use strict';

  /* De naam van een verf wijst naar een CSS-variabele, zodat de donkere modus
     de kleur meeverandert. De hex is alleen de noodgreep als de variabele
     niet gelezen kan worden. */
  var KLEUR = {
    kobalt: { var: '--kobalt', hex: '#2B50C8' },
    diep:   { var: '--kobalt-diep', hex: '#15307F' },
    oranje: { var: '--oranje', hex: '#E8601F' },
    licht:  { var: '--kobalt-licht', hex: '#7E9BE0' }
  };

  function kleurVan(naam) {
    var k = KLEUR[naam];
    if (!k) return naam;                /* een letterlijke kleur mag ook */
    try {
      var v = getComputedStyle(document.documentElement)
                .getPropertyValue(k.var).trim();
      if (v) return v;
    } catch (e) { /* dan de hex */ }
    return k.hex;
  }

  var DEFS =
    '<svg width="0" height="0" aria-hidden="true" focusable="false"' +
    ' style="position:absolute;left:-9999px"><defs>' +
    '<filter id="op-verf" x="-4%" y="-10%" width="108%" height="120%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.004 0.6" numOctaves="2" seed="5" result="n"/>' +
      '<feColorMatrix in="n" type="luminanceToAlpha" result="a"/>' +
      '<feComponentTransfer in="a" result="a2"><feFuncA type="linear" slope="1.25" intercept="0.3"/></feComponentTransfer>' +
      '<feComposite in="SourceGraphic" in2="a2" operator="in" result="s"/>' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="2" seed="1" result="d"/>' +
      '<feDisplacementMap in="s" in2="d" scale="6" xChannelSelector="R" yChannelSelector="G"/>' +
    '</filter>' +
    '<filter id="op-verf-klein" x="-10%" y="-14%" width="120%" height="128%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.01 0.9" numOctaves="2" seed="7" result="n"/>' +
      '<feColorMatrix in="n" type="luminanceToAlpha" result="a"/>' +
      '<feComponentTransfer in="a" result="a2"><feFuncA type="linear" slope="1.22" intercept="0.32"/></feComponentTransfer>' +
      '<feComposite in="SourceGraphic" in2="a2" operator="in" result="s"/>' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.03 0.08" numOctaves="2" seed="3" result="d"/>' +
      '<feDisplacementMap in="s" in2="d" scale="3" xChannelSelector="R" yChannelSelector="G"/>' +
    '</filter>' +
    '</defs></svg>';

  function ruis(n) { var x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); }

  /* De verf wordt in een vaste, kleine ruimte getekend en daarna uitgerekt
     (preserveAspectRatio="none"). Dat moet zo: het filter is op deze maten
     afgestemd. Tekenen we op ware grootte, dan vallen de borstelsporen onder
     een pixel en wordt het vlak egaal. */
  var RUIT = { groot: [300, 150], klein: [100, 30] };

  /* Een vlak met licht onregelmatige randen: de kwast raakt het papier niet
     overal even strak. w en h zijn de viewBox-maten, niet pixels. */
  function vlak(w, h, zaad) {
    var r = function (k) { return (ruis(zaad + k) - 0.5) * 7; };
    return 'M ' + r(1) + ' ' + (4 + r(2)) +
           ' L ' + (w + r(3)) + ' ' + r(4) +
           ' L ' + (w + r(5)) + ' ' + (h - 3 + r(6)) +
           ' L ' + r(7) + ' ' + (h + r(8)) + ' Z';
  }

  function verf(el) {
    var naam = el.getAttribute('data-verf') || 'kobalt';
    var kleur = kleurVan(naam);
    var klein = el.hasAttribute('data-verf-klein');
    var zaad = +(el.getAttribute('data-zaad') || 0) || (el.textContent.length * 13 + 7);

    var oud = el.querySelector(':scope > svg.verf');
    if (oud) oud.parentNode.removeChild(oud);

    var maat = klein ? RUIT.klein : RUIT.groot;
    var w = maat[0], h = maat[1];

    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'verf');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.innerHTML = '<g filter="url(#op-verf' + (klein ? '-klein' : '') + ')">' +
      '<path d="' + vlak(w, h, zaad) + '" fill="' + kleur + '"/></g>';
    el.insertBefore(svg, el.firstChild);

    /* De egale achtergrond is alleen de terugval voor "geen JS". Hij moet weg
       zodra er geschilderd is, anders vult hij de borstelsporen op en is het
       vlak weer egaal. Pas na het invoegen, zodat een mislukte verf geen
       onzichtbare tegel oplevert. */
    el.style.backgroundColor = 'transparent';
  }


  /* ---------- taalknop ----------
     De detectie zelf staat inline in de <head> van elke pagina, zodat
     er niets in de verkeerde taal flitst. Dit zet alleen de knoppen. */
  function taalNu() {
    return document.documentElement.getAttribute('data-taal') || 'nl';
  }

  function zetTaal(t) {
    var el = document.documentElement;
    el.setAttribute('data-taal', t);
    el.setAttribute('lang', t);
    var titel = el.getAttribute('data-titel-' + t);
    if (titel) document.title = titel;
    try { localStorage.setItem('oefenpad-taal', t); } catch (e) { /* privémodus */ }
    var knoppen = document.querySelectorAll('.taal button[data-taal-knop]');
    for (var i = 0; i < knoppen.length; i++) {
      knoppen[i].setAttribute('aria-pressed',
        String(knoppen[i].getAttribute('data-taal-knop') === t));
    }
    alles();
  }

  function taalKnoppen() {
    var knoppen = document.querySelectorAll('.taal button[data-taal-knop]');
    for (var i = 0; i < knoppen.length; i++) {
      knoppen[i].setAttribute('aria-pressed',
        String(knoppen[i].getAttribute('data-taal-knop') === taalNu()));
      knoppen[i].addEventListener('click', function () {
        zetTaal(this.getAttribute('data-taal-knop'));
      });
    }
  }

  /* ---------- licht/donker-knop ----------
     De schakelaar zelf staat in het inline-blok boven in elke pagina; die
     luistert naar een klik op #theme-toggle. Hier staat alleen de knop, want
     zonder JS is er ook geen donkere modus, dus dan hoeft hij er niet te zijn.
     Het pictogram toont waar je heen gaat: maan in het licht, zon in het donker. */
  var ZON = '<svg class="zon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<circle cx="12" cy="12" r="4.4"/><path d="M12 2.4v2.6M12 19v2.6M2.4 12h2.6M19 12h2.6' +
    'M5.2 5.2l1.9 1.9M16.9 16.9l1.9 1.9M18.8 5.2l-1.9 1.9M7.1 16.9l-1.9 1.9"/></svg>';
  var MAAN = '<svg class="maan" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path d="M20.5 14.8A8.8 8.8 0 0 1 9.2 3.5a7.9 7.9 0 1 0 11.3 11.3Z"/></svg>';

  function themaKnop() {
    if (document.getElementById('theme-toggle')) return;
    /* .balk is de eigen navigatiebalk; .header-right hoort bij de vier spellen
       die nog de oude kop van BigToe hebben. */
    var doel = document.querySelector('.balk .rechts') ||
               document.querySelector('.header-right');
    if (!doel) {
      var balk = document.querySelector('.balk');
      if (!balk) return;
      doel = document.createElement('div');
      doel.className = 'rechts';
      balk.appendChild(doel);
    }
    var knop = document.createElement('button');
    knop.type = 'button';
    knop.id = 'theme-toggle';
    knop.className = 'thema';
    knop.innerHTML = ZON + MAAN +
      '<span class="alleen-lezer" lang="nl">Licht of donker</span>' +
      '<span class="alleen-lezer" lang="en">Light or dark</span>';
    doel.appendChild(knop);
  }

  function alles() {
    var lijst = document.querySelectorAll('[data-verf]');
    for (var i = 0; i < lijst.length; i++) verf(lijst[i]);
  }

  function start() {
    if (!document.getElementById('op-verf')) {
      var houder = document.createElement('div');
      houder.innerHTML = DEFS;
      document.body.insertBefore(houder.firstChild, document.body.firstChild);
    }
    themaKnop();
    taalKnoppen();
    alles();
    /* De donkere modus wisselt de kleurvariabelen; de vlakken moeten opnieuw.
       Herschilderen bij resize of na het laden van het lettertype hoeft niet:
       de viewBox ligt vast, dus de verf rekt gewoon mee. */
    document.addEventListener('themechange', alles);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

  window.Oefenpad = window.Oefenpad || {};
  window.Oefenpad.verf = verf;
  window.Oefenpad.verfAlles = alles;
  window.Oefenpad.zetTaal = zetTaal;
  /* The game app draws its own bar after this script has run, so it asks for
     the button here instead of writing the button itself. */
  window.Oefenpad.ensureThemeToggle = themaKnop;
})();

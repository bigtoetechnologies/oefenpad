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
    taalKnoppen();
    alles();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(alles);
    /* De donkere modus wisselt de kleurvariabelen; de vlakken moeten opnieuw. */
    document.addEventListener('themechange', alles);
  }

  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(alles, 150); });

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

  window.Oefenpad = window.Oefenpad || {};
  window.Oefenpad.verf = verf;
  window.Oefenpad.verfAlles = alles;
  window.Oefenpad.zetTaal = zetTaal;
})();

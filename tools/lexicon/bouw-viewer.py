#!/usr/bin/env python3
"""Build tools/lexicon/index.html: a self-contained viewer for the lexicon TSVs.

Reads the six tab-separated files next to this script and writes one HTML file
with the raw TSV embedded in <script type="text/plain"> blocks. The page needs
no network and opens from file://.

The output is deterministic: no timestamps, no dict-ordering surprises, fixed
line endings. Re-running it over unchanged inputs must produce identical bytes.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "index.html"

# Themes that are not product themes. Everything else counts as "themed".
NON_PRODUCT_THEMES = {"algemeen", "naam", "plaats"}

# The 30 semantic-field labels in woorden-domein.tsv. A value outside this set
# means the file drifted, not that the view should learn a 31st label.
DOMAINS = [
    "People & relations", "Body & health", "Food & drink",
    "Clothing & appearance", "House & home", "Work & jobs", "Money & trade",
    "Transport & travel", "Nature & weather", "Animals", "Plants & farming",
    "Places & geography", "Time", "Quantity & measure", "Movement & position",
    "Thought & knowledge", "Communication & language", "Emotion & feeling",
    "Character & behaviour", "Society & politics", "Law & conflict",
    "War & military", "Education & learning", "Technology & tools",
    "Arts & media", "Sport & games", "Religion & belief",
    "Abstract & general", "Function words", "Names",
]
ABSTRACT_DOMAIN = "Abstract & general"

DATASETS = [
    # id, file, expected rows, expected columns
    ("woorden", "woorden.tsv", 10_000, ["nl", "en", "niveau", "top2000", "herkomst"]),
    ("woordsoort", "woorden-woordsoort.tsv", 10_000, ["nl", "pos", "en"]),
    ("thema", "woorden-thema.tsv", 10_000, ["nl", "thema", "thema_ook", "prioriteit", "en"]),
    ("domein", "woorden-domein.tsv", 10_000, ["nl", "domein", "en"]),
    ("niveau", "woorden-niveau.tsv", 10_000, ["nl", "niveau", "rang", "grondslag"]),
    ("knm-kandidaten", "knm-kandidaten.tsv", 321, ["nl", "en", "knm_thema", "knm_sectie"]),
    ("knm-thema", "knm-thema.tsv", 279, ["nl", "thema", "prioriteit", "waarom"]),
    ("kandidaten", "kandidaten.tsv", 10_442, ["nl", "en", "bron", "licentie"]),
]


def fail(msg: str) -> None:
    print(f"bouw-viewer: error: {msg}", file=sys.stderr)
    sys.exit(1)


def read_tsv(path: Path, columns: list[str], expected_rows: int) -> list[list[str]]:
    raw = path.read_bytes()
    if b"\r" in raw:
        fail(f"{path.name} contains CR; refusing to guess line endings")
    if not raw.endswith(b"\n"):
        fail(f"{path.name} does not end with a newline")
    text = raw.decode("utf-8")
    reader = csv.reader(io.StringIO(text, newline=""), delimiter="\t", quoting=csv.QUOTE_NONE)
    rows = list(reader)
    if not rows:
        fail(f"{path.name} is empty")
    header = rows[0]
    if header != columns:
        fail(f"{path.name} header {header!r} != expected {columns!r}")
    body = rows[1:]
    if len(body) != expected_rows:
        fail(f"{path.name} has {len(body)} data rows, expected {expected_rows}")
    for i, row in enumerate(body, start=2):
        if len(row) != len(columns):
            fail(f"{path.name}:{i} has {len(row)} fields, expected {len(columns)}: {row!r}")
    return body


def check_alignment(a: list[list[str]], b: list[list[str]]) -> None:
    for i, (ra, rb) in enumerate(zip(a, b), start=2):
        if ra[0] != rb[0]:
            fail(f"row-alignment broken at line {i}: nl {ra[0]!r} != {rb[0]!r}")
    if len(a) != len(b):
        fail(f"row counts differ: {len(a)} vs {len(b)}")


def verify(data: dict[str, list[list[str]]]) -> None:
    woorden = data["woorden"]
    woordsoort = data["woordsoort"]
    thema = data["thema"]
    domein = data["domein"]
    niveau = data["niveau"]

    # The five master files are row-aligned on nl, in the same order. That is
    # the join guarantee; the view joins by position, never by word.
    check_alignment(woorden, woordsoort)
    check_alignment(woorden, thema)
    check_alignment(woorden, domein)
    check_alignment(woorden, niveau)

    # domein is a closed set of 30 labels; anything else is a data fault.
    allowed = set(DOMAINS)
    if len(allowed) != 30:
        fail(f"DOMAINS has {len(allowed)} labels, expected 30")
    for i, row in enumerate(domein, start=2):
        if row[1] not in allowed:
            fail(f"woorden-domein.tsv:{i} has unknown domein {row[1]!r} (nl {row[0]!r})")
    seen_domains = {row[1] for row in domein}
    missing = allowed - seen_domains
    if missing:
        fail(f"woorden-domein.tsv never uses {sorted(missing)!r}")

    # Our level axis is a closed 5-band set and every row must carry one, or
    # the filter's counts will not add up. See niveau.py.
    bands = ["Start", "Basis", "Midden", "Gevorderd", "Verdieping"]
    for i, row in enumerate(niveau, start=2):
        if row[1] not in bands:
            fail(f"woorden-niveau.tsv:{i} has unknown niveau {row[1]!r} (nl {row[0]!r})")
        if row[3] not in ("rang", "trede", "knm", "spel"):
            fail(f"woorden-niveau.tsv:{i} has unknown grondslag {row[3]!r} (nl {row[0]!r})")
    used = {row[1] for row in niveau}
    if used != set(bands):
        fail(f"woorden-niveau.tsv uses {sorted(used)!r}, expected all five bands")

    # `niveau` is ours and `niveau` in woorden.tsv is the appendix tier. If they
    # were identical, the new axis would be a rename rather than a level.
    same = sum(1 for n, w in zip(niveau, woorden) if n[1] == w[2])
    if same > len(niveau) // 10:
        fail(f"woorden-niveau.tsv agrees with the appendix tier on {same} rows; "
             "that is too many for a frequency axis")

    # knm-thema is keyed by nl; a duplicate would make the left join ambiguous.
    seen: dict[str, int] = {}
    for i, row in enumerate(data["knm-thema"], start=2):
        key = row[0]
        if key in seen:
            fail(f"knm-thema.tsv has duplicate nl {key!r} at lines {seen[key]} and {i}")
        seen[key] = i

    # Theme accounting must reproduce the counts the brief states, or the
    # definition of a product theme has drifted.
    themed = sum(1 for row in thema if row[1] and row[1] not in NON_PRODUCT_THEMES)
    print(f"bouw-viewer: themed rows (primary thema, product themes only): {themed} of {len(thema)}")
    abstract = sum(1 for row in domein if row[1] == ABSTRACT_DOMAIN)
    print(f"bouw-viewer: domain labels checked against the 30-label set; {ABSTRACT_DOMAIN}: {abstract} of {len(domein)}")
    band_counts = {b: sum(1 for row in niveau if row[1] == b) for b in bands}
    print("bouw-viewer: niveau bands: " + ", ".join(f"{b} {n}" for b, n in band_counts.items()))
    print(f"bouw-viewer: woorden row-alignment check passed ({len(woorden)} rows)")


def embed_tsv(rows: list[list[str]], columns: list[str]) -> str:
    buf = ["\t".join(columns)]
    buf.extend("\t".join(row) for row in rows)
    text = "\n".join(buf) + "\n"
    # Defensive: a field could in principle contain a closing script tag.
    text = text.replace("</script", "<\\/script")
    if "\x00" in text:
        fail("data contains a NUL byte; cannot embed in HTML")
    return text


STYLE = """
:root{
  --bg:#ffffff; --fg:#16181d; --muted:#5b6270; --rule:#e2e5ea; --rule-strong:#c9ced7;
  --zebra:#f7f8fa; --hover:#eef3ff; --accent:#2B50C8; --accent-soft:#e8edfb;
  --dom-bg:#f1f2f4; --dom-fg:#3c424c; --dom-line:#d5d9e0;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#14161a; --fg:#e6e8ec; --muted:#9aa2b1; --rule:#2a2e36; --rule-strong:#3b414c;
    --zebra:#191c21; --hover:#1e2637; --accent:#7f9bff; --accent-soft:#1c2436;
    --dom-bg:#252a32; --dom-fg:#c3c9d4; --dom-line:#3a404b;
  }
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--fg)}
body{font:14px/1.45 var(--sans);padding:0 0 40px}
header.top{border-bottom:1px solid var(--rule-strong);padding:14px 20px 0;position:sticky;top:0;background:var(--bg);z-index:20}
h1{font-size:17px;margin:0 0 2px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:12px;margin-bottom:10px}
.tabs{display:flex;gap:2px;flex-wrap:wrap}
.tabs button{font:inherit;font-size:13px;background:none;border:1px solid transparent;border-bottom:none;
  padding:6px 12px;border-radius:6px 6px 0 0;color:var(--muted);cursor:pointer}
.tabs button[aria-selected="true"]{color:var(--fg);background:var(--accent-soft);border-color:var(--rule-strong);font-weight:600}
.tabs button .n{font-family:var(--mono);font-size:11px;color:var(--muted);margin-left:6px}

.controls{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:flex-end;padding:12px 20px;border-bottom:1px solid var(--rule)}
.field{display:flex;flex-direction:column;gap:3px}
.field label{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.field select,.field input{font:inherit;font-size:13px;padding:4px 6px;border:1px solid var(--rule-strong);
  border-radius:4px;background:var(--bg);color:var(--fg);min-width:110px}
.field.wide input{min-width:260px}
.field select.grp{font-weight:600}
button.reset{font:inherit;font-size:13px;padding:5px 12px;border:1px solid var(--rule-strong);border-radius:4px;
  background:var(--bg);color:var(--fg);cursor:pointer}
button.reset:hover{background:var(--hover)}
.count{margin-left:auto;font-size:13px;color:var(--muted)}
.count b{font-family:var(--mono);color:var(--fg);font-weight:600}

.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:8px 18px;padding:12px 20px;
  border-bottom:1px solid var(--rule);font-size:13px;align-items:start}
.summary section h2{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 6px;font-weight:600}
.summary .kv{display:flex;justify-content:space-between;gap:10px;padding:1px 0}
.summary .kv .num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.summary .kv .lbl{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.summary .themed-note{grid-column:1/-1;padding:8px 10px;border:1px solid var(--rule-strong);border-radius:6px;
  background:var(--accent-soft);font-size:13px}
.summary .themed-note b{font-family:var(--mono)}
.summary details{margin:0}
.summary summary{cursor:pointer;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;list-style:none;margin-bottom:4px;display:flex;gap:6px;align-items:baseline}
.summary summary::-webkit-details-marker{display:none;width:0}
.summary summary::before{content:'▸';font-size:11px;line-height:1;transition:transform .1s}
.summary details[open] summary::before{content:'▾'}
.summary summary .n{font-family:var(--mono);text-transform:none;letter-spacing:0;color:var(--fg);font-weight:500}
.summary section{min-width:0}
.summary summary{display:block}
.summary summary .n{display:inline}
.summary .theme-grid{margin-top:2px;max-height:340px;overflow:auto}
.summary .theme-grid .kv{font-size:12.5px}

.tablewrap{padding:0;overflow-x:auto}
table{width:100%;border-collapse:separate;border-spacing:0;min-width:0}
thead th{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--rule-strong);
  font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);text-align:left;
  padding:7px 8px;cursor:pointer;user-select:none;white-space:nowrap;z-index:2;vertical-align:bottom}
/* header labels may wrap at a narrow width instead of forcing the table wide */
thead th .lbl{display:inline-block;max-width:100%;white-space:normal;vertical-align:bottom}
thead th:hover{color:var(--fg)}
thead th .arrow{font-size:10px;margin-left:4px;color:var(--accent)}
tbody td{padding:4px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
tbody tr:nth-child(even){background:var(--zebra)}
tbody tr:hover{background:var(--hover)}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right;color:var(--muted);white-space:nowrap;width:1%}
td.mono{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
td.nl{font-weight:600}
td.en{max-width:520px;overflow-wrap:anywhere}
td.nowrap{white-space:nowrap}
td.herk{overflow-wrap:anywhere}
@media (max-width:1000px){
  td.en{max-width:none;min-width:170px;overflow-wrap:normal}
  td.herk{max-width:none;min-width:96px}
  table{min-width:820px}
  tbody td{padding:4px 6px}
  thead th{padding:6px 6px;font-size:10px}
}
.chip{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11.5px;line-height:1.5;
  background:var(--c,var(--accent-soft));color:var(--ct,var(--fg));border:1px solid transparent;white-space:nowrap}
/* Domain chips: square, grey, sans-serif, uppercase-leaning — deliberately not a
   theme pill, so the two axes cannot be confused at a glance. */
.chip.domein{border-radius:2px;padding:0 5px;font-family:var(--sans);font-size:11px;font-weight:500;
  letter-spacing:.01em;background:var(--dom-bg);color:var(--dom-fg);border:1px solid var(--dom-line)}
.pct{color:var(--muted);font-family:var(--mono);font-size:11px;margin-left:4px}
.dom-note{display:block;margin-top:4px}
.empty{color:var(--muted)}
.more{display:block;text-align:center;padding:12px;font:inherit;font-size:13px;background:var(--accent-soft);
  border:1px solid var(--rule-strong);border-radius:6px;color:var(--fg);cursor:pointer;margin:12px 20px;width:calc(100% - 40px)}
.more:hover{filter:brightness(.97)}
.none{padding:30px 20px;color:var(--muted)}

@media (max-width:900px){
  header.top{padding:10px 12px 0}
  .controls{padding:10px 12px;gap:6px 8px}
  .field.wide input{min-width:180px}
  .summary{padding:10px 12px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
  .count{width:100%;margin-left:0;order:-1}
  td.en{max-width:none}
}
"""

SCRIPT = r"""
'use strict';
(function(){
  var enc = document.getElementById('enc');
  function parseTSV(id){
    var el = document.getElementById('data-' + id);
    // Some parsers report the newline straight after the open tag as the
    // first line; drop empty lines at both ends before reading the header.
    var lines = el.textContent.split('\n');
    while (lines.length && lines[0] === '') lines.shift();
    while (lines.length && lines[lines.length-1] === '') lines.pop();
    var head = lines.shift().split('\t');
    var out = new Array(lines.length);
    for (var i = 0; i < lines.length; i++){
      var parts = lines[i].split('\t');
      var o = Object.create(null);
      for (var j = 0; j < head.length; j++) o[head[j]] = parts[j] === undefined ? '' : parts[j];
      out[i] = o;
    }
    return out;
  }

  var woorden     = parseTSV('woorden');
  var woordsoort  = parseTSV('woordsoort');
  var thema       = parseTSV('thema');
  var domein      = parseTSV('domein');
  var niveauRows  = parseTSV('niveau');
  var knmKand     = parseTSV('knm-kandidaten');
  var knmThema    = parseTSV('knm-thema');
  var kandidaten  = parseTSV('kandidaten');

  var NON_PRODUCT = {algemeen:1, naam:1, plaats:1};
  var ABSTRACT_DOMAIN = 'Abstract & general';

  // ---- master rows: join on row position, never on the word ----
  var master = new Array(woorden.length);
  for (var i = 0; i < woorden.length; i++){
    var w = woorden[i], p = woordsoort[i], t = thema[i], d = domein[i], n = niveauRows[i];
    master[i] = {
      idx: i + 1,
      nl: w.nl, en: w.en, pos: p.pos, thema: t.thema, domein: d.domein,
      thema_ook: t.thema_ook,
      prioriteit: t.prioriteit,
      niveau: n.niveau, rang: n.rang, grondslag: n.grondslag,
      trede: w.niveau, top2000: w.top2000, herkomst: w.herkomst
    };
  }

  // ---- knm: left join on nl ----
  var themaByNl = Object.create(null);
  for (var k = 0; k < knmThema.length; k++){
    var tk = knmThema[k];
    if (!(tk.nl in themaByNl)) themaByNl[tk.nl] = tk;
  }
  var knm = knmKand.map(function(r){
    // knm-thema carries one row per word, but knm-kandidaten may list the same
    // word once per KNM section (e.g. "recht" appears five times). Fall back to
    // a whitespace-normalised key so those still find their theme row.
    var t = themaByNl[r.nl] || themaByNl[r.nl.replace(/\s+/g, ' ').trim()];
    return {
      nl: r.nl, en: r.en, knm_thema: r.knm_thema, knm_sectie: r.knm_sectie,
      thema: t ? t.thema : '', prioriteit: t ? t.prioriteit : '', waarom: t ? t.waarom : '',
      heeft_thema: !!t
    };
  });

  // ---- normalise: case- and accent-insensitive ----
  if (String.prototype.normalize){
    var normCache = Object.create(null);
    var norm = function(s){
      var hit = normCache[s];
      if (hit !== undefined) return hit;
      var v = s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      normCache[s] = v;
      return v;
    };
  } else {
    var norm = function(s){ return s.toLowerCase(); };
  }

  // Collator: language-aware where available, accent-aware but case-insensitive.
  var collator;
  try { collator = new Intl.Collator('nl', {numeric:true, sensitivity:'base'}); }
  catch(e){ collator = null; }
  function cmpStr(a, b){
    if (a === b) return 0;
    if (a === '') return 1;      // blanks last
    if (b === '') return -1;
    if (collator) return collator.compare(a, b);
    return a < b ? -1 : 1;
  }
  function cmpNum(a, b){
    var na = a === '' ? null : Number(a), nb = b === '' ? null : Number(b);
    if (na === null && nb === null) return 0;
    if (na === null) return 1;
    if (nb === null) return -1;
    return na - nb;
  }

  // ---- palettes: restrained, deterministic; stable per value within a view ----
  function hueOf(s){
    var h = 2166136261;
    for (var i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return (h >>> 0);
  }
  var chipCache = Object.create(null);
  function chip(value, kind){
    if (!value) return '<span class="empty">—</span>';
    var key = kind + ':' + value;
    var style = chipCache[key];
    if (style === undefined){
      var h = hueOf(value) % 360;
      style = '--c:hsl(' + h + ' 46% 93%);--ct:hsl(' + h + ' 42% 26%)';
      chipCache[key] = style;
    }
    return '<span class="chip" style="' + style + '">' + esc(value) + '</span>';
  }
  function esc(s){
    return String(s).replace(/[&<>"]/g, function(c){
      return c === '&' ? '&amp;' : c === '<' ? '&lt;' : c === '>' ? '&gt;' : '&quot;';
    });
  }

  // Domains are English semantic fields; themes are Dutch product situations.
  // A domain chip is a square, grey, sans-serif label; a theme chip is a round
  // coloured pill. The two axes must never look alike.
  function dchip(v){
    if (!v) return '<span class="empty">—</span>';
    return '<span class="chip domein" title="semantic field">' + esc(v) + '</span>';
  }

  // Domains are English semantic fields; themes are Dutch product situations.
  // A domain chip is a square, grey, sans-serif label; a theme chip is a round
  // coloured pill. The two axes must never look alike.
  function dchip(v){
    if (!v) return '<span class="empty">—</span>';
    return '<span class="chip domein" title="semantic field">' + esc(v) + '</span>';
  }

  // ---- views ----
  function countBy(rows, get){
    var m = Object.create(null);
    for (var i = 0; i < rows.length; i++){
      var v = get(rows[i]);
      if (v) m[v] = (m[v] || 0) + 1;
    }
    return m;
  }
  function sortedEntries(m, byCount){
    var e = Object.keys(m).map(function(k){ return [k, m[k]]; });
    e.sort(function(a, b){
      if (byCount && b[1] !== a[1]) return b[1] - a[1];
      return cmpStr(a[0], b[0]);
    });
    return e;
  }
  function herkomstParts(v){ return v ? v.split(';') : []; }

  // Which KNM rows found no theme row; surfaced in the tab so a reader knows
  // the blank theme comes from the source, not from the join.
  var knmMissing = knm.filter(function(r){ return !r.heeft_thema; }).length;

  var MODES = {
    master: {
      data: master,
      columns: [
        {key:'idx',       label:'#',         type:'num',  sortBy:function(r){return String(r.idx);}, cell:function(r){return String(r.idx);}, cls:'num'},
        {key:'nl',        label:'nl',        type:'str',  cell:function(r){return r.nl;}, cls:'nl'},
        {key:'en',        label:'en',        type:'str',  cell:function(r){return r.en;}, cls:'en'},
        {key:'pos',       label:'pos',       type:'str',  cell:function(r){return r.pos;}, cls:'nowrap'},
        {key:'thema',     label:'thema',     type:'str',  cell:function(r){return chip(r.thema, 'thema');}},
        {key:'domein',    label:'domein',    type:'str',  cell:function(r){return dchip(r.domein);}, cls:'nowrap'},
        {key:'thema_ook', label:'thema_ook', type:'str',  cell:function(r){
            if (!r.thema_ook) return '<span class="empty">—</span>';
            return r.thema_ook.split(';').map(function(p){ return chip(p, 'thema'); }).join(' ');
          }},
        {key:'prioriteit',label:'prioriteit',type:'str',  cell:function(r){return r.prioriteit || '<span class="empty">—</span>';}, cls:'nowrap'},
        {key:'niveau',    label:'niveau',    type:'str',  cell:function(r){return r.niveau;}, cls:'nowrap'},
        {key:'rang',      label:'rang',      type:'num',  sortBy:function(r){return r.rang;}, cell:function(r){return r.rang;}, cls:'num'},
        {key:'trede',     label:'trede',     type:'str',  cell:function(r){return r.trede || '<span class="empty">—</span>';}, cls:'nowrap'},
        {key:'grondslag', label:'grondslag', type:'str',  cell:function(r){return r.grondslag;}, cls:'mono'},
        {key:'top2000',   label:'top2000',   type:'num',  sortBy:function(r){return r.top2000;}, cell:function(r){return r.top2000 || '<span class="empty">—</span>';}, cls:'mono'},
        {key:'herkomst',  label:'herkomst',  type:'str',  cell:function(r){return r.herkomst;}, cls:'mono herk'}
      ],
      search: function(r){ return norm(r.nl) + ' ' + norm(r.en); },
      filters: [
        {key:'pos',        label:'pos',        get:function(r){ return r.pos ? [r.pos] : []; }},
        {key:'thema',      label:'thema',      get:function(r){ return r.thema ? [r.thema] : []; }},
        {key:'domein',     label:'domein',     get:function(r){ return r.domein ? [r.domein] : []; }},
        {key:'prioriteit', label:'prioriteit', get:function(r){ return r.prioriteit ? [r.prioriteit] : []; }},
        {key:'niveau',     label:'niveau (ons)', get:function(r){ return r.niveau ? [r.niveau] : []; }},
        {key:'trede',      label:'appendix-trede', get:function(r){ return [r.trede || '(geen)']; }},
        {key:'herkomst',   label:'herkomst',   get:function(r){ return herkomstParts(r.herkomst); }, multi:true}
      ],
      defaultSort: {key:'idx', dir:1}
    },
    knm: {
      data: knm,
      columns: [
        {key:'idx',        label:'#',          type:'num', sortBy:function(r){return String(r._i);}, cell:function(r){return String(r._i);}, cls:'num'},
        {key:'nl',         label:'nl',         type:'str', cell:function(r){return r.nl;}, cls:'nl'},
        {key:'en',         label:'en',         type:'str', cell:function(r){return r.en;}, cls:'en'},
        {key:'knm_thema',  label:'knm_thema',  type:'str', cell:function(r){return r.knm_thema;}, cls:'nowrap'},
        {key:'knm_sectie', label:'knm_sectie', type:'str', cell:function(r){return r.knm_sectie;}},
        {key:'thema',      label:'thema',      type:'str', cell:function(r){return chip(r.thema, 'thema');}},
        {key:'prioriteit', label:'prioriteit', type:'str', cell:function(r){return r.prioriteit || '<span class="empty">—</span>';}, cls:'nowrap'},
        {key:'waarom',     label:'waarom',     type:'str', cell:function(r){return r.waarom ? r.waarom : '<span class="empty">—</span>';}}
      ],
      search: function(r){ return norm(r.nl) + ' ' + norm(r.en) + ' ' + norm(r.knm_sectie); },
      filters: [
        {key:'knm_thema',  label:'knm_thema',  get:function(r){ return r.knm_thema ? [r.knm_thema] : []; }},
        {key:'knm_sectie', label:'knm_sectie', get:function(r){ return r.knm_sectie ? [r.knm_sectie] : []; }},
        {key:'thema',      label:'thema',      get:function(r){ return r.thema ? [r.thema] : []; }},
        {key:'prioriteit', label:'prioriteit', get:function(r){ return r.prioriteit ? [r.prioriteit] : []; }}
      ],
      defaultSort: {key:'idx', dir:1}
    },
    kandidaten: {
      data: kandidaten,
      columns: [
        {key:'idx',      label:'#',        type:'num', sortBy:function(r){return String(r._i);}, cell:function(r){return String(r._i);}, cls:'num'},
        {key:'nl',       label:'nl',       type:'str', cell:function(r){return r.nl;}, cls:'nl'},
        {key:'en',       label:'en',       type:'str', cell:function(r){return r.en;}, cls:'en'},
        {key:'bron',     label:'bron',     type:'str', cell:function(r){return r.bron;}, cls:'mono en'},
        {key:'licentie', label:'licentie', type:'str', cell:function(r){return r.licentie;}, cls:'nowrap'}
      ],
      search: function(r){ return norm(r.nl) + ' ' + norm(r.en); },
      filters: [
        {key:'bron',     label:'bron',     get:function(r){ return r.bron ? [r.bron] : []; }},
        {key:'licentie', label:'licentie', get:function(r){ return r.licentie ? [r.licentie] : []; }}
      ],
      defaultSort: {key:'idx', dir:1}
    }
  };
  knm.forEach(function(r, n){ r._i = n + 1; });
  kandidaten.forEach(function(r, n){ r._i = n + 1; });

  // ---- state ----
  var state = {mode:'master', sort:{}, query:{}, filter:{}, limit:500};
  var PAGE = 500;
  Object.keys(MODES).forEach(function(m){
    state.sort[m] = {key:MODES[m].defaultSort.key, dir:MODES[m].defaultSort.dir};
    state.query[m] = '';
    state.filter[m] = Object.create(null);
  });

  // A row passes a filter when any of its components is selected. For a
  // multi-valued filter the value may be "spel:*", meaning any game word.
  function passesFilters(mode, r, skipKey){
    var fs = MODES[mode].filters;
    for (var i = 0; i < fs.length; i++){
      var f = fs[i];
      if (skipKey && f.key === skipKey) continue;
      var want = state.filter[mode][f.key];
      if (!want) continue;
      var vals = f.get(r);
      var ok = false;
      for (var j = 0; j < vals.length; j++){
        var v = vals[j];
        if (!v) continue;
        if (want[v]){ ok = true; break; }
        if (f.multi && want['spel:*'] && v.indexOf('spel:') === 0){ ok = true; break; }
      }
      if (!ok) return false;
    }
    return true;
  }

  // Options show how many rows of the *current* view carry each value, i.e.
  // with the search and the other filters applied, so the numbers stay useful.
  function filterOptions(mode, f){
    var rows = MODES[mode].data;
    var counts = Object.create(null);
    var spel = 0;
    for (var i = 0; i < rows.length; i++){
      var r = rows[i];
      if (!passesFilters(mode, r, f.key)) continue;
      var vals = f.get(r);
      var seen = Object.create(null);
      var hasSpel = false;
      for (var j = 0; j < vals.length; j++){
        var v = vals[j];
        if (!v || seen[v]) continue;
        seen[v] = 1;
        counts[v] = (counts[v] || 0) + 1;
        if (f.multi && v.indexOf('spel:') === 0) hasSpel = true;
      }
      if (hasSpel) spel++;
    }
    return {counts:counts, spel:spel};
  }

  function currentRows(){
    var mode = state.mode, M = MODES[mode];
    var q = norm(state.query[mode].trim());
    var terms = q ? q.split(/\s+/) : [];
    var out = [];
    var rows = M.data;
    for (var i = 0; i < rows.length; i++){
      var r = rows[i];
      if (terms.length){
        var hay = M.search(r);
        var all = true;
        for (var t = 0; t < terms.length; t++){ if (hay.indexOf(terms[t]) === -1){ all = false; break; } }
        if (!all) continue;
      }
      if (!passesFilters(mode, r)) continue;
      out.push(r);
    }
    var s = state.sort[mode];
    var col = null;
    for (var c = 0; c < M.columns.length; c++) if (M.columns[c].key === s.key) col = M.columns[c];
    if (col){
      var getv = col.sortBy || function(r){ return String(r[col.key] || ''); };
      var dir = s.dir;
      var isNum = col.type === 'num';
      out.sort(function(a, b){
        var va = getv(a), vb = getv(b);
        var d = isNum ? cmpNum(va, vb) : cmpStr(va, vb);
        if (d === 0){ d = a._i - b._i; }
        return d * dir;
      });
    }
    return out;
  }

  // ---- rendering ----
  var $ = function(id){ return document.getElementById(id); };
var tbody = $('tbody'), thead = $('thead-row'), countEl = $('count'), moreBtn = $('more');
  var emptyMsg = $('none');
  var FOCUS = {key:''};

  function renderHead(mode){
    var M = MODES[mode], s = state.sort[mode];
    var html = '';
    for (var i = 0; i < M.columns.length; i++){
      var c = M.columns[i];
      var arrow = s.key === c.key ? '<span class="arrow">' + (s.dir > 0 ? '\u25B2' : '\u25BC') + '</span>' : '';
      html += '<th data-key="' + c.key + '" title="click to sort"><span class="lbl">' + esc(c.label) + '</span>' + arrow + '</th>';
    }
    thead.innerHTML = html;
  }

  function renderFilters(mode){
    var M = MODES[mode];
    var holder = $('filters');
    var html = '';
    for (var i = 0; i < M.filters.length; i++){
      var f = M.filters[i];
      var opts = filterOptions(mode, f);
      var entries = sortedEntries(opts.counts, false);
      var sel = state.filter[mode][f.key] || {};
      var all = countsFor(mode, f);
      html += '<div class="field"><label for="f-' + mode + '-' + f.key + '">' + esc(f.label) + '</label>' +
              '<select id="f-' + mode + '-' + f.key + '" data-fkey="' + f.key + '">' +
              '<option value="">all (' + all.toLocaleString('en-US') + ')</option>';
      if (f.multi && opts.spel){
        html += '<option class="grp" value="spel:*"' + (sel['spel:*'] ? ' selected' : '') +
                '>spel:* — any game word (' + opts.spel.toLocaleString('en-US') + ')</option>';
      }
      for (var j = 0; j < entries.length; j++){
        var v = entries[j][0];
        html += '<option value="' + esc(v) + '"' + (sel[v] ? ' selected' : '') + '>' +
                esc(v) + ' (' + entries[j][1].toLocaleString('en-US') + ')</option>';
      }
      html += '</select></div>';
    }
    holder.innerHTML = html;
    var sels = holder.querySelectorAll('select');
    for (var k = 0; k < sels.length; k++){
      sels[k].addEventListener('change', function(ev){
        var fk = ev.target.getAttribute('data-fkey');
        var v = ev.target.value;
        var next = Object.create(null);
        if (v) next[v] = 1;
        state.filter[mode][fk] = next;
        state.limit = PAGE;
        FOCUS.key = fk;
        render();
        FOCUS.key = '';
      });
    }
  }

  // "all" should mean all rows that pass the other filters, not the file size.
  function countsFor(mode, f){
    var rows = MODES[mode].data, n = 0;
    for (var i = 0; i < rows.length; i++) if (passesFilters(mode, rows[i], f.key)) n++;
    return n;
  }

  function renderSummary(mode){
    var box = $('summary');
    if (mode !== 'master'){
      box.innerHTML = '';
      box.style.display = 'none';
      return;
    }
    box.style.display = '';
    var pos = sortedEntries(countBy(master, function(r){ return r.pos; }), true);
    var pri = sortedEntries(countBy(master, function(r){ return r.prioriteit; }), true);
    var nivCounts = countBy(master, function(r){ return r.niveau; });
    var BANDS = ['Start', 'Basis', 'Midden', 'Gevorderd', 'Verdieping'];
    var CEFR = {Start:'\u2248A0-A1', Basis:'\u2248A1-A2', Midden:'\u2248A2-B1',
                Gevorderd:'\u2248B1-B2', Verdieping:'\u2248B2+' };
    // Band order is meaningful, so do not sort this list by count.
    var niv = BANDS.map(function(b){ return [b + '  ' + CEFR[b], nivCounts[b] || 0]; });
    var tredeE = sortedEntries(countBy(master, function(r){ return r.trede || '(geen)'; }), true);
    var hk = Object.create(null);
    for (var i = 0; i < master.length; i++){
      var parts = herkomstParts(master[i].herkomst);
      var hit = Object.create(null);
      for (var j = 0; j < parts.length; j++) if (parts[j]) hit[parts[j]] = 1;
      for (var k in hit) hk[k] = (hk[k] || 0) + 1;
    }
    var hke = sortedEntries(hk, false);
    var the = Object.create(null);
    var themed = 0;
    for (var t = 0; t < master.length; t++){
      var th = master[t].thema;
      if (!th) continue;
      the[th] = (the[th] || 0) + 1;
      if (!NON_PRODUCT[th]) themed++;
    }
    var theE = sortedEntries(the, true);

    var dom = sortedEntries(countBy(master, function(r){ return r.domein; }), true);
    var abstractN = 0;
    for (var d = 0; d < dom.length; d++) if (dom[d][0] === ABSTRACT_DOMAIN) abstractN = dom[d][1];
    var abstractPct = master.length ? (abstractN * 100 / master.length) : 0;
    var domPct = function(n){ return (n * 100 / master.length).toFixed(1) + '%'; };

    function list(title, entries, open, pct){
      var rows = entries.map(function(e){
        return '<div class="kv"><span class="lbl" title="' + esc(e[0]) + '">' + esc(e[0]) + '</span>' +
               '<span class="num">' + e[1].toLocaleString('en-US') + '</span></div>';
      }).join('');
      if (open === undefined) return '<section><h2>' + title + '</h2>' + rows + '</section>';
      // Collapsed lists keep their total in the summary line so the panel stays
      // short; open the ones the reader is most likely to want at a glance.
      var total = entries.reduce(function(a, e){ return a + e[1]; }, 0);
      var body = rows;
      if (pct) body = entries.map(function(e){
        return '<div class="kv"><span class="lbl" title="' + esc(e[0]) + '">' + esc(e[0]) + '</span>' +
               '<span class="num">' + e[1].toLocaleString('en-US') +
               ' <span class="pct">' + domPct(e[1]) + '</span></span></div>';
      }).join('');
      return '<section><details' + (open ? ' open' : '') + '><summary>' + title +
             ' <span class="n">' + entries.length + ' &middot; ' + total.toLocaleString('en-US') + '</span></summary>' +
             '<div class="theme-grid">' + body + '</div></details></section>';
    }
    box.innerHTML =
      '<div class="themed-note">themed: <b>' + themed.toLocaleString('en-US') + '</b> of <b>' +
        master.length.toLocaleString('en-US') + '</b> ' +
        '<span class="empty">(product themes only; excludes ' + Object.keys(NON_PRODUCT).join(', ') + ')</span><br>' +
        '<span class="dom-note">' + esc(ABSTRACT_DOMAIN) + ': <b>' + abstractN.toLocaleString('en-US') + '</b>' +
        ' of <b>' + master.length.toLocaleString('en-US') + '</b> = <b>' + abstractPct.toFixed(1) + '%</b>' +
        ' <span class="empty">(semantic fields, the other axis)</span></span><br>' +
        '<span class="dom-note">niveau is ours: five frequency bands, every row has one. ' +
        'trede is the appendix tier (A1/B1/open), blank for 4,839 rows \u2014 source ' +
        'evidence, not a level; the CEFR ranges beside a band are an approximation.</span></div>' +
      list('pos', pos, true) + list('prioriteit', pri, true) +
      list('niveau (ours, by frequency rank)', niv, true) +
      list('appendix-trede (coursebook evidence)', tredeE, true) +
      list('herkomst', hke, false) +
      list('thema', theE, false) +
      list('domein', dom, false, true);
  }

  function render(){
    var mode = state.mode, M = MODES[mode];
    renderHead(mode);
    renderSummary(mode);
    renderFilters(mode);
    var rows = currentRows();
    var shown = Math.min(rows.length, state.limit);
    var html = [];
    for (var i = 0; i < shown; i++){
      var r = rows[i];
      html.push('<tr>');
      for (var c = 0; c < M.columns.length; c++){
        var col = M.columns[c];
        html.push('<td' + (col.cls ? ' class="' + col.cls + '"' : '') + '>' + col.cell(r) + '</td>');
      }
      html.push('</tr>');
    }
    tbody.innerHTML = html.join('');
    var total = M.data.length;
    countEl.innerHTML = 'showing <b>' + shown.toLocaleString('en-US') + '</b> of <b>' +
      rows.length.toLocaleString('en-US') + '</b>' +
      (rows.length !== total ? ' matching (' + total.toLocaleString('en-US') + ' in file)' : '');
    moreBtn.style.display = rows.length > shown ? '' : 'none';
    if (rows.length > shown) moreBtn.textContent = 'show more (' + (rows.length - shown).toLocaleString('en-US') + ' rows not shown)';
    emptyMsg.style.display = rows.length ? 'none' : '';
  }

  // ---- events ----
  thead.addEventListener('click', function(ev){
    var th = ev.target.closest('th');
    if (!th) return;
    var key = th.getAttribute('data-key');
    var s = state.sort[state.mode];
    if (s.key === key) s.dir = -s.dir;
    else { s.key = key; s.dir = 1; }
    if (key === 'idx') s.dir = 1;      // the default is always file order ascending
    render();
  });
  $('search').addEventListener('input', function(ev){
    state.query[state.mode] = ev.target.value;
    state.limit = PAGE;
    render();
  });
  $('reset').addEventListener('click', function(){
    var m = state.mode;
    state.sort[m] = {key:MODES[m].defaultSort.key, dir:MODES[m].defaultSort.dir};
    state.query[m] = '';
    state.filter[m] = Object.create(null);
    state.limit = PAGE;
    $('search').value = '';
    render();
  });
  moreBtn.addEventListener('click', function(){
    state.limit += PAGE * 4;
    render();
  });
  var tabs = $('tabs').querySelectorAll('button');
  for (var i = 0; i < tabs.length; i++){
    tabs[i].addEventListener('click', function(ev){
      var btn = ev.currentTarget;
      state.mode = btn.getAttribute('data-mode');
      state.limit = PAGE;
      for (var j = 0; j < tabs.length; j++) tabs[j].setAttribute('aria-selected', tabs[j] === btn ? 'true' : 'false');
      $('search').value = state.query[state.mode];
      $('search').placeholder = state.mode === 'master' ? 'search nl or en (accent-insensitive)' : 'search nl or en';
      render();
    });
  }

  $('tabs').querySelector('[data-mode="master"]').click();
  $('meta').textContent = 'woorden ' + master.length.toLocaleString('en-US') +
    ' · knm ' + knm.length.toLocaleString('en-US') +
    ' (' + knmMissing + ' without a theme row)' +
    ' · kandidaten ' + kandidaten.length.toLocaleString('en-US') +
    ' · five files joined on position, not on the word';
})();
"""


def build() -> None:
    data: dict[str, list[list[str]]] = {}
    headers: dict[str, list[str]] = {}
    for key, name, rows, cols in DATASETS:
        path = HERE / name
        if not path.exists():
            fail(f"missing input {path}")
        data[key] = read_tsv(path, cols, rows)
        headers[key] = cols
        print(f"bouw-viewer: read {name}: {len(data[key])} rows, {len(cols)} columns")

    verify(data)

    blocks = []
    for key, _name, _rows, cols in DATASETS:
        blocks.append('<script type="text/plain" id="data-' + key + '">\n' + embed_tsv(data[key], cols) + '</script>')
    data_html = "\n".join(blocks)

    counts = {key: len(data[key]) for key, *_ in DATASETS}

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lexicon viewer — oefenpad</title>
<style>{STYLE}</style>
</head>
<body>
<header class="top">
  <h1>Lexicon viewer</h1>
  <div class="sub" id="meta">built from the TSVs in tools/lexicon by bouw-viewer.py</div>
  <nav class="tabs" id="tabs" role="tablist">
    <button role="tab" data-mode="master" aria-selected="true">Master<span class="n">{counts['woorden']:,}</span></button>
    <button role="tab" data-mode="knm" aria-selected="false">KNM<span class="n">{counts['knm-kandidaten']:,}</span></button>
    <button role="tab" data-mode="kandidaten" aria-selected="false">Kandidaten<span class="n">{counts['kandidaten']:,}</span></button>
  </nav>
</header>

<div class="controls">
  <div class="field wide"><label for="search">search</label>
    <input id="search" type="search" autocomplete="off" spellcheck="false" placeholder="search nl or en (accent-insensitive)">
  </div>
  <div id="filters" style="display:contents"></div>
  <button class="reset" id="reset" type="button">reset</button>
  <div class="count" id="count"></div>
</div>

<div class="summary" id="summary"></div>

<div class="tablewrap">
  <table>
    <thead><tr id="thead-row"></tr></thead>
    <tbody id="tbody"></tbody>
  </table>
  <button class="more" id="more" type="button" style="display:none">show more</button>
  <div class="none" id="none" style="display:none">nothing matches these filters.</div>
</div>

{data_html}
<script>{SCRIPT}</script>
</body>
</html>
"""
    # Normalise line endings and refuse to ship any external reference.
    if not html.endswith("\n"):
        html += "\n"
    for bad in ("http://", "https://", "//cdn", "src=", "fetch(", "XMLHttpRequest", "@import", "<link"):
        if bad in html:
            fail(f"generated page contains forbidden token {bad!r}")
    OUT.write_bytes(html.encode("utf-8"))
    print(f"bouw-viewer: wrote {OUT.name}: {len(html.encode('utf-8'))} bytes")


if __name__ == "__main__":
    build()

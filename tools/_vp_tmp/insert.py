"""Insert new chunk groups / clusters into the voorzetselpaden band pages.

Scratch tool for the 15 Nov 2026 verb-preposition audit. Reads GROUPS lists
from data_a.py and data_more.py and rewrites the band pages in place.

Actions per group:
  single   - new cluster section with one chunk, no <h2>, placed at the end
             of the Single frames run
  cluster  - new contrast section with <h2>preps</h2>, placed at the end of
             the Contrast sets run
  append   - extra chunk group added to an existing section, counts and
             <h2> prepositions refreshed
  convert  - an existing single section gains a partner and becomes a
             contrast set, moved up into the Contrast sets run
"""
import re
import sys

sys.path.insert(0, 'tools/_vp_tmp')

PAGES = ['a0', 'a1', 'a2', 'a2-pairs', 'a2-plus', 'b1', 'b1-plus', 'b2']
SINGLE_KOP = '<section class="sectiekop"><h2>Single frames</h2>'
RESTORED_KOP = '<section class="sectiekop"><h2>Restored</h2>'


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace("'", '&#x27;'))


def card_html(g, ch, c):
    b = c['builds']
    return (
        '<article class="kaart" data-id="{id}" data-band="{band}" '
        'data-kind="proposal" data-status="planned" data-row="" data-severity="">'
        '<p class="geenbeeld">not drawn yet</p>'
        '<h3 class="chunk">{chunk}</h3><p class="gloss">{gloss}</p><dl>'
        '<dt>Scene</dt><dd class="scene">{scene}</dd>'
        '<dt>Must read</dt><dd class="must">{must}</dd>'
        '<dt>Avoid</dt><dd class="avoid">{avoid}</dd>'
        '<dt>Pair / note</dt><dd class="note">{note}</dd>'
        '<dt>Example</dt><dd class="voorbeeld-nl">{nl}<br>'
        '<span class="voorbeeld-en">{en}</span></dd>'
        '<dt>Build</dt><dd class="bouw">{b0}</dd>'
        '<dt>Build</dt><dd class="bouw">{b1}</dd>'
        '<dt>Check question</dt><dd class="controlevraag">{q} '
        '<strong class="antwoord">{ans}</strong></dd>'
        '<dt>Alt text</dt><dd class="alt">{alt}</dd>'
        '</dl><p class="id">{id}.png · nieuw</p></article>'
    ).format(id=c['id'], band=g['band'], chunk=esc(ch['chunk']), gloss=esc(ch['gloss']),
             scene=esc(c['scene']), must=esc(c['must']), avoid=esc(c['avoid']),
             note=esc(c['note']), nl=esc(c['nl']), en=esc(c['en']),
             b0=esc(b[0]), b1=esc(b[1]), q=esc(c['q']), ans=c['answer'],
             alt=esc(c['alt']))


def group_html(g, ch):
    n = len(ch['cards'])
    if n >= 3:
        telling = '%d examples' % n
    else:
        telling = ('<span class="tekort">%d example%s — needs at least 3</span>'
                   % (n, '' if n == 1 else 's'))
    cards = ''.join(card_html(g, ch, c) for c in ch['cards'])
    return ('<div class="chunkgroep" data-chunk="{chunk}" data-examples="{n}">'
            '<h3>{chunk}</h3><p class="telling">{telling}</p>'
            '<div class="kaarten">{cards}</div></div>').format(
                chunk=esc(ch['chunk']), n=n, telling=telling, cards=cards)


def section_span(s, stem):
    m = re.search(r'<section class="cluster" data-stem="%s">\n(.*?)</section>\n'
                  % re.escape(stem), s, re.S)
    return m


def counts(section):
    n_cards = sum(int(x) for x in re.findall(r'data-examples="(\d+)"', section))
    n_groups = len(re.findall(r'<div class="chunkgroep"', section))
    return n_groups, n_cards


def set_preps(section, stem, preps):
    new_h2 = '<h2>%s<span class="preps">%s</span></h2>' % (esc(stem), ' · '.join(preps))
    if '<h2>' in section:
        return re.sub(r'<h2>.*?</h2>', new_h2, section, count=1, flags=re.S)
    # first line is the <section ...> opening; insert after it
    i = section.index('\n') + 1
    return section[:i] + new_h2 + '\n' + section[i:]


def counts_line(n_groups, n_cards):
    return '%d %s, %d %s' % (n_groups, 'preposition' if n_groups == 1 else 'prepositions',
                             n_cards, 'card' if n_cards == 1 else 'cards')


def set_noot(section, noot):
    n_groups, n_cards = counts(section)
    # A cluster counts its distinct prepositions, not its chunk groups: three
    # chunks that all take aan are one preposition, three cards.
    m = re.search(r'<span class="preps">(.*?)</span>', section, re.S)
    if m:
        n_groups = len([x for x in m.group(1).split(' · ') if x.strip()])
    base = counts_line(n_groups, n_cards)
    if noot:
        base += ' · ' + noot
    line = '<p class="contrastnoot">%s</p>' % base
    if '<p class="contrastnoot">' in section:
        return re.sub(r'<p class="contrastnoot">.*?</p>', lambda m: line, section,
                      count=1, flags=re.S)
    i = section.index('\n') + 1
    if section[i:i + 4] == '<h2>':
        i = section.index('\n', i) + 1
    return section[:i] + line + '\n' + section[i:]


def append_groups(section, group):
    """Add the group's chunk groups after the last chunk group in the section."""
    html = '\n'.join(group_html(group, ch) for ch in group['chunks'])
    last = list(re.finditer(r'<div class="chunkgroep".*?</div></div>\n', section, re.S))
    if not last:
        raise SystemExit('no chunk group to append after in %r' % group['stem'])
    end = last[-1].end()
    return section[:end] + html + '\n' + section[end:]


def new_section(group):
    body = '\n'.join(group_html(group, ch) for ch in group['chunks'])
    if group['action'] == 'cluster':
        preps = group['preps']
        n_groups = len(preps)
        n_cards = sum(len(ch['cards']) for ch in group['chunks'])
        noot = group.get('noot')
        line = counts_line(n_groups, n_cards)
        if noot:
            line += ' · ' + noot
        head = ('<section class="cluster" data-stem="%s">\n'
                '<h2>%s<span class="preps">%s</span></h2>\n'
                '<p class="contrastnoot">%s</p>\n'
                % (esc(group['stem']), esc(group['stem']), ' · '.join(preps), line))
    else:
        noot = group.get('noot')
        head = '<section class="cluster" data-stem="%s">\n' % esc(group['stem'])
        if noot:
            head += '<p class="contrastnoot">%s</p>\n' % noot
    return head + body + '\n</section>\n'


def apply_page(page, groups):
    path = 'Docs/voorzetselpaden/%s.html' % page
    s = open(path, encoding='utf-8').read()
    before_ids = set(re.findall(r'data-id="([^"]+)"', s))
    for g in groups:
        action = g['action']
        if action in ('single', 'cluster'):
            sec = new_section(g)
            if action == 'cluster':
                i = s.index(SINGLE_KOP)
                s = s[:i] + sec + s[i:]
            else:
                i = s.find(RESTORED_KOP)
                if i == -1:
                    i = s.index('</main>')
                s = s[:i] + sec + s[i:]
        elif action == 'append':
            m = section_span(s, g['stem'])
            if not m:
                raise SystemExit('%s: no section for stem %r' % (page, g['stem']))
            sec = m.group(0)
            sec = append_groups(sec, g)
            sec = set_preps(sec, g['stem'], g['preps'])
            sec = set_noot(sec, g.get('noot'))
            s = s[:m.start()] + sec + s[m.end():]
        elif action == 'convert':
            m = section_span(s, g['stem'])
            if not m:
                raise SystemExit('%s: no section for stem %r' % (page, g['stem']))
            sec = m.group(0)
            sec = append_groups(sec, g)
            sec = set_preps(sec, g['stem'], g['preps'])
            sec = set_noot(sec, g.get('noot'))
            s = s[:m.start()] + s[m.end():]
            i = s.index(SINGLE_KOP)
            s = s[:i] + sec + s[i:]
        else:
            raise SystemExit('unknown action %r' % action)
    after_ids = re.findall(r'data-id="([^"]+)"', s)
    dupes = sorted({x for x in after_ids if after_ids.count(x) > 1})
    if dupes:
        raise SystemExit('%s: duplicate ids %s' % (page, dupes))
    open(path, 'w', encoding='utf-8').write(s)
    print('%-10s %d groups, %d new cards, %d -> %d ids'
          % (page, len(groups), len(after_ids) - len(before_ids),
             len(before_ids), len(after_ids)))


def normalise(groups):
    """Fill in 'action' for the data_a entries, which predate the key."""
    pages = {p: open('Docs/voorzetselpaden/%s.html' % p, encoding='utf-8').read()
             for p in PAGES}
    for g in groups:
        if g.get('action'):
            continue
        s = pages[g['page'].replace('.html', '')]
        m = section_span(s, g['stem'])
        if g.get('append') or g.get('preps'):
            if m is None:
                g['action'] = 'cluster' if g.get('preps') else 'single'
            elif '<h2>' in m.group(0):
                g['action'] = 'append'
            else:
                g['action'] = 'convert'
        else:
            g['action'] = 'single' if m is None else 'append'
        g.setdefault('preps', None)
    return groups


def main():
    import data_a
    groups = list(data_a.GROUPS)
    for name in ('data_more', 'data_more2'):
        try:
            mod = __import__(name)
        except ImportError:
            print('(%s.py not found)' % name)
            continue
        groups += list(mod.GROUPS)
    groups = normalise(groups)
    by_page = {}
    for g in groups:
        by_page.setdefault(g['page'].replace('.html', ''), []).append(g)
    for page in PAGES:
        if page in by_page:
            apply_page(page, by_page[page])


if __name__ == '__main__':
    main()

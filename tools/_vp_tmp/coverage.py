"""Measure which ZiN / HDH verb+preposition entries the band pages cover.

Normalises a chunk to (verb, last token): drops zich/zijn/hebben/iemand/iets
and the indefinite article, then compares the first and last surviving token.
That is loose enough to see 'zich aanpassen aan' = 'aanpassen aan' but still
separates 'denken aan' from 'denken om'.
"""
import re
import sys
import unicodedata

sys.path.insert(0, 'tools/_vp_tmp')
import refs

PAGES = ['a0', 'a1', 'a2', 'a2-pairs', 'a2-plus', 'b1', 'b1-plus', 'b2']
DROP = {'zich', 'zijn', 'hebben', 'heb', 'heeft', 'had', 'iemand', 'iets',
        'het', 'een', 'de', 'er', 'zichzelf', 'je', 'men'}


def norm(chunk):
    chunk = unicodedata.normalize('NFKD', chunk.lower())
    chunk = ''.join(c for c in chunk if not unicodedata.combining(c))
    words = re.findall(r"[a-z]+", chunk)
    keep = [w for w in words if w not in DROP]
    if not keep:
        return None
    return (keep[0], keep[-1])


def corpus():
    """chunk string -> list of pages it appears on."""
    found = {}
    for p in PAGES:
        s = open('Docs/voorzetselpaden/%s.html' % p, encoding='utf-8').read()
        for m in re.finditer(r'data-chunk="([^"]+)"', s):
            found.setdefault(m.group(1), []).append(p)
    return found


def main():
    c = corpus()
    keys = {}
    for chunk in c:
        k = norm(chunk)
        if k:
            keys.setdefault(k, []).append(chunk)
    print('distinct chunks on the pages: %d' % len(c))
    for name, entries in (('ZiN', refs.ZIN), ('HDH', refs.HDH)):
        missing = []
        for e in entries:
            k = norm(e)
            if k not in keys:
                missing.append(e)
        print('\n%s: %d entries, %d missing' % (name, len(entries), len(missing)))
        for e in missing:
            print('   ', e)


if __name__ == '__main__':
    main()

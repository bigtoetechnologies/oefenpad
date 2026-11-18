"""Apply only the audit batches (data_more*.py) to the band pages.

insert.main() also re-applies data_a, which is already in the pages and is not
idempotent. This runner loads the new batches only. Pages are backed up to
tools/_vp_tmp/backup2/ before the first write.
"""
import os
import shutil
import sys

sys.path.insert(0, 'tools/_vp_tmp')
import insert

MODULES = ['data_more', 'data_more2', 'data_more3', 'data_more4', 'data_more5']
KEYS = {'id', 'scene', 'must', 'avoid', 'note', 'nl', 'en', 'builds', 'q',
        'answer', 'alt'}


def check(groups):
    ids = []
    for g in groups:
        for ch in g['chunks']:
            for c in ch['cards']:
                missing = KEYS - set(c)
                if missing:
                    raise SystemExit('%s: missing %s' % (c.get('id'), missing))
                if len(c['builds']) != 2 or not all(c['builds']):
                    raise SystemExit('%s: builds' % c['id'])
                if c['answer'] not in ('Ja', 'Nee'):
                    raise SystemExit('%s: answer %r' % (c['id'], c['answer']))
                ids.append(c['id'])
    dupes = sorted({x for x in ids if ids.count(x) > 1})
    if dupes:
        raise SystemExit('duplicate ids in the batches: %s' % dupes)
    return len(groups), len(ids)


def main():
    groups = []
    for name in MODULES:
        groups += list(__import__(name).GROUPS)
    groups = insert.normalise(groups)
    print('validated: %d groups, %d cards' % check(groups))

    pages = sorted({g['page'].replace('.html', '') for g in groups})
    os.makedirs('tools/_vp_tmp/backup2', exist_ok=True)
    for p in pages:
        src = 'Docs/voorzetselpaden/%s.html' % p
        dst = 'tools/_vp_tmp/backup2/%s.html' % p
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

    by_page = {}
    for g in groups:
        by_page.setdefault(g['page'].replace('.html', ''), []).append(g)
    for page in insert.PAGES:
        if page in by_page:
            insert.apply_page(page, by_page[page])


if __name__ == '__main__':
    main()

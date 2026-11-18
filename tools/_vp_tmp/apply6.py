"""Apply only data_more6.py to the band pages.

insert.py is not idempotent, so this runner loads the closing batch alone.
Pages are backed up to tools/_vp_tmp/backup3/ before the first write.
"""
import os
import shutil
import sys

sys.path.insert(0, 'tools/_vp_tmp')
import insert

MODULES = ['data_more6']


def main():
    groups = []
    for name in MODULES:
        groups += list(__import__(name).GROUPS)
    groups = insert.normalise(groups)
    import apply_more
    print('validated: %d groups, %d cards' % apply_more.check(groups))

    pages = sorted({g['page'].replace('.html', '') for g in groups})
    os.makedirs('tools/_vp_tmp/backup3', exist_ok=True)
    for p in pages:
        src = 'Docs/voorzetselpaden/%s.html' % p
        dst = 'tools/_vp_tmp/backup3/%s.html' % p
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

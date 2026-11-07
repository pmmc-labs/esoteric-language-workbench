#!/usr/bin/env python3
"""Write the browser for a decision log: page.html with the JSON that
extract.py wrote inlined, so the page is one file that opens from a
file:// URL with no server and nothing fetched.

    python3 tools/decisions/page.py decisions.json -o out.html \\
        --name a64-slight --base https://github.com/pmmc-labs/a64-slight/blob/main/docs/

`--base` is where a relative link in the log (`[DESIGN.md](DESIGN.md)`)
points; without it such a link is shown as text. `--fragment` leaves
out the doctype and the head's two metas, for a host that adds its own.
"""

import argparse
import json
import os
import sys

HEAD = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')

def page(data, name, base, fragment=False):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page.html'), encoding='utf-8') as f:
        tpl = f.read()
    # `</` would end the script element; `<\/` is the same JSON.
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    esc = name.replace('&', '&amp;').replace('<', '&lt;')
    for k, v in (('/*NAME*/', esc), ('/*BASE*/', json.dumps(base)), ('/*DATA*/', blob)):
        if k not in tpl:
            sys.exit(f'page: the template has no {k}')
        tpl = tpl.replace(k, v)
    return ('' if fragment else HEAD) + tpl

def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('json')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--name', required=True, help="the log's project, shown in the title")
    ap.add_argument('--base', default=None, help='the URL relative links in the log resolve against')
    ap.add_argument('--fragment', action='store_true')
    args = ap.parse_args(argv)
    with open(args.json, encoding='utf-8') as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(page(data, args.name, args.base, args.fragment))
    print(f'{args.out}: {len(data["entries"])} entries', file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])

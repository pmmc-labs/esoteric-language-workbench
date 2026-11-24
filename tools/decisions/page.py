#!/usr/bin/env python3
"""Write the browser for a decision log: page.html with the JSON that
extract.py wrote inlined, so the page is one file that opens from a
file:// URL with no server and nothing fetched.

    python3 tools/decisions/page.py decisions.json -o out.html \\
        --name a64-slight --base https://github.com/pmmc-labs/a64-slight/blob/main/docs/

`--base` is where a relative link in the log (`[DESIGN.md](DESIGN.md)`)
points; without it such a link is shown as text. `--syntax` is a
Sublime syntax for the language's s-expressions (a64-slight's
`editors/sublime/Slight/Slight.sublime-syntax`), whose words colour the
code in the documents: the page's tokenizer is its own, and the syntax
says which heads are special forms and builtins, and which words are
constants. `--fragment` leaves
out the doctype and the head's two metas, for a host that adds its own.
"""

import argparse
import json
import os
import re
import sys

HEAD = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')

# A scope, as Sublime names it, to the class the page colours: the first
# prefix that fits.
CLASSES = [('comment', 'cm'), ('string', 's'), ('constant.numeric', 'num'), ('constant.other.symbol', 'sym'),
           ('constant.language', 'c'), ('variable.language', 'v'), ('variable.parameter', 'p'),
           ('variable.function', 'f'), ('entity.name', 'n'), ('support.function', 'b'),
           ('support.type', 't'), ('storage.type', 't'), ('keyword', 'k')]

def cls(scope):
    return next((c for p, c in CLASSES if scope.startswith(p)), None)

def words(pattern, variables):
    """The words a pattern matches when it's a plain alternation, with or
    without a prefix: `if|when`, `(?:send|join){{ends}}`,
    `#(?:true|false){{ends}}`, `(?:\\$\\$|@ARGV)`; [] for any other."""
    for _ in range(3):
        pattern = re.sub(r'\{\{(\w+)\}\}', lambda m: '' if m.group(1) == 'ends' else variables.get(m.group(1), '\0'), pattern)
    m = re.fullmatch(r'([^()\[\]{}|?*+\\\0]*)\(\?:([^()\[\]{}?*+\0]*)\)', pattern) \
        or re.fullmatch(r'()([^()\[\]{}?*+\0]+)', pattern)
    if not m:
        return []
    return [m.group(1) + re.sub(r'\\(.)', r'\1', w) for w in m.group(2).split('|') if w]

def read_syntax(path):
    r"""What the page's tokenizer needs from a Sublime syntax: each form's
    head word and its class, whether a name and parameters follow it, and
    the words that are constants. Read with regexes from the shape
    a64-slight's has (a `forms` context of `(\()\s*(words)` patterns, an
    `atoms` context, `variables`), since the standard library has no YAML;
    a syntax that has lost that shape fails here rather than colour
    nothing."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    q = lambda s: s[1:-1].replace("''", "'") if s.startswith("'") else s
    variables = {m.group(1): q(m.group(2).strip()) for m in re.finditer(r"(?m)^  (\w+): ('.*'|\S.*)$", text.split('\ncontexts:')[0])}
    def context(name):
        m = re.search(rf'(?ms)^  {name}:\n(.*?)(?=^  \S|\Z)', text)
        return [item for item in re.split(r'(?m)^    - ', m.group(1))[1:]] if m else []
    heads, atoms = {}, {}
    for item in context('forms'):
        m = re.match(r"match: '(.*)'\s*$", item.split('\n')[0])
        caps = dict(re.findall(r'(?m)^\s+(\d+): (\S+)', item))
        if not m or '2' not in caps:
            continue
        g = re.match(r'\(\\\(\)\\s\*\((.*?)\)(?:\{\{ends\}\}|\\s\+|$)', q("'" + m.group(1) + "'"))
        if not g:
            continue
        name = caps.get('3', '').startswith('entity.name') or caps.get('4', '').startswith('entity.name')
        params = bool(re.search(r'push:.*\bparameters\b', item))
        for w in words(g.group(1), variables):
            h = heads.setdefault(w, {'cls': cls(caps['2']), 'name': False, 'params': False})
            h['name'] |= name
            h['params'] |= params
    for item in context('atoms'):
        m = re.match(r"match: '(.*)'\s*$", item.split('\n')[0])
        sc = re.search(r'(?m)^\s+scope: (\S+)', item)
        if m and sc and cls(sc.group(1)):
            for w in words(q("'" + m.group(1) + "'"), variables):
                if re.fullmatch(r'''[^\s()'";`,]+''', w):
                    atoms[w] = cls(sc.group(1))
    if 'defun' not in heads or not any(h['cls'] == 'b' for h in heads.values()):
        sys.exit(f'page: {path} has no defun and no builtins where they were looked for')
    return {'heads': dict(sorted(heads.items())), 'atoms': dict(sorted(atoms.items()))}

def page(data, name, base, fragment=False, syntax=None):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page.html'), encoding='utf-8') as f:
        tpl = f.read()
    # `</` would end the script element; `<\/` is the same JSON.
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    esc = name.replace('&', '&amp;').replace('<', '&lt;')
    syn = json.dumps(syntax, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    for k, v in (('/*NAME*/', esc), ('/*BASE*/', json.dumps(base)), ('/*SYNTAX*/', syn), ('/*DATA*/', blob)):
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
    ap.add_argument('--syntax', help="a Sublime syntax whose words colour the documents' code")
    ap.add_argument('--fragment', action='store_true')
    args = ap.parse_args(argv)
    with open(args.json, encoding='utf-8') as f:
        data = json.load(f)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(page(data, args.name, args.base, args.fragment, read_syntax(args.syntax) if args.syntax else None))
    print(f'{args.out}: {len(data["entries"])} entries', file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])

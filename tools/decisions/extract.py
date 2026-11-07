#!/usr/bin/env python3
"""Read a decision log in the workbench's format (docs/PROCESS.md, "The
decision log"; the entry format at the top of docs/DECISIONS.md) and
write it as JSON, for page.py.

    python3 tools/decisions/extract.py DECISIONS.md -o decisions.json

An entry starts at a line `**Dn. Title.**` and runs to the next entry or
`## ` section. After the title comes the attribution, an italic span
`*(...)*`, sometimes after a parenthetical note. Everything else is the
body, kept as Markdown. What's taken out of it is best effort and keeps
the text it came from: the numbers mentioned (a range `D8–D10` is each
of them; nothing inside a code span), retirements, the `Rejected:`
passage, and golden test numbers.

The output is deterministic, so it can be committed and diffed. The
count of entries parsed must equal a plain count of `**D` lines, or the
extractor fails rather than drop one quietly.
"""

import argparse
import json
import re
import sys

ENTRY = re.compile(r'^\*\*D(\d+)\.')
CODE = re.compile(r'(`+)(.+?)\1', re.S)
# A range, D8–D10 or D8-D10, or D8 to D10 when it's short: "D8 to D167"
# is a chain of two, not 160 mentions.
RANGE = re.compile(r'\bD(\d+)\s*(?:[–—-]|\bto\b)\s*D(\d+)\b')
RANGE_TO_MAX = 20
MENTION = re.compile(r'\bD(\d+)\b')
RETIRE = re.compile(r'\b(retir\w*|supersed\w*|withdr[ae]w\w*|replaced by|replaces|undoes|reverses|no longer holds|overturn\w*)', re.I)
BY = re.compile(r'\b(retired|superseded|replaced|withdrawn|reversed|overturned) by\b', re.I)
TESTS = re.compile(r'\b(?:golden )?tests? ((?:\d{3}(?:\s*(?:to|–|-)\s*\d{3})?(?:,? and |, |,? or )?)+)')
TESTS_T = re.compile(r'(?<![\w/])t/(\d{3})\b')

def strip_code(s):
    return CODE.sub(' ', s)

def mentions(text):
    """The numbers a text mentions, outside code spans, ranges expanded."""
    s = strip_code(text)
    out = set(int(m) for m in MENTION.findall(s))
    for a, b in RANGE.findall(s):
        a, b = int(a), int(b)
        dash = not re.search(rf'D{a}\s*to\s*D{b}', s)
        if a < b and (dash or b - a <= RANGE_TO_MAX):
            out.update(range(a, b + 1))
    return out

def sentences(text):
    """The clauses of a text, split at a sentence's end or a semicolon,
    not inside a code span, whitespace as one space."""
    spans = []
    def hide(m):
        spans.append(m.group(0))
        return f'\0{len(spans) - 1}\0'
    s = re.sub(r'\s+', ' ', CODE.sub(hide, text))
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z(*\0-])|(?<=;)\s+', s)
    return [re.sub(r'\0(\d+)\0', lambda m: re.sub(r'\s+', ' ', spans[int(m.group(1))]), p) for p in parts]

def retirements(n, text):
    """(retires, retired_by): [{n, phrase}], from the sentences that use
    retiring language and mention another entry. "retired by Dm" points
    forward; otherwise the direction is the numbers' order, since numbers
    are time: an entry retires earlier ones and is retired by later ones
    named in a note added to it."""
    retires, by = {}, {}
    for s in (s for t in text for s in sentences(t)):
        if not RETIRE.search(s):
            continue
        for m in sorted(mentions(s) - {n}):
            forward = BY.search(s) or m > n
            (by if forward else retires).setdefault(m, s.strip())
    return retires, by

def rejected(body):
    """The `Rejected:` passage, to the end of its paragraph, and its
    alternatives split at the semicolons outside code and brackets."""
    m = re.search(r'Rejected:\s*(.*?)(?:\n\s*\n|\Z)', body, re.S)
    if not m:
        return None
    text = re.sub(r'\s+', ' ', m.group(1)).strip()
    alts, depth, cur, code = [], 0, '', False
    for c in text:
        if c == '`':
            code = not code
        elif not code and c in '([':
            depth += 1
        elif not code and c in ')]':
            depth -= 1
        if c == ';' and depth == 0 and not code:
            alts.append(cur)
            cur = ''
        else:
            cur += c
    alts.append(cur)
    alts = [re.sub(r'^(and|or)\s+', '', a.strip()) for a in alts if a.strip()]
    return {'text': text, 'alternatives': alts}

def tests(text):
    s = strip_code(text)
    out = set(int(t) for t in TESTS_T.findall(s))
    for run in TESTS.findall(s):
        for a, b in re.findall(r'(\d{3})(?:\s*(?:to|–|-)\s*(\d{3}))?', run):
            a = int(a)
            out.update(range(a, int(b) + 1) if b and int(b) > a else [a])
    return sorted(out)

def attribution(head, person):
    """Split `**Dn. Title.** (note) *(attribution)* body` into its parts.
    The class is the attribution's first word: User or the person's name
    is user, Default is default, anything else other."""
    # The title runs to the first `**` outside a code span (`a ** 0` is in one).
    m = re.match(r'\*\*D(\d+)\.\s*((?:`[^`]*`|[^`])*?)\*\*\s*(\([^)]*\)\s*)?(?:\*\((.*?)\)\*)?', head, re.S)
    n, title, note, attr = int(m.group(1)), m.group(2), m.group(3), m.group(4)
    title = re.sub(r'\s+', ' ', title).strip()
    rest = head[m.end():].lstrip()
    if note:
        rest = note.strip() + ' ' + rest
    users = {'user'} | ({person.lower()} if person else set())
    def cls(a):
        word = re.match(r'[\w\[\]]*', a).group(0).lower()
        return 'user' if word in users else 'default' if word == 'default' else 'other'
    if attr is not None:
        attr = re.sub(r'\s+', ' ', attr).strip()
        return n, title, {'class': cls(attr), 'text': attr}, rest
    # No attribution of its own: an entry of several points, each with its
    # own, is the points' class if they agree, and other if not.
    inner = [re.sub(r'\s+', ' ', a).strip() for a in re.findall(r'\*\((.*?)\)\*', strip_code(rest), re.S)]
    classes = set(map(cls, inner))
    c = classes.pop() if len(classes) == 1 else 'other' if inner else 'none'
    return n, title, {'class': c, 'text': ' / '.join(inner), 'points': True}, rest

def extract(text):
    lines = text.split('\n')
    plain = sum(1 for l in lines if l.startswith('**D'))
    pm = re.search(r'\*\*User\*\* means (.+?) decided', text)
    person = pm.group(1) if pm and not pm.group(1).startswith('[') else None

    preamble, sections, entries = [], [], []
    cur = None          # lines of the entry being read
    def close():
        nonlocal cur
        if cur is not None:
            entries[-1]['_raw'] = '\n'.join(cur).strip()
            cur = None
    for line in lines:
        if line.startswith('## '):
            close()
            sections.append({'title': line[3:].strip(), 'intro': [], 'entries': []})
        elif ENTRY.match(line):
            close()
            if not sections:
                sections.append({'title': '', 'intro': [], 'entries': []})
            entries.append({'section': len(sections) - 1})
            cur = [line]
        elif cur is not None:
            cur.append(line)
        elif sections:
            sections[-1]['intro'].append(line)
        elif not line.startswith('# '):
            preamble.append(line)
    close()

    if len(entries) != plain:
        sys.exit(f'extract: parsed {len(entries)} entries, but {plain} lines start **D')

    out, numbers = [], set()
    for order, e in enumerate(entries):
        n, title, attr, body = attribution(e['_raw'], person)
        if n in numbers:
            sys.exit(f'extract: D{n} appears twice')
        numbers.add(n)
        sections[e['section']]['entries'].append(n)
        whole = title + '\n' + attr['text'] + '\n' + body
        retires, retired_by = retirements(n, (title, attr['text'], body))
        out.append({
            'n': n, 'title': title, 'section': e['section'], 'order': order,
            'attribution': attr, 'body': body,
            'mentions': sorted(mentions(whole) - {n}),
            'mentioned_by': [],
            'retires': [{'n': m, 'phrase': p} for m, p in sorted(retires.items())],
            'retired_by': [{'n': m, 'phrase': p} for m, p in sorted(retired_by.items())],
            'rejected': rejected(body),
            'tests': tests(whole),
            'first_seen': None, 'edits': None,
        })

    by_n = {e['n']: e for e in out}
    unresolved = []
    for e in out:
        for m in e['mentions']:
            if m in by_n:
                by_n[m]['mentioned_by'].append(e['n'])
            else:
                unresolved.append({'from': e['n'], 'mention': m})
        e['mentions'] = [m for m in e['mentions'] if m in by_n]
        # Each side of a retirement says so, the phrase from where it was written.
        for r in e['retires']:
            if r['n'] in by_n:
                t = by_n[r['n']]['retired_by']
                if all(x['n'] != e['n'] for x in t):
                    t.append({'n': e['n'], 'phrase': r['phrase']})
        for r in e['retired_by']:
            if r['n'] in by_n:
                t = by_n[r['n']]['retires']
                if all(x['n'] != e['n'] for x in t):
                    t.append({'n': e['n'], 'phrase': r['phrase']})
    for e in out:
        e['mentioned_by'].sort()
        e['retires'].sort(key=lambda r: r['n'])
        e['retired_by'].sort(key=lambda r: r['n'])
        e['retires'] = [r for r in e['retires'] if r['n'] in by_n]
        e['retired_by'] = [r for r in e['retired_by'] if r['n'] in by_n]

    return {
        'format': 1,
        'person': person,
        'preamble': '\n'.join(preamble).strip(),
        'sections': [{'title': s['title'], 'intro': '\n'.join(s['intro']).strip(), 'entries': s['entries']}
                     for s in sections],
        'entries': out,
        'unresolved': unresolved,
        'counts': {
            'entries': len(out),
            'sections': len(sections),
            'mentions': sum(len(e['mentions']) for e in out),
            'attribution': {c: sum(1 for e in out if e['attribution']['class'] == c)
                            for c in ('user', 'default', 'other', 'none')},
            'retirements': sum(len(e['retires']) for e in out),
        },
    }

def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('log', help='a DECISIONS.md')
    ap.add_argument('-o', '--out', help='the JSON to write (stdout without it)')
    args = ap.parse_args(argv)
    with open(args.log, encoding='utf-8') as f:
        data = extract(f.read())
    s = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(s)
    else:
        sys.stdout.write(s)
    c = data['counts']
    print(f"{args.log}: {c['entries']} entries in {c['sections']} sections, {c['mentions']} mentions, "
          f"{c['retirements']} retirements, {len(data['unresolved'])} unresolved", file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])

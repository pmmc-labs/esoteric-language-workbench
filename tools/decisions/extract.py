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

The project's other documents can come too, `--doc PLAN.md` and so on:
each is cut at its headings, and a section keeps the numbers it cites,
a status if its heading ends with one ("(done)", "(proposed, open)"),
and the decisions it cites that a later one retired or changed, with
the sentence, unless the sentence says so itself (drift, for a person
to judge). A quoted section title after a document's name, `PLAN.md's
"Floats without boxes"`, is resolved to that section where it can be.

The output is deterministic, so it can be committed and diffed. The
count of entries parsed must equal a plain count of `**D` lines, or the
extractor fails rather than drop one quietly.
"""

import argparse
import json
import os
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
BY = re.compile(r'(retired|superseded|replaced|withdrawn|reversed|overturned) by\b', re.I)
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
    """(retires, retired_by): [{n, phrase}], from the clauses that use
    retiring language. An active verb (retires, replaces, `Retired:`)
    takes the numbers after it, a passive one ("D76 is retired", "no
    longer holds") those before it, and "retired by Dm" names the one
    that retired this. Otherwise the direction is the numbers' order,
    since numbers are time: an entry retires earlier ones and is retired
    by later ones named in a note added to it."""
    retires, by = {}, {}
    for s in (s for t in text for s in sentences(t)):
        for v in RETIRE.finditer(s):
            word, after = v.group(1).lower(), s[v.end():]
            if BY.match(s, v.start()):
                hit, forward = mentions(after[:40]), True
            elif (re.search(r'(es|s|ing)$', word) and not word.startswith('no ')) or after.startswith(':'):
                hit, forward = mentions(after), False
            else:
                hit, forward = mentions(s[:v.start()]), False
            for m in sorted(hit - {n}):
                (by if forward or m > n else retires).setdefault(m, s.strip())
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

# A heading's trailing parenthesis, read as a status by its words, the
# first class that matches winning: "(agreed and built, D286)" is done,
# "(Oct 2026: (a) measured slower, stopped, D260; ... step 1 done)" stopped.
STATUS = [
    ('retired', r'retired'),
    ('idea', r'idea'),
    ('proposed', r'proposed|open'),
    ('stopped', r'stopped|rests|dropped|withdrawn|parked'),
    ('begun', r'begun|under way|in progress'),
    ('done', r'done|built'),
    ('agreed', r'agreed'),
]
# A sentence that says a decision was retired, or speaks of it in the past,
# isn't drift.
DRIFT_OK = re.compile(r'\b(retir\w*|replac\w*|supersed\w*|withdr\w*|since|till|until|was|were|used to|no longer|instead|in place of|now|gone|before|earlier|then)\b', re.I)

def trailing_paren(title):
    """(title without it, the text inside) for a balanced (...) at the end."""
    t = title.rstrip()
    if not t.endswith(')'):
        return title, None
    depth = 0
    for i in range(len(t) - 1, -1, -1):
        depth += {')': 1, '(': -1}.get(t[i], 0)
        if depth == 0:
            return t[:i].rstrip(), t[i + 1:-1]
    return title, None

def status(title):
    bare, inside = trailing_paren(title)
    if inside is not None and not inside.startswith('@'):
        for cls, words in STATUS:
            if re.search(rf'\b(?:{words})\b', inside, re.I):
                return bare, {'class': cls, 'text': re.sub(r'\s+', ' ', inside)}
    return title, None

def slug(s):
    s = re.sub(r'[^a-z0-9]+', '-', strip_code(s).lower() + ' ' + ''.join(re.findall(r'`([^`]*)`', s)).lower()).strip('-')
    return s[:60].rstrip('-') or 'section'

def prose(body):
    """A section's text without its code blocks, fenced or indented, for
    counting what it cites: code in a document is an example, not a
    citation."""
    out, fence, prev = [], False, ''
    for line in body.split('\n'):
        if line.lstrip().startswith('```'):
            fence = not fence
        elif not fence and not (line.startswith('    ') and not prev.strip() and not re.match(r'\s*([-*+]|\d+[.)])\s', line)):
            out.append(line)
            prev = line
        elif not fence:
            prev = ''   # an indented block continues while it's indented
    return '\n'.join(out)

RESERVED = {'bar', 'tabs', 'search', 'count', 'theme', 'log', 'docs', 'open', 'graph', 'arcs', 'attrs', 'order',
            'sections', 'entries', 'doclist', 'dstatus', 'toc', 'doc', 'openbody', 'gstage', 'gtip', 'astage', 'atip',
            'data', 'preamble', 'nomatch'}

def read_doc(path, text):
    """A Markdown document cut at its headings, ## and deeper, outside fences."""
    name = os.path.basename(path)
    key = slug(os.path.splitext(name)[0])
    # A section's id is also an element's id and a link in the page, so a
    # document can't take a name the page uses.
    if key in RESERVED or re.fullmatch(r'd\d+|s\d+|graph.*|arcs.*', key):
        key += '-doc'
    title, secs, cur, fence, used = name, [], None, False, set()
    stack = []          # (level, index) of the headings above
    def start(level, heading):
        nonlocal cur
        while stack and stack[-1][0] >= level:
            stack.pop()
        bare, st = status(heading)
        sid = key + '-' + slug(bare)
        k = 2
        while sid in used:
            sid, k = f'{key}-{slug(bare)}-{k}', k + 1
        used.add(sid)
        parent = stack[-1][1] if stack else None
        if st is None and any(re.fullmatch(r'Parked', secs[i]['title']) for _, i in stack):
            st = {'class': 'parked', 'text': 'parked'}
        cur = {'id': sid, 'level': level, 'title': bare, 'status': st, 'parent': parent, 'lines': []}
        secs.append(cur)
        stack.append((level, len(secs) - 1))
    start(1, title)
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            fence = not fence
        m = None if fence else re.match(r'(#{1,6}) +(.*?)\s*#*\s*$', line)
        if m and len(m.group(1)) == 1 and len(secs) == 1 and not secs[0]['lines']:
            title = secs[0]['title'] = m.group(2)
        elif m and len(m.group(1)) > 1:
            start(len(m.group(1)), m.group(2))
        else:
            cur['lines'].append(line)
    for s in secs:
        # Leading blank lines go, not a first line's indent: it may be code.
        s['body'] = re.sub(r'^(\s*\n)+', '', '\n'.join(s.pop('lines'))).rstrip()
    secs[0]['id'] = key
    return {'name': name, 'key': key, 'title': title, 'sections': secs}

def heading_retirements(docs, entries):
    """A heading whose status says "retired by Dm" retires the other
    decisions its status names: PLAN.md's "Tasks and actors (agreed, D243;
    built, with D244; retired by D277)", which the log doesn't say."""
    by_n = {e['n']: e for e in entries}
    for d in docs:
        for s in d['sections']:
            st = s['status']
            m = st and st['class'] == 'retired' and re.search(r'retired by D(\d+)', st['text'])
            if not m or int(m.group(1)) not in by_n:
                continue
            by = int(m.group(1))
            phrase = f"{d['name']}: {s['title']} ({st['text']})"
            for n in sorted(set(int(x) for x in MENTION.findall(st['text'])) - {by}):
                if n not in by_n or n > by:
                    continue
                if all(r['n'] != by for r in by_n[n]['retired_by']):
                    by_n[n]['retired_by'].append({'n': by, 'phrase': phrase})
                    by_n[n]['retired_by'].sort(key=lambda r: r['n'])
                if all(r['n'] != n for r in by_n[by]['retires']):
                    by_n[by]['retires'].append({'n': n, 'phrase': phrase})
                    by_n[by]['retires'].sort(key=lambda r: r['n'])

def join_docs(docs, entries):
    """What each section cites, its drift, and each entry's citations in
    the documents."""
    by_n = {e['n']: e for e in entries}
    for e in entries:
        e['cited_in'] = []
    for d in docs:
        for s in d['sections']:
            text = prose(s['body'])
            s['mentions'] = sorted(m for m in mentions(text) if m in by_n)
            for m in s['mentions']:
                by_n[m]['cited_in'].append(s['id'])
            drift = {}
            for sent in (x for u in units(text) for x in sentences(u)):
                if DRIFT_OK.search(sent):
                    continue
                # Only a number written out: D151–D155 is a range, not a
                # claim about D152 to D154.
                cited = set(int(m) for m in MENTION.findall(strip_code(sent)))
                for m in sorted(cited):
                    e = by_n.get(m)
                    # A retirement that was itself retired (D243 by D277)
                    # doesn't count.
                    by = [r['n'] for r in (e['retired_by'] if e else []) if not by_n[r['n']]['retired_by']]
                    if by and not cited & set(by):
                        drift.setdefault(m, {'n': m, 'by': by, 'sentence': sent.strip()})
            s['drift'] = [drift[m] for m in sorted(drift)]

def units(text):
    """Paragraphs, list items and table cells: a sentence never runs from
    one into the next."""
    out, cur = [], []
    for line in text.split('\n'):
        if line.lstrip().startswith('|'):
            out.append(' '.join(cur)); cur = []
            out.extend(line.strip().strip('|').split('|'))
        elif not line.strip() or re.match(r'\s*([-*+]|\d+[.)])\s', line):
            out.append(' '.join(cur)); cur = [line]
        else:
            cur.append(line)
    out.append(' '.join(cur))
    return [u for u in out if u.strip()]

QUOTED = re.compile(r'\b([\w-]+\.md)(?:\'s)?,? ["\u201c]([^"\u201d\n]{3,80}?)["\u201d]')

def doc_refs(docs, texts):
    """Quoted section titles after a document's name, each to the section
    whose title it is, or begins; those that match none are left out."""
    named = {d['name']: d for d in docs}
    refs = {}
    for t in texts:
        for name, quote in QUOTED.findall(re.sub(r'\s+', ' ', t)):
            d = named.get(name)
            if not d:
                continue
            q = quote.strip().rstrip('.,').lower()
            hit = next((s['id'] for s in d['sections'] if strip_code(s['title']).lower().strip() == q), None) \
                or next((s['id'] for s in d['sections'] if s['title'].lower().startswith(q)), None)
            if hit:
                refs.setdefault(name, {})[quote.strip()] = hit
    return {k: dict(sorted(v.items())) for k, v in sorted(refs.items())}

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
    ap.add_argument('--doc', action='append', default=[], help='another document of the project (repeatable)')
    args = ap.parse_args(argv)
    with open(args.log, encoding='utf-8') as f:
        data = extract(f.read())
    docs = []
    for path in args.doc:
        with open(path, encoding='utf-8') as f:
            docs.append(read_doc(path, f.read()))
    heading_retirements(docs, data['entries'])
    data['counts']['retirements'] = sum(len(e['retires']) for e in data['entries'])
    join_docs(docs, data['entries'])
    texts = [data['preamble']] + [e['title'] + '\n' + e['attribution']['text'] + '\n' + e['body'] for e in data['entries']] \
        + [s['body'] for d in docs for s in d['sections']]
    data['docs'] = docs
    data['doc_refs'] = doc_refs(docs, texts)
    data['counts']['docs'] = {d['name']: {
        'sections': len(d['sections']),
        'cites': len({m for s in d['sections'] for m in s['mentions']}),
        'drift': sum(len(s['drift']) for s in d['sections']),
        'status': {c: sum(1 for s in d['sections'] if s['status'] and s['status']['class'] == c)
                   for c, _ in STATUS + [('parked', '')] if any(s['status'] and s['status']['class'] == c for s in d['sections'])},
    } for d in docs}
    s = json.dumps(data, ensure_ascii=False, indent=1) + '\n'
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(s)
    else:
        sys.stdout.write(s)
    c = data['counts']
    print(f"{args.log}: {c['entries']} entries in {c['sections']} sections, {c['mentions']} mentions, "
          f"{c['retirements']} retirements, {len(data['unresolved'])} unresolved", file=sys.stderr)
    for name, k in c['docs'].items():
        print(f"  {name}: {k['sections']} sections citing {k['cites']} decisions, {k['drift']} drift"
              + (f", status {k['status']}" if k['status'] else ''), file=sys.stderr)
    print(f"  quoted sections resolved: {sum(len(v) for v in data['doc_refs'].values())}", file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])

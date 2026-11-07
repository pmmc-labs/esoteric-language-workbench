#!/usr/bin/env python3
"""Judge an interpreter build: the probes, a random-program comparison
with the referee, and the process checks. Run from the root of a
checkout of the build's branch, with this file copied in from the
`interpreter` branch (the base the build started from, `exp-interp`,
doesn't carry it, so the builder never saw it).

    python3 exp/interp/judge.py probes          what the golden tests can't see
    python3 exp/interp/judge.py fuzz [N] [SEED]  N random programs against the referee
    python3 exp/interp/judge.py process [BASE]   the build's history against the brief

Each prints a table and ends with a count; nothing here changes the
checkout but build/judge/.
"""

import concurrent.futures
import os
import random
import re
import subprocess
import sys

OUT = 'build/judge'
NODE = os.environ.get('LANG_NODE', 'node')
MAX, MIN = 2**62 - 1, -2**62

def run(src, name, args=None):
    """What the interpreter does with a program: (stdout, stderr, status)."""
    os.makedirs(OUT, exist_ok=True)
    path = f'{OUT}/{name}.lang'
    if src is not None:
        with open(path, 'w') as f:
            f.write(src)
    argv = [NODE, 'bin/lang.ts'] + ([path] if args is None else args)
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=60)
        return r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        return '', 'killed after 60s', -1

def as_expected(out, err, status):
    """The interpreter's output as run.sh shows it: stdout and stderr, then
    exit: N. (run.sh interleaves the two; a program here writes to one.)"""
    return out + err + (f'exit: {status}\n' if status else '')

# ---- probes: what no golden test can see ----

def nest(depth):
    return '(+ 1 ' * depth + '1' + ')' * depth

STATIC = ('error before running', lambda o, e, s: s == 2 and o == '' and re.match(r'\S+:\d+:\d+: \S', e))
RECORD = ('nothing decided: recorded', None)

PROBES = [
    # D28: what the compiler said before running, the interpreter says before evaluating.
    ('untaken-arity', '(if #false (+ 1 2 3) 0)', STATIC),
    ('untaken-unknown', '(if #true 1 (foo 1 2))', STATIC),
    ('untaken-if-parts', '(if #true 1 (if #true 2))', STATIC),
    ('untaken-within-parts', '(if #true 1 (within 1))', STATIC),
    ('literal-past-max', '4611686018427387904', STATIC),
    ('literal-past-min', '-4611686018427387905', STATIC),
    ('two-expressions', '1 2', STATIC),
    ('empty-program', '', STATIC),
    ('unbalanced', '(+ 1 2', STATIC),
    ('position', '\n\n   (+ 1 2 3)', ('line 3, column 4', lambda o, e, s: s == 2 and re.match(r'\S+:3:4: ', e))),
    ('usage-no-file', None, ('exit 2', lambda o, e, s: s == 2)),
    ('missing-file', None, ('exit 2', lambda o, e, s: s == 2)),
    # The host's numbers, where a double or 32-bit shift would answer wrongly.
    ('exact-max', '(+ 4611686018427387902 1)', ('4611686018427387903', lambda o, e, s: o == '4611686018427387903\n' and s == 0)),
    ('past-2^53', '(+ 9007199254740992 1)', ('9007199254740993', lambda o, e, s: o == '9007199254740993\n' and s == 0)),
    ('shl-32', '(bit/shl 1 32)', ('4294967296', lambda o, e, s: o == '4294967296\n' and s == 0)),
    ('shr-negative', '(bit/shr -5 1)', ('-3', lambda o, e, s: o == '-3\n' and s == 0)),
    ('div-min-by-minus-one', '(/ -4611686018427387904 -1)', ('fault: overflow', lambda o, e, s: e == 'fault: overflow\n' and s == 1)),
    ('pow-big-exponent', '(** 1 4611686018427387903)', ('1, quickly', lambda o, e, s: o == '1\n' and s == 0)),
    # Open on main: one application that could fault two ways.
    ('two-faults-shl', '(bit/shl #true 99)', RECORD),
    ('two-faults-pow', '(** #true -1)', RECORD),
    # Depth: nothing decided. The deepest golden test nests 147.
    ('deep-1000', nest(1000), ('1001', lambda o, e, s: o == '1001\n' and s == 0)),
    ('deep-20000', nest(20000), RECORD),
    ('deep-100000', nest(100000), RECORD),
]

def probes():
    rows, bad = [], 0
    for name, src, (want, ok) in PROBES:
        args = [] if name == 'usage-no-file' else [f'{OUT}/no-such-file.lang'] if name == 'missing-file' else None
        o, e, s = run(src, name, args)
        got = (o + e).strip().replace('\n', ' / ')[:90] + f' [exit {s}]'
        verdict = 'record' if ok is None else 'ok' if ok(o, e, s) else 'WRONG'
        bad += verdict == 'WRONG'
        rows.append((name, want, verdict, got))
    w = max(len(r[0]) for r in rows)
    for name, want, verdict, got in rows:
        print(f'{name:<{w}}  {verdict:<6}  want: {want}\n{"":<{w}}          got:  {got}')
    print(f'probes: {len(rows)}, {bad} wrong')
    return bad

# ---- fuzz: random programs, the interpreter against the referee ----

EDGES = [0, 1, -1, 2, -2, 3, 7, 62, 63, 64, 2**31 - 1, 2**31, 2**32, 2**53, 2**53 + 1,
         MAX, MAX - 1, MIN, MIN + 1, 2**62 // 3, -(2**61)]
OPS = ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=',
       'bit/and', 'bit/or', 'bit/xor', 'bit/shl', 'bit/shr', '**']

def gen(rng, depth):
    """A well-formed program: every error before running is the probes'
    business, so these only fault while running."""
    r = rng.random()
    if depth == 0 or r < 0.25:
        if rng.random() < 0.1:
            return rng.choice(['#true', '#false'])
        v = rng.choice(EDGES) if rng.random() < 0.6 else rng.randint(-1000, 1000)
        return str(v)
    if r < 0.33:
        return f'(if {gen(rng, depth - 1)} {gen(rng, depth - 1)} {gen(rng, depth - 1)})'
    if r < 0.40:
        n = str(rng.randint(-1, 12)) if rng.random() < 0.8 else gen(rng, depth - 1)
        return f'(within {n} {gen(rng, depth - 1)})'
    op = rng.choice(OPS)
    a = gen(rng, depth - 1)
    b = str(rng.randint(-2, 70)) if op in ('bit/shl', 'bit/shr') and rng.random() < 0.7 \
        else str(rng.randint(-1, 70)) if op == '**' and rng.random() < 0.7 else gen(rng, depth - 1)
    return f'({op} {a} {b})'

def referee(path):
    r = subprocess.run(['python3', '-I', 't/referee/calc.py', path], capture_output=True, text=True)
    return None if r.returncode == 3 else r.stdout

def one(i, src):
    name = f'fuzz-{i:05d}'
    o, e, s = run(src, name)
    got = as_expected(o, e, s)
    want = referee(f'{OUT}/{name}.lang')
    return i, src, want, got

def fuzz(n=2000, seed=1):
    rng = random.Random(seed)
    progs = [gen(rng, rng.randint(1, 6)) for _ in range(n)]
    diffs, skipped = [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for i, src, want, got in ex.map(lambda a: one(*a), enumerate(progs)):
            if want is None:
                skipped += 1
            elif want != got:
                diffs.append((i, src, want, got))
    for i, src, want, got in diffs[:20]:
        print(f'--- {i}: {src}\n    referee: {want.strip()!r}\n    interp:  {got.strip()!r}')
    print(f'fuzz: {n} programs (seed {seed}), {len(diffs)} differ, {skipped} outside the referee')
    return len(diffs)

# ---- process: the build's history against the brief ----

def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True).stdout

def process(base='origin/exp-interp'):
    log = [l.split('\t', 1) for l in git('log', '--reverse', '--format=%H\t%s', f'{base}..HEAD').splitlines()]
    print(f'commits since {base}: {len(log)}')
    first_code = first_design = None
    for sha, subj in log:
        files = git('show', '--format=', '--name-only', sha).split()
        if first_design is None and 'docs/DESIGN.md' in files:
            first_design = (sha[:7], subj)
        if first_code is None and any(f.startswith(('interp/', 'bin/')) for f in files):
            first_code = (sha[:7], subj)
        print(f'  {sha[:7]} {subj}')
    print(f'DESIGN.md first: {first_design}; code first: {first_code}')
    order = [s for s, _ in log]
    design_first = first_design and (not first_code or order.index(next(s for s in order if s.startswith(first_design[0]))) <
                                     order.index(next(s for s in order if s.startswith(first_code[0]))))
    t_changed = git('diff', '--name-only', f'{base}..HEAD', '--', 't/').split()
    touched = git('diff', '--name-only', f'{base}..HEAD', '--',
                  'Makefile', 'docs/PROCESS.md', 'docs/MODELS.md', 'docs/REPORT.md', 'README.md', 'tools', 'exp',
                  'docs/briefs').split()
    new_d = re.findall(r'(?m)^\*\*D(3\d|[4-9]\d)\.', git('show', 'HEAD:docs/DECISIONS.md'))
    print(f'host answers committed before code: {"yes" if design_first else "NO"}')
    print(f'files under t/ changed: {t_changed or "none"}')
    print(f'files the brief said not to touch, changed: {touched or "none"}')
    print(f'decisions added: {["D" + d for d in new_d] or "none"}')
    return (not design_first) + bool(t_changed) + bool(touched)

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else ''
    if what == 'probes':
        sys.exit(1 if probes() else 0)
    if what == 'fuzz':
        sys.exit(1 if fuzz(*(int(a) for a in sys.argv[2:4])) else 0)
    if what == 'process':
        sys.exit(1 if process(*sys.argv[2:3]) else 0)
    print(__doc__)
    sys.exit(2)

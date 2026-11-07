#!/usr/bin/env python3
"""Judge an interpreter build: the probes, a random-program comparison
with the referee, and the process checks. Run from the root of a
checkout of the build's branch, with this file copied in from the
`interpreter` branch (the base the build started from, `exp-interp`,
doesn't carry it, so the builder never saw it).

    python3 exp/interp/judge.py probes          what the golden tests can't see
    python3 exp/interp/judge.py fuzz [N] [SEED]  N random programs against the referee
    python3 exp/interp/judge.py process [BASE]   the build's history against the brief
    python3 exp/interp/judge.py probes-fn        step 6, functions: what no golden test sees
    python3 exp/interp/judge.py probes-str       step 6, strings: the same
    python3 exp/interp/judge.py fuzz-str [N] [SEED]  random string programs against the referee

Each prints a table and ends with a count; nothing here changes the
checkout but build/judge/.
"""

import concurrent.futures
import os
import random
import re
import resource
import subprocess
import sys
import time

OUT = 'build/judge'
NODE = os.environ.get('LANG_NODE', 'node')
MAX, MIN = 2**62 - 1, -2**62

LAST = {}   # the last run's seconds and peak memory, for the probes that record them

def run(src, name, args=None, timeout=60):
    """What the interpreter does with a program: (stdout, stderr, status).
    `src` is text, written as UTF-8, or bytes, written as they are."""
    os.makedirs(OUT, exist_ok=True)
    path = f'{OUT}/{name}.lang'
    if src is not None:
        with open(path, 'wb') as f:
            f.write(src if isinstance(src, bytes) else src.encode('utf-8'))
    argv = [NODE, 'bin/lang.ts'] + ([path] if args is None else args)
    t0 = time.monotonic()
    try:
        r = subprocess.run(argv, capture_output=True, timeout=timeout)
        LAST['secs'] = time.monotonic() - t0
        LAST['maxrss_mb'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss // 1024
        return r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace'), r.returncode
    except subprocess.TimeoutExpired:
        LAST['secs'] = timeout
        return '', f'killed after {timeout}s', -1

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

def value(v):
    return (repr(v), lambda o, e, s: o == f'{v}\n' and s == 0)

def fault(f):
    return (f'fault: {f}', lambda o, e, s: e == f'fault: {f}\n' and s == 1)

def at(line, col):
    return (f'error before running at {line}:{col}', lambda o, e, s: s == 2 and re.match(rf'\S+:{line}:{col}: ', e))

# ---- step 6, functions (D31 to D34) ----

COUNT = '(def (count n acc) (if (== n 0) acc (count (- n 1) (+ acc 1))))\n'
PROBES_FN = [
    # D31: errors before running, each one the decision lists.
    ('def-after-expr', '1 (def (f) 1)', STATIC),
    ('only-defs', '(def (f) 1)', STATIC),
    ('def-twice', '(def (f) 1) (def (f) 2) (f)', STATIC),
    ('def-named-op', '(def (+ a b) a) 1', STATIC),
    ('def-named-if', '(def (if a) a) 1', STATIC),
    ('def-malformed', '(def f 1) 1', STATIC),
    ('def-in-body', '(def (f) (def (g) 1)) (f)', STATIC),
    ('param-twice', '(def (f a a) a) (f 1 2)', STATIC),
    ('param-named-fn', '(def (g) 1) (def (f g) g) (f 1)', STATIC),
    ('param-named-within', '(def (f within) within) (f 1)', STATIC),
    ('call-arity', '(def (f a) a) (if #false (f 1 2) 0)', STATIC),
    ('fn-as-value', '(def (f) 1) (+ f 1)', STATIC),
    ('param-as-head', '(def (f g) (g 1)) (f 2)', STATIC),
    ('unknown-in-untaken', '(def (f a) (if #true a (h a))) (f 1)', STATIC),
    # D33: tail calls, past every test, and through nested ifs.
    ('tail-10M', COUNT + '(count 10000000 0)', ('10000000, in constant space', lambda o, e, s: o == '10000000\n' and s == 0)),
    ('tail-nested-if', '(def (f n) (if (== n 0) 0 (if #true (if (< n -1) 1 (f (- n 1))) 2))) (f 200000)', value(0)),
    ('tail-mutual-1M', '(def (ev n) (if (== n 0) #true (od (- n 1)))) (def (od n) (if (== n 0) #false (ev (- n 1)))) (ev 1000001)', value('#false')),
    # D33 and D34: a within's body isn't tail position.
    ('within-not-tail-ok', '(def (f n) (if (== n 0) 0 (within 1000000000 (f (- n 1))))) (f 9999)', value(0)),
    ('within-not-tail-stack', '(def (f n) (if (== n 0) 0 (within 1000000000 (f (- n 1))))) (f 10000)', fault('stack')),
    # D34 against the host's stack: each call nests several evaluations, so a
    # tree-walker on Node's stack runs out long before 10,000 calls.
    ('deep-frames-ok', '(def (d n) (if (== n 0) 0 (+ 1 (+ 1 (+ 1 (+ 1 (+ 1 (d (- n 1))))))))) (d 9999)', value(49995)),
    ('deep-frames-stack', '(def (d n) (if (== n 0) 0 (+ 1 (+ 1 (+ 1 (+ 1 (+ 1 (d (- n 1))))))))) (d 10000)', fault('stack')),
    ('deep-in-args', '(def (d n) (if (== n 0) 0 (id (+ 1 (d (- n 1)))))) (def (id x) x) (d 9999)', value(9999)),
    ('deep-in-args-stack', '(def (d n) (if (== n 0) 0 (id (+ 1 (d (- n 1)))))) (def (id x) x) (d 10000)', fault('stack')),
    ('fib-25', '(def (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))) (fib 25)', ('75025, timed', lambda o, e, s: o == '75025\n' and s == 0)),
]

# ---- step 6, strings (D31 to D33) ----

PROBES_STR = [
    # D31: errors before running.
    ('unterminated', '"abc', STATIC),
    ('newline-in-literal', '"a\nb"', STATIC),
    ('bad-escape', '"\\q"', STATIC),
    ('empty-u', '"\\u{}"', STATIC),
    ('seven-digits', '"\\u{1000000}"', STATIC),
    ('surrogate-escape', '"\\u{D800}"', STATIC),
    ('past-10ffff', '"\\u{110000}"', STATIC),
    ('not-hex', '"\\u{zz}"', STATIC),
    ('bad-utf8', b'"a\xff"', STATIC),
    ('overlong-utf8', b'"\xc0\xaf"', STATIC),
    ('encoded-surrogate', b'"\xed\xa0\x80"', STATIC),
    ('len-arity', '(str/len "a" "b")', STATIC),
    ('char-arity', '(str/char)', STATIC),
    ('cat-arity', '(str/cat "a")', STATIC),
    # D31: a column counts code points: the form opens at column 5.
    ('column-after-astral', '"' + chr(0x1F600) + '" (+ 1 2 3)', at(1, 5)),
    ('column-after-accent', '"e' + chr(0x301) + '" (+ 1 2 3)', at(1, 6)),
    # D32: printing, where JSON and the host's own escapes differ.
    ('print-astral', '(str/char 128512)', value('"' + chr(0x1F600) + '"')),
    ('print-nul', '(str/char 0)', value('"\\u{0}"')),
    ('print-del', '(str/char 127)', value('"\\u{7f}"')),
    ('print-ls', '(str/char 8232)', value('"' + chr(0x2028) + '"')),
    ('print-bom', '(str/char 65279)', value('"' + chr(0xFEFF) + '"')),
    ('print-quote-backslash', '(str/cat (str/char 34) (str/char 92))', value('"' + chr(92) + '"' + chr(92) * 2 + '"')),
    # D33: where UTF-16 and code points part.
    ('len-astral', '(str/len (str/cat (str/char 128512) (str/char 128512)))', value(2)),
    ('at-after-astral', '(str/code (str/at (str/cat (str/char 128512) "b") 1))', value(98)),
    ('lt-ffff-10000', '(str/lt (str/char 65535) (str/char 65536))', value('#true')),
    ('lt-e000-1f600', '(str/lt (str/char 57344) (str/char 128512))', value('#true')),
    ('eq-not-normalised', '(== (str/char 233) (str/cat "e" (str/char 769)))', value('#false')),
    ('char-surrogate', '(str/char 55296)', fault('not a character')),
    ('code-of-pair', '(str/code (str/cat (str/char 55295) (str/char 57344)))', fault('not a character')),
    ('big-cat', '(str/len (str/cat "' + 'x' * 100000 + '" "' + chr(0x1F600) * 100000 + '"))', value(200000)),
]

def probe_table(table):
    rows, bad = [], 0
    for name, src, (want, ok) in table:
        o, e, s = run(src, name, timeout=120)
        got = (o + e).strip().replace('\n', ' / ')[:90] + f' [exit {s}, {LAST.get("secs", 0):.1f}s, {LAST.get("maxrss_mb", 0)} MB peak so far]'
        verdict = 'record' if ok is None else 'ok' if ok(o, e, s) else 'WRONG'
        bad += verdict == 'WRONG'
        rows.append((name, want, verdict, got))
    w = max(len(r[0]) for r in rows)
    for name, want, verdict, got in rows:
        print(f'{name:<{w}}  {verdict:<6}  want: {want}\n{"":<{w}}          got:  {got}')
    print(f'probes: {len(rows)}, {bad} wrong')
    return bad

# ---- fuzz for strings: random programs, the interpreter against the referee ----

CHARS = [0, 7, 9, 10, 31, 32, 34, 39, 92, 97, 127, 233, 769, 8205, 8232, 55295, 57344, 65279, 65535, 65536, 128512, 1114111]

def lit(rng):
    out = []
    for _ in range(rng.randint(0, 4)):
        c = rng.choice(CHARS)
        if c in (34, 92):
            out.append('\\' + chr(c))
        elif c < 32 or c == 127 or rng.random() < 0.3:
            out.append('\\u{%x}' % c)
        else:
            out.append(chr(c))
    return '"' + ''.join(out) + '"'

def sgen(rng, depth, want='str'):
    """A well-formed program around strings; it may fault while running."""
    if depth == 0 or rng.random() < 0.2:
        if want == 'int' or rng.random() < 0.1:
            return str(rng.choice([0, 1, 2, -1, 3, 65535, 65536, 55296, 1114111, 1114112, 128512]))
        return lit(rng)
    r = rng.random()
    if want == 'int':
        return rng.choice([f'(str/len {sgen(rng, depth - 1)})', f'(str/code {sgen(rng, depth - 1)})',
                           f'(+ {sgen(rng, depth - 1, "int")} {sgen(rng, depth - 1, "int")})'])
    if r < 0.3:
        return f'(str/cat {sgen(rng, depth - 1)} {sgen(rng, depth - 1)})'
    if r < 0.45:
        return f'(str/at {sgen(rng, depth - 1)} {sgen(rng, depth - 1, "int")})'
    if r < 0.55:
        return f'(str/char {sgen(rng, depth - 1, "int")})'
    if r < 0.65:
        return f'(if (str/lt {sgen(rng, depth - 1)} {sgen(rng, depth - 1)}) {sgen(rng, depth - 1)} {sgen(rng, depth - 1)})'
    if r < 0.72:
        return f'(if (== {sgen(rng, depth - 1)} {sgen(rng, depth - 1)}) "same" "differ")'
    if r < 0.80:
        return f'(within {rng.randint(0, 6)} {sgen(rng, depth - 1)})'
    if r < 0.90:
        return f'(str/len {sgen(rng, depth - 1)})'
    return f'(str/code {sgen(rng, depth - 1)})'

def fuzz_str(n=1000, seed=1):
    rng = random.Random(seed)
    progs = [sgen(rng, rng.randint(1, 5)) for _ in range(n)]
    diffs, skipped = [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as ex:
        for i, src, want, got in ex.map(lambda a: one(*a), enumerate(progs)):
            if want is None:
                skipped += 1
            elif want != got:
                diffs.append((i, src, want, got))
    for i, src, want, got in diffs[:20]:
        print(f'--- {i}: {src}\n    referee: {want.strip()!r}\n    interp:  {got.strip()!r}')
    print(f'fuzz-str: {n} programs (seed {seed}), {len(diffs)} differ, {skipped} outside the referee')
    return len(diffs)

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
    r = subprocess.run(['python3', '-I', 't/referee/calc.py', path], capture_output=True,
                       env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    return None if r.returncode == 3 else r.stdout.decode('utf-8', 'replace')

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
    if what == 'probes-fn':
        sys.exit(1 if probe_table(PROBES_FN) else 0)
    if what == 'probes-str':
        sys.exit(1 if probe_table(PROBES_STR) else 0)
    if what == 'fuzz-str':
        sys.exit(1 if fuzz_str(*(int(a) for a in sys.argv[2:4])) else 0)
    if what == 'process':
        sys.exit(1 if process(*sys.argv[2:3]) else 0)
    print(__doc__)
    sys.exit(2)

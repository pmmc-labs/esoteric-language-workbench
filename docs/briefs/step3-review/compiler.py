#!/usr/bin/env python3
"""The compiler held to the reviewer's model of step 3, and to perl.

    python3 docs/briefs/step3-review/compiler.py SEED COUNT [nl]

model.py, pools.py and harness.py are the reviewer's own, as it left
them (docs/PLAN.md, step 3): a model of the step's definition written
from the proposal alone, with the amendments its review asked for as
switches, all on here. a4_random.py is its generator of random
statements over the whole grammar, and this script generates the same
way.

Each statement is given to the reviewer's model alone, and then:

  the model prints    The statements go to the compiler, 300 to a
                      program, and to perl. The compiled program must
                      print what perl prints, and perl must say nothing.
                      A statement the compiler refuses or faults on is
                      taken out and counted, which is allowed: the
                      compiler may be stricter than the model.
  the model faults    A sample of them, each a program of its own. The
                      compiler must refuse it, or fault having printed
                      nothing; or print what perl prints, perl silent.
  the model refuses   A sample, each alone: the compiler must refuse it,
                      or run and print what perl prints, perl silent.

What it reports as WRONG is a program the compiler accepts that runs,
doesn't fault, and differs from perl. Not part of make test.
"""
import os, random, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import model
from pools import numstrings, numbers, q

sys.set_int_max_str_digits(0)      # a string of a thousand digits is a number to the model
for k in model.OPT:
    if k.startswith('amend_'):
        model.OPT[k] = True

PERL = os.environ.get('CURLY_PERL', 'perl')
HO = "use v5.42;\nuse open ':std', ':encoding(UTF-8)';\n"
seed, count = int(sys.argv[1]), int(sys.argv[2])
NL = 'nl' in sys.argv
R = random.Random(seed)
S = [s for s in numstrings(full=False) if len(s) < 45 and '3037000' not in s]
NICE_S = ['abc', 'Ab', '', ' ', 'a b', 'x', 'hello world', '12', '3', '1.5', '2.0', '1e3', '-4', '0', '007', ' 5 ', '65', '0.5', '10', '-1.0', '+7', 'aXb', '(', ')', '#', "it's", '5e0', '00', '-0', '.5', 'e', '9']
NICE_N = ['0', '1', '2', '3', '5', '10', '65', '100', '0.5', '1.5', '2.0', '1e3', '3.0', '0.1', '7', '255', '2.5', '1e15', '0x10', '0b11', '0o17', '1_000', '.5', '1.0']
N = [n for n in numbers() if '3037000500' not in n]
UN = ['length', 'uc', 'lc', 'ord', 'chr']

def lit():
    r = R.random()
    if r < 0.30: return R.choice(NICE_N)
    if r < 0.60:
        s = R.choice(NICE_S)
        if R.random() < 0.3 and "'" not in s and '\\' not in s: return "'" + s + "'"
        return q(s)
    if r < 0.75: return q(R.choice(S))
    if r < 0.90: return R.choice(N)
    return R.choice(['"\\x{E9}"', '"\\x{100}a"', '"a\\x{10FFFF}"', '"\\xFF"', '"\\0"', '"\\n"', '"A\\tb"', '9007199254740993', '4611686018427387904', '1e16', '"1e15"', '"9007199254740992"', '18014398509481984'])

def ws():
    r = R.random()
    if NL and r < 0.25: return R.choice(['\n', ' \n', '\n ', ' # c\n', '\t', '\n\n', ' # ) x . (\n', '\n# "\n'])
    return ' ' if r < 0.8 else '' if r < 0.95 else '  '

def expr(d):
    if d <= 0 or R.random() < 0.12: return lit()
    r = R.random()
    if r < 0.50:
        op = R.choice(['+', '-', '*', '/', '%', '**', '.', '.', '.', 'x', 'x', '+', '*'])
        return expr(d - 1) + ws() + op + ws() + expr(d - 1)
    if r < 0.60: return '(' + expr(d - 1) + ')'
    if r < 0.67: return R.choice(['-', '-', '+', '- ']) + expr(d - 1)
    if r < 0.77: return R.choice(UN) + R.choice(['', '', ' ']) + '(' + expr(d - 1) + ')'
    if r < 0.89: return R.choice(UN) + (ws() if NL else R.choice([' ', ' ', ''])) + expr(d - 1)
    if r < 0.95:
        a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.6 else [])
        return 'substr' + R.choice(['', '', ' ']) + '(' + ', '.join(a) + ')'
    a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.5 else [])
    return 'index' + R.choice(['', '', ' ']) + '(' + ','.join(a) + ')'

def statement():
    e = expr(R.choice([1, 2, 2, 3]))
    r = R.random()
    return ('say %s;' if r < 0.7 else 'say(%s);' if r < 0.8 else 'print %s;' if r < 0.9 else 'print(%s);') % e

def verdict(stmt):
    """What the reviewer's model makes of one statement alone."""
    try:
        prog = model.parse((HO + stmt + '\n').encode())
    except model.Refuse:
        return 'refuses'
    try:
        out, fault = model.run(prog)
    except model.Big:
        # A string too long for the model to build: perl builds it as it
        # compiles (T102), and the compiler faults.
        return 'faults'
    return 'faults' if fault is not None else 'prints'

work = tempfile.mkdtemp(prefix='step3-review-')

def both(stmts):
    """(what the compiler did, its stdout, perl's stdout, perl's stderr,
    the line of a refusal or a fault) for a program of these statements."""
    path = os.path.join(work, 'p.pl')
    open(path, 'w').write(HO + ''.join(s + '\n' for s in stmts))
    c = subprocess.run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', os.path.join(work, 'p'), path], capture_output=True, text=True)
    if c.returncode == 1:
        return 'refused', b'', b'', b'', int(c.stderr.split(':')[1])
    assert c.returncode == 0, c.stderr
    r = subprocess.run([os.path.join(work, 'p')], capture_output=True, stdin=subprocess.DEVNULL)
    p = subprocess.run([PERL, path], capture_output=True, stdin=subprocess.DEVNULL)
    if r.returncode == 0:
        return 'ran', r.stdout, p.stdout, p.stderr, 0
    assert r.returncode == 1, r
    return 'faulted', r.stdout, p.stdout, p.stderr, int(r.stderr.split(b' line ')[-1].rstrip(b'.\n'))

def line_of(stmts, line):
    """Which statement a line of the program is in."""
    at = 3
    for n, s in enumerate(stmts):
        at += s.count('\n') + 1
        if line < at:
            return n
    return len(stmts) - 1

counts = {'the model prints': 0, 'and the compiler agrees with perl': 0, 'which the compiler refuses': 0,
          'which the compiler faults on': 0, 'the model faults (sampled)': 0, 'the model refuses (sampled)': 0, 'WRONG': 0}
wrong = []
stricter = []       # what the compiler refuses or faults on, and the model prints
by = {'prints': [], 'faults': [], 'refuses': []}
for _ in range(count):
    s = statement()
    by[verdict(s)].append(s)
print(f"seed {seed}: {count} statements; the reviewer's model prints for {len(by['prints'])}, faults on {len(by['faults'])}, refuses {len(by['refuses'])}", flush=True)

pending = by['prints']
counts['the model prints'] = len(pending)
while pending:
    batch, pending = pending[:300], pending[300:]
    while batch:
        what, out, perl_out, perl_err, line = both(batch)
        if what == 'ran':
            if out == perl_out and not perl_err:
                counts['and the compiler agrees with perl'] += len(batch)
            elif len(batch) == 1:
                counts['WRONG'] += 1
                wrong.append((batch[0], out, perl_out, perl_err))
            else:
                # Somewhere in here: one at a time.
                pending = [[s] for s in batch] and pending
                for s in batch:
                    w, o, po, pe, _ = both([s])
                    if w == 'ran' and (o != po or pe):
                        counts['WRONG'] += 1
                        wrong.append((s, o, po, pe))
                    elif w == 'ran':
                        counts['and the compiler agrees with perl'] += 1
                    else:
                        counts['which the compiler refuses' if w == 'refused' else 'which the compiler faults on'] += 1
            break
        n = line_of(batch, line)
        counts['which the compiler refuses' if what == 'refused' else 'which the compiler faults on'] += 1
        stricter.append((what, batch[n]))
        if what == 'faulted' and not perl_out.startswith(out):
            counts['WRONG'] += 1
            wrong.append((batch[n], out, perl_out, perl_err))
        del batch[n]

for kind, name in (('faults', 'the model faults (sampled)'), ('refuses', 'the model refuses (sampled)')):
    for s in R.sample(by[kind], min(150, len(by[kind]))):
        counts[name] += 1
        what, out, perl_out, perl_err, _ = both([s])
        if what == 'ran' and (out != perl_out or perl_err):
            counts['WRONG'] += 1
            wrong.append((s, out, perl_out, perl_err))
        elif what == 'faulted' and not perl_out.startswith(out):
            counts['WRONG'] += 1
            wrong.append((s, out, perl_out, perl_err))

for k, v in counts.items():
    print(f'{v:8}  {k}')
for what, s in stricter[:12]:
    print(f'{what}: {s!r}')
for s, out, perl_out, perl_err in wrong[:20]:
    print(f'WRONG: {s!r}\n   the compiler: {out[:120]!r}\n   perl: {perl_out[:120]!r} {perl_err[:200]!r}')
sys.exit(1 if wrong else 0)

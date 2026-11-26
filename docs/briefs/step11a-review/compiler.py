#!/usr/bin/env python3
"""Holds the compiler to the reviewer's model of step 11a's lexing rule, and
to perl, over the strings fuzz.py makes (written by the builder, after the
build; model.py and fuzz.py are the reviewer's, unchanged).

For every string: the compiler's verdict (classify.ts: refused, or the
pieces its lexer found) beside the model's.

  both take it         the pieces must be the same
  the model alone      counted, by the compiler's message: the compiler is
                       the stricter there
  the compiler alone   run: the string under perl and compiled, which must
                       print the same with nothing on stderr, or fault where
                       perl warns

And a sample of what both take is compiled and run beside perl, batches of
strings to a program.

    python3 docs/briefs/step11a-review/compiler.py [MODE ...]

MODE is exhaustive, random, arrow, index, for, sort (default: all). Work
files go to $REVIEW_TMP.
"""

import collections
import re
import json
import os
import random
import subprocess
import sys
import functools
print = functools.partial(print, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import model
import fuzz

PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
TMP = os.environ.get('REVIEW_TMP', os.path.join(HERE, 'tmp'))
SEP = '=#=#='

class Opts(model.Opts):
    refuse_leading_zero = True      # T211
    blank_after_minus = False       # D95
    trailing_comma = True           # D95

def classify(bodies):
    out = []
    for k in range(0, len(bodies), 20000):
        ask = json.dumps({'header': fuzz.HEADER, 'wrap': list(fuzz.WRAP), 'bodies': bodies[k:k + 20000]})
        r = subprocess.run(['node', os.path.join(HERE, 'classify.ts')], input=ask, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-2000:]
        out += json.loads(r.stdout)
    return out

def norm(pieces):
    """Pieces as lists, text beside text joined."""
    out = []
    for p in json.loads(json.dumps(pieces)):
        if p[0] == 'text' and out and out[-1][0] == 'text':
            out[-1][1] += p[1]
        else:
            out.append(p)
    return out

def program(bodies):
    # (In a batch the sort's array is declared once: a second `my @r` is a
    # warning of perl's, and no part of what is asked.)
    if fuzz.WRAP[0].startswith('my @r = '):
        return fuzz.HEADER + 'my @r;\n' + ''.join(f'{fuzz.WRAP[0][3:]}print "{b}"; print "\\n{SEP}\\n";{fuzz.WRAP[1]}\n' for b in bodies)
    return fuzz.HEADER + ''.join(f'{fuzz.WRAP[0]}print "{b}"; print "\\n{SEP}\\n";{fuzz.WRAP[1]}\n' for b in bodies)

def run_both(bodies, tag):
    """The strings as one program, under perl and compiled. A string perl
    warns on, or stops at, is taken out and tried alone; returns what
    differs."""
    bad = []
    lines_before = fuzz.HEADER.count('\n') + fuzz.WRAP[0].startswith('my @r = ')
    bodies = list(bodies)
    while True:
        path = os.path.join(TMP, f'batch-{tag}.pl')
        open(path, 'w').write(program(bodies))
        p = subprocess.run([PERL, path], capture_output=True, timeout=120)
        err = p.stderr.decode('utf-8', 'replace')
        if not err and p.returncode == 0:
            break
        # Each string is a line (one with a new line in it is more): every
        # one perl names a line of is taken out, and the rest tried again.
        named = sorted(set(int(n) for n in re.findall(r' line (\d+)', err)))
        assert named, err[:300]
        out, line = set(), lines_before
        for n, b in enumerate(bodies):
            first, line = line + 1, line + 1 + b.count('\n')
            if any(first <= k <= line for k in named):
                out.add(n)
        assert out, err[:300]
        said = err.strip().split('\n')[0]
        bad += [(bodies[n], said) for n in sorted(out)]
        bodies = [b for n, b in enumerate(bodies) if n not in out]
    if bodies:
        exe = os.path.join(TMP, f'batch-{tag}')
        c = subprocess.run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', exe, path], capture_output=True, text=True)
        assert c.returncode == 0, c.stderr[:500]
        r = subprocess.run([exe], capture_output=True, timeout=120)
        if r.stdout != p.stdout or r.stderr or r.returncode:
            theirs, ours = p.stdout.decode('utf-8', 'replace').split(f'\n{SEP}\n'), r.stdout.decode('utf-8', 'replace').split(f'\n{SEP}\n')
            for n, b in enumerate(bodies):
                if n >= len(ours) or ours[n] != theirs[n]:
                    return [('DIFFERS', b, theirs[n], ours[n] if n < len(ours) else r.stderr.decode()[:200])], bad
    return [], bad

def alone(body, tag):
    """A string perl complains of: the compiled program must fault."""
    path = os.path.join(TMP, f'alone-{tag}.pl')
    open(path, 'w').write(fuzz.HEADER + f'{fuzz.WRAP[0]}print "{body}";{fuzz.WRAP[1]}\n')
    exe = os.path.join(TMP, f'alone-{tag}')
    c = subprocess.run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', exe, path], capture_output=True, text=True)
    if c.returncode != 0:
        return 'refused after all: ' + c.stderr.strip()[-120:]
    r = subprocess.run([exe], capture_output=True, timeout=60)
    return None if r.returncode == 1 and r.stderr.startswith(b'fault: ') else f'runs: exit {r.returncode}, {r.stdout[:80]!r}'

def hold(bodies, tag, sample=4000):
    os.makedirs(TMP, exist_ok=True)
    verdicts = classify(bodies)
    both = same = 0
    stricter = collections.Counter()
    differ, lone, taken = [], [], []
    for b, v in zip(bodies, verdicts):
        kind, got = model.lex(b, fuzz.SCALARS, fuzz.ARRAYS, Opts)
        if 'ok' in v and kind == 'ok':
            both += 1
            taken.append(b)
            if norm(v['ok']) == norm(got):
                same += 1
            else:
                differ.append((b, v['ok'], got))
        elif 'ok' in v:
            lone.append((b, got))
        elif kind == 'ok':
            stricter[v['no'].split(':')[0][:70]] += 1
    print(f'{tag}: {len(bodies)} strings; both take {both}, the same pieces for {same}; the compiler alone refuses {sum(stricter.values())}; the compiler alone takes {len(lone)}')
    for b, ours, theirs in differ[:20]:
        print(f'  PIECES DIFFER {b!r}: compiler {ours}, model {theirs}')
    for why, n in stricter.most_common(12):
        print(f'  stricter, {n}: {why}')
    reasons = collections.Counter(str(got)[:60] for _, got in lone)
    for why, n in reasons.most_common(8):
        print(f'  the model refused, {n}: {why}')
    # What the compiler alone takes, all of it; and a sample of the rest.
    r = random.Random(11)
    rest = r.sample(taken, min(sample, len(taken)))
    wrong = []
    for name, group in (('alone', [b for b, _ in lone]), ('sample', rest)):
        ran = faulted = skipped = 0
        for k in range(0, len(group), 1500):
            diffs, bad = run_both(group[k:k + 1500], tag)
            wrong += diffs
            ran += len(group[k:k + 1500]) - len(bad)
            # Each of these is a compile and a run of its own: 150 a
            # batch at most, picked at random.
            skipped += max(0, len(bad) - 150)
            for b, err in r.sample(bad, min(150, len(bad))):
                why = alone(b, tag)
                faulted += why is None
                if why is not None:
                    wrong.append(('PERL COMPLAINS', b, err, why))
        print(f'  {name}: {ran} run beside perl and the same, {faulted} that perl warns of and the program faults at, {skipped} more that perl warns of and were not tried')
    for w in wrong[:20]:
        print('  WRONG', w)
    return len(differ) + len(wrong)

def main(modes):
    modes = modes or ['exhaustive', 'random', 'arrow', 'index', 'for', 'sort']
    failed = 0
    for mode in modes:
        if mode == 'exhaustive':
            failed += hold(fuzz.exhaustive(), mode)
        elif mode == 'random':
            failed += hold(fuzz.rand(200000, 7), mode)
        elif mode == 'arrow':
            failed += hold(fuzz.arrow(), mode)
        elif mode == 'index':
            failed += hold(fuzz.index(), mode)
        else:
            failed += hold(fuzz.binder(mode), mode)
    print('nothing differs' if not failed else f'{failed} DIFFER')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

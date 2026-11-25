#!/usr/bin/env python3
"""What perl 5.42 does when it compares, and when a boolean is used as a
number, under every past of every operand; and the rule step 4 proposes
(docs/PLAN.md), held to it.

    python3 docs/briefs/step4-comparisons.py

perl keeps, in a value, what it has been used as: a string that has been
a float, an Int that has been a float (T83, T92). A value in the language
has no past. So a rule has to give perl's answer where every past gives
the same one, and fault where they differ. Steps 2 and 3 each made that
claim of arithmetic and each had it refuted by a review, so this asks
perl before the proposal is written: each operand fresh, after a use as a
float, as an integer, as a string, and as a float and then an integer.

The rule for the numeric comparisons, `compare`:

    Both operands are made numbers as D40 has it (a string that isn't a
    number faults; so does one D40 faults on).
    Both integral (an Int, or a whole Num below 2^53, a soft string
    included): the whole numbers are compared, exactly.
    Otherwise: the doubles are compared.

That is D35's one question again, and nothing more: the run found no
place where perl's answer turns on an operand's past and the rule doesn't
already fault for D40's reasons. (perl marks a number as carrying a float
only when the float is exactly the number, so two whole numbers past 2^53
that differ are never compared as the one double they share.)

`==`, `!=`, `<`, `<=`, `>`, `>=` give a boolean and `<=>` gives -1, 0 or
1. The string comparisons make both operands strings, as `say` prints
them, and compare those character by character (`compare_strings`); truth
is perl's (`truth`). A boolean as a number is the Int 1 or 0 (`as_int`), and that is held
to perl here too, in arithmetic, under every past of the other operand.

Not part of make test.
"""

import importlib.util
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
step3 = load('step3', 'step3-strings-as-numbers.py')
step2 = step3.step2
Fault = step3.Fault

def number(v):
    """An operand as D40 has it: ('i', n), ('n', x) or ('soft', x)."""
    if v[0] == 's':
        return step3.numify(v[1])
    if v[0] == 'b':
        return ('i', int(v[1]))
    return v

def compare(a, b):
    """-1, 0 or 1."""
    p, q = number(a), number(b)
    plain = [('n', v[1]) if v[0] == 'soft' else v for v in (p, q)]
    x, y = step2.integral(plain[0]), step2.integral(plain[1])
    if x is not None and y is not None:
        return (x > y) - (x < y)
    fx, fy = float(plain[0][1]), float(plain[1][1])
    return (fx > fy) - (fx < fy)

def text(v):
    """An operand as a string: what `say` prints for it (D36's fault
    included), and for a boolean `1` or the empty string."""
    if v[0] == 's':
        return v[1]
    if v[0] == 'b':
        return '1' if v[1] else ''
    if v[0] == 'i':
        return str(v[1])
    x = v[1]
    if x == math.trunc(x) and 10**15 <= abs(x) < 2**53:
        raise Fault('a whole float this size prints two ways in perl')
    return '0' if x == 0 else '%.15g' % x

def compare_strings(a, b):
    """-1, 0 or 1: the two as strings, character by character."""
    s, t = text(a), text(b)
    return (s > t) - (s < t)

def truth(v):
    """perl's: false is the empty string, the string `0`, a number that
    is zero, and the boolean false. (undef too, which has no past.)"""
    return v[1] not in ('', '0') if v[0] == 's' else bool(v[1])

NUMERIC = {'==': lambda c: c == 0, '!=': lambda c: c != 0, '<': lambda c: c < 0, '<=': lambda c: c <= 0,
           '>': lambda c: c > 0, '>=': lambda c: c >= 0, '<=>': lambda c: c}

PASTS = {
    'fresh': '',
    'float': 'my $t = %s > 0.5;',
    'integer': 'my $t = %s + 0;',
    'string': 'my $t = "%s";',
    'float, integer': 'my $t = %s > 0.5; $t = %s %% 7;',
}

STRINGS = [s for s in step3.STRINGS] + ['9007199254740994', '9007199254740992.5', '-9007199254740993', '18014398509481985',
                                        '18014398509481984', '9223372036854775806', '3', '3.5']
OTHERS = step3.OTHERS + [('i', 2**53 + 2), ('i', 2**54 + 1), ('i', 2**54), ('i', step3.INT_MAX - 1), ('n', 2.0**54), ('n', 2.0**63),
                         ('n', 3.5), ('n', -(2.0**53))]
BOOLS = [('b', True), ('b', False)]

step3_value = step3.perl_value

def perl_value(v):
    if v[0] == 'b':
        return '(!!1)' if v[1] else '(!!0)'
    return step3_value(v)

def ask(cases):
    """perl's answers for each (op, a, b), one per pair of pasts. With b
    None the operator is before a."""
    perl = os.environ.get('CURLY_PERL', 'perl')
    lines = ['use v5.42; use warnings;', 'sub n($hex) { return unpack "d>", pack "H16", $hex }',
             'our ($listening, $warned) = (0, 0); $SIG{__WARN__} = sub { $warned = 1 if $listening };',
             'sub shown($r) { return !defined $r ? "undef" : $r eq "" ? "F" : "$r" }']
    keys = []
    for n, (op, a, b) in enumerate(cases):
        for pa in PASTS.values():
            for pb in PASTS.values():
                before = pa.replace('%s', '$x').replace('%%', '%') + ' ' + pb.replace('%s', '$y').replace('%%', '%')
                expr = f'{op}$x' if b is None else f'$x {op} $y'
                lines.append(f'sub {{ ($listening, $warned) = (0, 0); my $x = {perl_value(a)}; my $y = {perl_value(b or a)}; {before} '
                             f'$listening = 1; my $r = eval {{ {expr} }}; say $warned ? "warns" : $@ ? "dies" : shown($r); }}->();')
                keys.append(n)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'compare.pl')
        open(path, 'w').write('\n'.join(lines) + '\n')
        r = subprocess.run([perl, path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[:2000])
    answers = [[] for _ in cases]
    for n, line in zip(keys, r.stdout.split('\n')):
        answers[n].append(line)
    return answers

def shown(v):
    return 'F' if v is False else '1' if v is True else str(v)

def cases():
    strings = [('s', s) for s in STRINGS]
    pairs = [(a, b) for a in strings for b in OTHERS] + [(b, a) for a in strings for b in OTHERS]
    pairs += [(a, b) for a in strings for b in strings] + [(a, b) for a in OTHERS for b in OTHERS]
    pairs += [(a, b) for a in BOOLS for b in OTHERS + strings[::2] + BOOLS] + [(b, a) for a in BOOLS for b in OTHERS]
    return pairs

def main():
    pairs = cases()
    wrong = two = 0
    counts = {}
    # `<=>` first, over every pair; the other six are the same comparison
    # read six ways, and perl has a short cut of its own in each.
    for op in ['<=>', '==', '<', '!=', '<=', '>', '>=']:
        cs = [(op, a, b) for a, b in (pairs if op in ('<=>', '==', '<') else pairs[::3])]
        for (_, a, b), perls in zip(cs, ask(cs)):
            two += len(set(perls)) > 1
            try:
                r = shown(NUMERIC[op](compare(a, b)))
                what = 'an answer'
                if any(p != r for p in perls):
                    wrong += 1
                    if wrong <= 30:
                        print(f'WRONG {a} {op} {b}: the rule {r}; perl, by its past: {sorted(set(perls))}')
            except Fault as f:
                what = f'fault: {f}'
            counts[what] = counts.get(what, 0) + 1
    total = sum(counts.values())
    first_wrong = wrong
    print(f'{total} comparisons, each under {len(PASTS) ** 2} pairs of pasts; perl has more than one answer for {two}')
    print(f'the rule gives an answer perl does not, under some past, on {wrong}')
    for what, n in sorted(counts.items()):
        print(f'    {n:6}  {what}')

    # The string comparisons, and truth.
    wrong = two = 0
    counts = {}
    values = [('s', s) for s in STRINGS] + OTHERS + BOOLS
    for op in ['cmp', 'eq', 'lt', '!']:
        if op == '!':
            cs = [(op, a, None) for a in values]
        else:
            cs = [(op, a, b) for a in values for b in values[::2 if op == 'cmp' else 5]]
        for (_, a, b), perls in zip(cs, ask(cs)):
            two += len(set(perls)) > 1
            try:
                r = shown(not truth(a) if op == '!' else NUMERIC[{'cmp': '<=>', 'eq': '==', 'lt': '<'}[op]](compare_strings(a, b)))
                what = 'an answer'
                if any(p != r for p in perls):
                    wrong += 1
                    if wrong <= 30:
                        print(f'WRONG {a} {op} {b}: the rule {r}; perl, by its past: {sorted(set(perls))}')
            except Fault as f:
                what = f'fault: {f}'
            counts[what] = counts.get(what, 0) + 1
    print(f'{sum(counts.values())} string comparisons and tests of truth; perl has more than one answer for {two}')
    print(f'the rule gives an answer perl does not, under some past, on {wrong}')
    for what, n in sorted(counts.items()):
        print(f'    {n:6}  {what}')
    all_wrong = wrong

    # A boolean as a number: the Int 1 or 0, in arithmetic, beside every
    # other operand under every past step 3's script knows.
    step3.perl_value = perl_value
    cs = [(op, a, b) for op in step2.OPS for a in BOOLS for b in step3.OTHERS + [('s', s) for s in step3.STRINGS] + BOOLS]
    cs += [(op, b, a) for op, a, b in cs]
    bad = 0
    for (op, a, b), perls in zip(cs, step3.ask_perl(cs)):
        try:
            r = step3.language3(op, *[('i', int(v[1])) if v[0] == 'b' else v for v in (a, b)])
        except Fault:
            continue
        if any(not step3.agrees(r, p) for p in perls):
            bad += 1
            if bad <= 10:
                print(f'WRONG {a} {op} {b}: the rule {step3.shown(r)}; perl, by its past: {sorted(set(perls))}')
    print(f'{len(cs)} operations with a boolean as the Int 1 or 0; a value perl does not give, under some past, on {bad}')
    return 1 if first_wrong or all_wrong or bad else 0

if __name__ == '__main__':
    sys.exit(main())

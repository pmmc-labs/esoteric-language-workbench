#!/usr/bin/env python3
"""What perl 5.42 does with `++`, `--` and the assigning operators, under
every past of the variable, and the rule step 5 proposes (docs/PLAN.md),
held to it.

    python3 docs/briefs/step5-increments.py

A variable in perl carries what it has been used as (T83, T92), and `++`
and `--` change it where it stands, by routes of their own (T93). So
each is asked of every value fresh, after a use as a float, as an
integer, as a string, and as a float and then an integer.

The rule, `step`, for `++` (and `--`):

    undef           the Int 1 (-1)
    a boolean       the Int one more (less) than its 1 or 0
    an Int          the Int one more (less), or `integer overflow`
    a Num           `++`: as `$x + 1` is (D35): the Int if the Num is
                    integral, otherwise the Num one more.
                    `--`: the Num one less, always; and a fault if the
                    Num is integral and the answer reaches 2^53 in size,
                    where perl has the float or the integer by the Num's
                    past (T93).
                    Either: a fault if the Num is so large that the step
                    is lost, `$x + 1 == $x`, where perl warns.
    a string        its number by D40, and then the Num one more (less),
                    whatever kind of number the string is: perl steps it
                    as an integer or as a float by the string's past. A
                    fault if the number is whole and it or the answer
                    reaches 2^53; and for `++`, if the string is digits
                    that begin with a zero, which perl steps as text
                    ("009" to "010") until it has been used as a number.
                    A string that isn't a number faults
                    (perl's `++` on one makes the next string, `aa` to
                    `ab`, and its `--` makes -1, in silence: T44)

The value of `$x++` is `$x` as it was (0 for an undef), and of `$x--`
likewise (an undef for an undef: T43). `$x OP= $y` is `$x = $x OP $y`,
which the second half checks: step 3's rule, `language3`, against what
perl leaves in `$x`.

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
INT_MIN, INT_MAX = step3.INT_MIN, step3.INT_MAX

def step(op, v):
    """('i', n) or ('n', x): what `++` or `--` leaves in the variable."""
    d = 1 if op == '++' else -1
    if v[0] == 'u':
        return ('i', d)
    if v[0] == 'b':
        return ('i', int(v[1]) + d)
    if v[0] == 's':
        # perl steps a string as an integer or as a float by what the
        # string has been used as, and the two are the same number while a
        # double holds it: so the Num, and a fault where one doesn't.
        x = float(step3.numify(v[1])[1])
        if x == math.trunc(x) and (abs(x) >= 2**53 or abs(x + d) >= 2**53):
            raise Fault('two answers')
        # And `++` on digits alone makes the next string, of the same
        # width, until the string has been used as a number: "009" is
        # "010", or 10.
        if op == '++' and len(v[1]) > 1 and v[1][0] == '0' and v[1].isdigit():
            raise Fault('two answers')
        return ('n', x + d)
    kind, x = v
    if kind == 'i':
        if not INT_MIN <= x + d <= INT_MAX:
            raise Fault('integer overflow')
        return ('i', x + d)
    whole = step2.integral(v)
    if op == '++' and whole is not None:
        return ('i', whole + 1)
    # perl warns when the step is lost: a float so large that one more or
    # less is the same float.
    if x + d == x:
        raise Fault('precision lost')
    if whole is not None and abs(whole - 1) >= 2**53:
        raise Fault('two answers')
    return ('n', x + d)

def agrees(rule, perl):
    """Whether perl's answer, `KIND VALUE [as it prints]`, is the rule's:
    the same number of a kind that can't be told from it (step 3's test),
    and the same text when it prints."""
    if perl == 'warns' or perl.startswith('dies'):
        return False
    value, text = perl.split(' [', 1)
    if not step3.agrees(rule, value):
        return False
    kind, x = rule
    if kind == 'n' and x == math.trunc(x) and 10**15 <= abs(x) < 2**53:
        return True         # the language faults when this one is printed (D36)
    return text[:-1] == (str(x) if kind == 'i' else '0' if x == 0 else '%.15g' % x)

PASTS = ['', 'my $t = $x > 0.5;', 'my $t = $x + 0;', 'my $t = "$x";', 'my $t = $x > 0.5; $t = $x % 7;', 'my $t = $x * 1.5;', 'my $t = -$x;']
VALUES = [('s', s) for s in step3.STRINGS] + step3.OTHERS + [('n', v) for v in (-(2.0**53), -(2.0**53) + 1, 2.0**53 - 1, 1e15 - 1, -1e15, 2.5, -0.5,
                                                                          4503599627370496.0, -9007199254740991.0)] + \
         [('i', v) for v in (INT_MAX - 1, INT_MIN + 1, -(2**53), -(2**53) + 1)] + [('b', True), ('b', False), ('u', None)]

def perl_value(v):
    return 'undef' if v[0] == 'u' else ('(!!1)' if v[1] else '(!!0)') if v[0] == 'b' else step3.perl_value(v)

def ask(cases):
    perl = os.environ.get('CURLY_PERL', 'perl')
    lines = [step2.PRELUDE.replace('no warnings;', 'use warnings;'),
             'our ($listening, $warned) = (0, 0); $SIG{__WARN__} = sub { $warned = 1 if $listening };']
    keys = []
    for n, (expr, v) in enumerate(cases):
        for past in PASTS:
            lines.append(f'sub {{ ($listening, $warned) = (0, 0); my $x = {perl_value(v)}; {{ no warnings; {past} }} $listening = 1; '
                         f'my $r = attempt(sub {{ {expr}; $x }}); say $warned ? "warns" : "$r [$x]"; }}->();')
            keys.append(n)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'steps.pl')
        open(path, 'w').write('\n'.join(lines) + '\n')
        r = subprocess.run([perl, path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[:2000])
    answers = [[] for _ in cases]
    for n, line in zip(keys, r.stdout.split('\n')):
        answers[n].append(line)
    return answers

def main():
    wrong = two = 0
    counts = {}
    cases = [(f'{op}$x' if pre else f'$x{op}', v) for op in ('++', '--') for pre in (True, False) for v in VALUES]
    for (expr, v), perls in zip(cases, ask(cases)):
        two += len(set(perls)) > 1
        try:
            r = step('++' if '++' in expr else '--', v)
            what = 'an Int' if r[0] == 'i' else 'a Num'
            if any(not agrees(r, p) for p in perls):
                wrong += 1
                if wrong <= 30:
                    print(f'WRONG {expr} on {v}: the rule {step3.shown(r)}; perl, by its past: {sorted(set(perls))}')
        except Fault as f:
            what = f'fault: {f}'
        counts[what] = counts.get(what, 0) + 1
    print(f'{len(cases)} steps, each under {len(PASTS)} pasts; perl has more than one answer for {two}')
    print(f'the rule leaves a value perl does not, under some past, on {wrong}')
    for what, n in sorted(counts.items()):
        print(f'    {n:6}  {what}')

    # `$x OP= $y` leaves in `$x` what `$x OP $y` is.
    cs = [(op + '=', a, b) for op in step2.OPS for a in [('s', s) for s in step3.STRINGS[::2]] + step3.OTHERS for b in step3.OTHERS[::2] + [('s', '3.0'), ('s', '12')]]
    bad = 0
    for (op, a, b), perls in zip(cs, step3.ask_perl(cs)):
        try:
            r = step3.language3(op[:-1], a, b)
        except Fault:
            continue
        if any(not step3.agrees(r, p) for p in perls):
            bad += 1
            if bad <= 10:
                print(f'WRONG {a} {op} {b}: the rule {step3.shown(r)}; perl, by its past: {sorted(set(perls))}')
    print(f'{len(cs)} assigning operations as the operation and then the assignment; a value perl does not leave, under some past, on {bad}')
    return 1 if wrong or bad else 0

if __name__ == '__main__':
    sys.exit(main())

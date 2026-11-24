#!/usr/bin/env python3
"""What perl 5.42 does with a string where a number is wanted, and the rule
step 3 proposes for it (docs/PLAN.md), held to perl.

    python3 docs/briefs/step3-strings-as-numbers.py

perl decides what a string is worth the first time it is used as a
number, and remembers: so the same string can give two answers,
depending on whether an operation that wanted a float met it before one
that wanted an integer. `my $s = "3.0"; say $s + 9007199254740990;`
prints 9.00719925474099e+15, and with `my $t = $s > 0.5;` in between it
prints 9007199254740993. A value in the language has no past. So the
rule has to give perl's answer where every past gives the same one, and
fault where they differ.

This script asks perl for every answer it can give: each operand, string
or number, fresh, after a float use (`$x > 0.5`), and after an integer
use (`$x + 0`); and requires of the rule (`language3`), for each
operation:

    a fault                      nothing (perl may do as it likes: D12)
    an Int k                     every perl answer is the integer k
    a Num x                      every perl answer is the float x, or the
                                 integer equal to x with x below 2^53
                                 (then nothing can tell them apart but
                                 printing from 1e15 up, where a Num
                                 faults, and the sign of a zero: T79)

The rule, for a string where a number is wanted:

    class A   digits                   the Int, or a fault past the Ints
                                       (and at -2^63 itself)
    class C   with an exponent         whole and below 2^53: the Int;
                                       whole and 2^53 or more: a fault
                                       (D23); otherwise the Num
    class B   with a point, no         the Num. If it is whole and below
              exponent                 2^53 it is "soft": arithmetic
                                       with it is float arithmetic, and
                                       faults if whole-number arithmetic
                                       would have given another answer
    anything else                      a fault: not a number (D15)

each after blanks, an optional sign, and before blanks. `Inf`, `NaN`
and `0 but true`, which perl takes in silence, are faults (D37).

A minus sign before a string negates its number as a Num, and faults for
a whole number of 2^53 or more, and for a string that starts with `+`,
which perl negates as text.

Not part of make test. t/models/str.py, written when step 3 is built, is
the model of the language; this is the evidence for its proposal.
"""

import importlib.util
import math
import os
import re
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('step2', os.path.join(HERE, 'step2-perl-numbers.py'))
step2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(step2)
Fault, language, shown = step2.Fault, step2.language, step2.shown
INT_MIN, INT_MAX = step2.INT_MIN, step2.INT_MAX

NUMERIC = re.compile(r'[ \t\n\r\f\v]*([+-]?)(?:(\d+)(?:(\.)(\d*))?|(\.)(\d+))(?:[eE]([+-]?\d+))?[ \t\n\r\f\v]*\Z')

def numify(text):
    """A string where a number is wanted: ('i', n), ('n', x) or ('soft', x)."""
    m = NUMERIC.match(text)
    if not m:
        raise Fault('not a numeric string')
    sign, whole, point, frac, lead_point, lead_frac, exponent = m.groups()
    digits = (whole or '') + ('.' + (frac or lead_frac or '') if point or lead_point else '')
    if exponent is None and not (point or lead_point):                      # class A
        n = int(sign + whole)
        # -2^63 too: perl holds that one string as an integer or as a
        # float, by its past, and no other.
        if not INT_MIN < n <= INT_MAX:
            raise Fault('integer overflow')
        return ('i', n)
    x = float(sign + digits + ('e' + exponent if exponent is not None else ''))
    if math.isinf(x):
        raise Fault('float overflow')
    whole_value = x == math.trunc(x)
    if exponent is not None:                                                # class C
        if whole_value and abs(x) < 2**53:
            return ('i', int(x))
        if whole_value:
            raise Fault('a whole number this large written with an exponent has two values in perl')
        return ('n', x)
    return ('soft', x) if whole_value and abs(x) < 2**53 else ('n', x)     # class B

def language3(op, a, b=None):
    """The proposed rule, for operands that may be strings."""
    values = [numify(v[1]) if v[0] == 's' else v for v in ((a,) if b is None else (a, b))]
    soft = [v[0] == 'soft' for v in values]
    plain = [('n', v[1]) if v[0] == 'soft' else v for v in values]
    if op == 'neg' and a[0] != 's':
        return language('neg', a)
    if op == 'neg':
        # perl negates a string of digits as an integer until it has been
        # used as a float, and as a float after: the same number, so a Num
        # will do, while a double can hold it. And a string that starts
        # with a plus it negates as text: -"+0" is the string "-0".
        if a[1].startswith('+'):
            raise Fault('a minus before a string that starts with a plus: perl changes the sign as text')
        x = float(plain[0][1])
        if x == math.trunc(x) and abs(x) >= 2**53:
            raise Fault('a minus before a string that is a whole number this large has two answers in perl')
        return step2.Num(-x)
    if op in ('+', '-', '*'):
        # T92. perl adds, subtracts and multiplies as floats when both
        # operands carry a float, and a whole number that has been used
        # as a float carries one if a double holds it exactly. So a whole
        # number of 2^53 or more that is exactly a double has two answers
        # with any operand but a true Int: `10000000000000000 + 1.0` is
        # 10000000000000001, or 1e+16 once the Int has been divided.
        wholes = [step2.integral(v) for v in plain]
        if all(w is not None for w in wholes):
            for k in (0, 1):
                other = (a, b)[1 - k]
                if abs(wholes[k]) >= 2**53 and float(wholes[k]) == wholes[k] and other[0] != 'i':
                    raise Fault('a whole number this large with a float or a string has two answers in perl')
    if not any(soft) or op == '%':
        return language(op, *plain)
    # A soft operand makes it float arithmetic, which is what perl does
    # with a string it has not yet used as a float.
    as_floats = [('n', float(v[1])) if s else v for v, s in zip(plain, soft)]
    x, y = float(as_floats[0][1]), float(as_floats[1][1])
    wholes = [step2.integral(v) for v in plain]
    if all(w is not None for w in wholes):
        # perl would do this on whole numbers once the string has been
        # used as a float. Same answer only when nothing is rounded.
        if any(abs(w) >= 2**53 for w in wholes):
            raise Fault('a string like "3.0" in arithmetic this large has two answers in perl')
        exact = None
        if op == '+': exact = wholes[0] + wholes[1]
        if op == '-': exact = wholes[0] - wholes[1]
        if op == '*': exact = wholes[0] * wholes[1]
        if op == '**' and wholes[1] >= 0: exact = wholes[0] ** wholes[1] if wholes[1] < 4096 else 2**64
        if exact is not None and abs(exact) >= 2**53:
            raise Fault('a string like "3.0" in arithmetic this large has two answers in perl')
    if op == '+': return step2.Num(x + y)
    if op == '-': return step2.Num(x - y)
    if op == '*': return step2.Num(x * y)
    if op == '/':
        if y == 0.0:
            raise Fault('division by zero')
        return step2.Num(x / y)
    if op == '**': return step2.Num(step2.libm.pow(x, y))
    raise AssertionError(op)

# ---- the values, and perl

STRINGS = ['0', '1', '12', '-12', '+12', ' 12 ', '012', '-0', '9007199254740991', '9007199254740993', '9223372036854775807',
           '9007199254740992', '10000000000000000', '-4611686018427387904',
           '-9223372036854775808', '9223372036854775808', '18446744073709551616', '1000000000000000', '999999999999999',
           '3.0', '-3.0', '5.', '0.0', '-0.0', '1.5', '.5', '-.5', '2.50', '1000000000000000.0', '999999999999999.0',
           '9007199254740991.0', '9007199254740992.0', '9007199254740993.0', '10000000000000000.0', '4503599627370496.0',
           '1e3', '1E3', '1.5e1', '1e0', '1.0e0', '1e-3', '1e15', '1e16', '-1e16', '1e19', '1e20', '9007199254740992e0',
           '4611686018427387904e0', '1e-400', '0e0', '2.5e-1', '1e400',
           'abc', '', '12abc', '0x10', '1_000', 'Inf', 'nan', '0 but true', '1e', '.', '- 1', '1 2']
OTHERS = [('i', v) for v in (0, 1, -1, 2, 3, 7, 10, 2**31, 10**15, 2**53 - 1, 2**53, 2**53 + 1, -(2**53) - 1, 9007199254740990,
                              10**16, 10**16 + 1, -(2**60), 2**62, INT_MAX, INT_MIN)] + \
         [('n', v) for v in (0.0, -0.0, 0.5, 1.5, 3.0, 1000.0, 1e15, 2.0**53 - 1, 2.0**53, 1e16, 2.0**62, 1e19, 1e300, 0.1)]
PASTS = {'fresh': '', 'float first': 'my $t = %s > 0.5;', 'integer first': 'my $t = %s + 0;'}

def perl_value(v):
    if v[0] == 's':
        return "'" + v[1].replace('\\', '\\\\').replace("'", "\\'") + "'"
    return step2.perl_source(v)

def cases():
    strings = [('s', s) for s in STRINGS]
    out = [('neg', a, None) for a in strings + OTHERS]
    for op in step2.OPS:
        for a in strings:
            for b in OTHERS:
                out += [(op, a, b), (op, b, a)]
            for b in strings[::3]:
                out.append((op, a, b))
        # Numbers have a past too (T92): an Int that has been used as a
        # float, a Num that has been used as an integer.
        for a in OTHERS:
            for b in OTHERS:
                out.append((op, a, b))
    return out

def ask_perl(cs):
    """For each case, perl's answer under each past of its string operands."""
    perl = os.environ.get('CURLY_PERL', 'perl')
    # One handler for the whole run, listening only while the operation
    # itself is evaluated: perl compiles a `use warnings` for every case
    # far too slowly, and what the earlier uses warn about is not the point.
    # Each case is a sub of its own: perl looks a variable up by walking
    # back through every `my` of the enclosing scope, and a hundred
    # thousand of them in one scope take minutes to compile.
    lines = [step2.PRELUDE.replace('no warnings;', 'use warnings;'),
             'our ($listening, $warned) = (0, 0); $SIG{__WARN__} = sub { $warned = 1 if $listening };']
    keys = []
    for n, (op, a, b) in enumerate(cs):
        for pa in PASTS:
            for pb in PASTS if b is not None else ['fresh']:
                before = (PASTS[pa] % '$x' if PASTS[pa] else '') + ' ' + (PASTS[pb] % '$y' if PASTS[pb] else '')
                expr = '-$x' if op == 'neg' else f'$x {op} $y'
                rhs = '' if b is None else f' my $y = {perl_value(b)};'
                lines.append(f'sub {{ ($listening, $warned) = (0, 0); my $x = {perl_value(a)};{rhs} {before} $listening = 1; '
                             f'my $r = attempt(sub {{ {expr} }}); say $warned ? "warns" : $r; }}->();')
                keys.append(n)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'strings.pl')
        open(path, 'w').write('\n'.join(lines) + '\n')
        r = subprocess.run([perl, path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[:2000])
    answers = [[] for _ in cs]
    for n, line in zip(keys, r.stdout.split('\n')):
        answers[n].append(line)
    return answers

def agrees(rule, perl):
    """Whether one perl answer is the rule's value, as the docstring has it."""
    if perl.startswith(('dies', 'warns')):
        return False
    kind, text = perl.split(' ', 1)
    if rule[0] == 'i':
        return kind == 'I' and int(text) == rule[1]
    x = rule[1]
    if kind == 'N':
        return text != 'nan' and struct.unpack('>d', bytes.fromhex(text))[0] == x
    return kind == 'I' and abs(x) < 2**53 and int(text) == x

def main():
    cs = cases()
    answers = ask_perl(cs)
    wrong = 0
    counts = {}
    two = 0
    for (op, a, b), perls in zip(cs, answers):
        if len(set(perls)) > 1:
            two += 1
        try:
            r = language3(op, a, b)
            what = 'an Int' if r[0] == 'i' else 'a Num'
            bad = [p for p in perls if not agrees(r, p)]
            if bad:
                wrong += 1
                if wrong <= 25:
                    print(f'WRONG {op} {a} {b}: the rule {shown(r)}; perl, by its past: {sorted(set(perls))}')
        except Fault as f:
            what = f'fault: {f}'
        counts[what] = counts.get(what, 0) + 1
    print(f'{len(cs)} operations on strings and numbers; perl has more than one answer, by its operands\' pasts, for {two}')
    print(f'the proposed rule gives a value perl does not, under some past, on {wrong}')
    for what, n in sorted(counts.items()):
        print(f'    {n:6}  {what}')
    return 1 if wrong else 0

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""t/030 to t/035: the bit operations (D15 to D17). 030 folds bit/and,
bit/or and bit/xor over every pair of the edge values; 031 and 032 fold
bit/shl and bit/shr over the pairs that give a value; 033 to 035 each end
in a fault, so that the fault's message and the exit code are checked: 033 a
boolean argument (not an integer), 034 a shift that overflows, 035 a shift
count out of range (bad shift).

The model is Python's integers, which never overflow and whose &, |, ^ are
the sign-extended two's-complement operations (D15), so (-1 & 7) is 7,
(-8 | 1) is -7 and (-1 ^ 0) is -1. A left shift is a * 2**n, checked
against the 63-bit range after (D16); a right shift is a // 2**n, Python's
floor division, which rounds toward negative infinity, so (-7 // 2) is -4
where (/ -7 2) is -3. A shift count outside 0 to 62 faults `bad shift`,
whatever the value is.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/bits.py --program 030 > t/030-bit-logic.lang
    python3 t/models/bits.py 030 > t/030-bit-logic.expected
    python3 t/models/bits.py --program 031 > t/031-bit-shl.lang
    python3 t/models/bits.py 031 > t/031-bit-shl.expected
    python3 t/models/bits.py --program 032 > t/032-bit-shr.lang
    python3 t/models/bits.py 032 > t/032-bit-shr.expected
    python3 t/models/bits.py --program 033 > t/033-bit-not-int.lang
    python3 t/models/bits.py 033 > t/033-bit-not-int.expected
    python3 t/models/bits.py --program 034 > t/034-bit-overflow.lang
    python3 t/models/bits.py 034 > t/034-bit-overflow.expected
    python3 t/models/bits.py --program 035 > t/035-bit-bad-shift.lang
    python3 t/models/bits.py 035 > t/035-bit-bad-shift.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
P = 1000000007
VALUES = [0, 1, -1, 7, -7, 15, -15, MAX, MIN]
COUNTS = [0, 1, 2, 3, 31, 62]

def mod(a, b):
    """The language's remainder: the dividend's sign (D5)."""
    r = abs(a) % abs(b)
    return r if a >= 0 else -r

def apply(op, a, b):
    """The value, or the fault's message (D15, D16, D17)."""
    if op == 'bit/and':
        return a & b
    if op == 'bit/or':
        return a | b
    if op == 'bit/xor':
        return a ^ b
    if not (0 <= b <= 62):
        return 'bad shift'
    if op == 'bit/shl':
        r = a * (2 ** b)
        return r if MIN <= r <= MAX else 'overflow'
    return a // (2 ** b)

def fold(terms):
    """A balanced tree that adds the terms mod P, so the fold never
    overflows and its depth is O(log n), not the chain clang caps at 256.
    The value mirrors the program: each (+) is reduced mod P, so the value
    is the sum of the terms mod P, taken the way the program takes it."""
    if not terms:
        return '0', 0
    if len(terms) == 1:
        e, v = terms[0]
        return f'(% {e} {P})', mod(v, P)
    mid = len(terms) // 2
    le, lv = fold(terms[:mid])
    re, rv = fold(terms[mid:])
    return f'(% (+ {le} {re}) {P})', mod(lv + rv, P)

def pairs(op):
    """The (a, b) pairs that give a value, for the fold."""
    out = []
    for a in VALUES:
        for b in (COUNTS if op in ('bit/shl', 'bit/shr') else VALUES):
            if isinstance(apply(op, a, b), int):
                out.append((a, b))
    return out

def terms(op):
    return [(f'({op} {a} {b})', apply(op, a, b)) for a, b in pairs(op)]

def program(test):
    if test == '030':
        t = []
        for op in ('bit/and', 'bit/or', 'bit/xor'):
            t += terms(op)
        e, _ = fold(t)
        return '\n'.join([
            '; bit/and, bit/or and bit/xor over every pair of edge values,',
            '; folded into one expression. Expected output and this program',
            '; from t/models/bits.py.',
            e,
        ]) + '\n'
    if test in ('031', '032'):
        op = 'bit/shl' if test == '031' else 'bit/shr'
        e, _ = fold(terms(op))
        return '\n'.join([
            f'; {op} over the pairs that give a value, folded into one',
            '; expression. Expected output and this program from t/models/bits.py.',
            e,
        ]) + '\n'
    if test == '033':
        return '\n'.join([
            '; A boolean argument to a bit operation faults (D15, D17): the',
            '; fault ends the program before anything prints. From t/models/bits.py.',
            '(+ (* 2 3) (bit/and #true 7))',
        ]) + '\n'
    if test == '034':
        return '\n'.join([
            '; A shift that overflows faults (D16, D17), after a value is',
            '; computed. From t/models/bits.py.',
            f'(+ (* 2 3) (bit/shl {MAX} 1))',
        ]) + '\n'
    if test == '035':
        return '\n'.join([
            '; A shift count out of range faults (D16, D17), whatever the',
            '; value is. From t/models/bits.py.',
            '(+ (* 2 3) (bit/shr 7 63))',
        ]) + '\n'

def expected(test):
    if test == '030':
        t = []
        for op in ('bit/and', 'bit/or', 'bit/xor'):
            t += terms(op)
        _, v = fold(t)
        return f'{v}\n'
    if test in ('031', '032'):
        op = 'bit/shl' if test == '031' else 'bit/shr'
        _, v = fold(terms(op))
        return f'{v}\n'
    if test == '033':
        return 'fault: not an integer\nexit: 1\n'
    if test == '034':
        return 'fault: overflow\nexit: 1\n'
    if test == '035':
        return 'fault: bad shift\nexit: 1\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    test = args[0] if args else '030'
    sys.stdout.write(program(test) if '--program' in sys.argv else expected(test))

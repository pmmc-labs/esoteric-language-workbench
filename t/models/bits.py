#!/usr/bin/env python3
"""t/030 to t/040: the five bit operations (D15, D16, D17). Computed from
the definition, not from the runtime: the integers are the mathematical
ones, two's complement of unlimited width, which is what Python's &, |
and ^ do on its own integers, so the three are Python's. A left shift is
a * 2**n with the range checked after (D4, D16); a right shift is
a // 2**n, Python's floor division, which rounds toward negative infinity
(D16), not C's `>>` and not the truncating division of D5. The count is
checked first: outside 0 to 62 is `bad shift` whatever a is (D16). A
boolean is `not an integer` (D15, D17). The model has no booleans; those
two tests are written out, and say so.

030 folds every pair of edge values through and, or and xor, which
always give a value. 031 and 032 fold the shifts that give a value;
033 and up are one fault each, since a fault ends the program (as 011 to
015). The fold reduces each term by a prime, with the
remainder taking the dividend's sign (D5), the one place this model
needs the language's division, so it is written here again from D5.

    python3 t/models/bits.py --program 030 > t/030-bit-logic.lang
    python3 t/models/bits.py 030 > t/030-bit-logic.expected
    python3 t/models/bits.py --program 031 > t/031-bit-shl.lang
    python3 t/models/bits.py 031 > t/031-bit-shl.expected
    python3 t/models/bits.py --program 032 > t/032-bit-shr.lang
    python3 t/models/bits.py 032 > t/032-bit-shr.expected
    python3 t/models/bits.py --program 033 > t/033-shl-overflow.lang
    python3 t/models/bits.py 033 > t/033-shl-overflow.expected
    python3 t/models/bits.py --program 034 > t/034-shl-overflow-min.lang
    python3 t/models/bits.py 034 > t/034-shl-overflow-min.expected
    python3 t/models/bits.py --program 035 > t/035-shl-count-63.lang
    python3 t/models/bits.py 035 > t/035-shl-count-63.expected
    python3 t/models/bits.py --program 036 > t/036-shl-count-neg.lang
    python3 t/models/bits.py 036 > t/036-shl-count-neg.expected
    python3 t/models/bits.py --program 037 > t/037-shr-count-63.lang
    python3 t/models/bits.py 037 > t/037-shr-count-63.expected
    python3 t/models/bits.py --program 038 > t/038-shr-count-neg.lang
    python3 t/models/bits.py 038 > t/038-shr-count-neg.expected
    python3 t/models/bits.py --program 039 > t/039-bit-and-bool.lang
    python3 t/models/bits.py 039 > t/039-bit-and-bool.expected
    python3 t/models/bits.py --program 040 > t/040-shr-count-bool.lang
    python3 t/models/bits.py 040 > t/040-shr-count-bool.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
P = 1000000007
VALUES = [0, 1, -1, 7, -7, 5, -8, MAX, MIN, 3037000499, -3037000500]
# Counts that find the edges of 0 to 62 (D16).
COUNTS = [0, 1, 2, 31, 32, 61, 62]

def trunc_div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def mod(a, b):
    return a - trunc_div(a, b) * b

def logic(op, a, b):
    return {'and': a & b, 'or': a | b, 'xor': a ^ b}[op]

def shift(op, a, n):
    """The value, or the fault's message."""
    if not 0 <= n <= 62:
        return 'bad shift'
    r = a * 2**n if op == 'shl' else a // 2**n
    return r if MIN <= r <= MAX else 'overflow'

def fold(terms):
    """terms: (text, value) pairs, summed mod P as a balanced tree, so the
    nesting is log n deep: clang stops at 256 brackets, and a linear fold
    of 363 terms is past it. A node is (% (+ (% L p) (% R p)) p)."""
    if len(terms) == 1:
        return f'(% {terms[0][0]} {P})', mod(terms[0][1], P)
    mid = len(terms) // 2
    (lt, lv), (rt, rv) = fold(terms[:mid]), fold(terms[mid:])
    return f'(% (+ {lt} {rt}) {P})', mod(lv + rv, P)

def logic_terms():
    return [(f'(bit/{op} {a} {b})', logic(op, a, b)) for op in ('and', 'or', 'xor') for a in VALUES for b in VALUES]

def shift_terms(op):
    out = []
    for a in VALUES:
        for n in COUNTS:
            r = shift(op, a, n)
            if isinstance(r, int):
                out.append((f'(bit/{op} {a} {n})', r))
    return out

# 033 and up: one expression that faults, after one that doesn't. The
# fault's name comes from the definition above, except the booleans.
FAULTS = {
    '033': ('(bit/shl 1 62)', shift('shl', 1, 62), 'the smallest power of two past the range'),
    '034': (f'(bit/shl {MIN} 1)', shift('shl', MIN, 1), 'the smallest integer doubled'),
    '035': ('(bit/shl 0 63)', shift('shl', 0, 63), 'the count is checked even where the result would fit'),
    '036': ('(bit/shl 1 -1)', shift('shl', 1, -1), 'a negative count is a mistake, not the other shift'),
    '037': ('(bit/shr 1 63)', shift('shr', 1, 63), 'shr counts are checked too'),
    '038': ('(bit/shr -1 -1)', shift('shr', -1, -1), 'a negative count, shr'),
    '039': ('(bit/and 1 #true)', 'not an integer', 'a boolean (D15); written by hand, the model has none'),
    '040': ('(bit/shr 8 #false)', 'not an integer', 'a boolean as a count (D15); written by hand'),
}

def program(test):
    if test == '030':
        lines = ['; and, or and xor over every pair of edge values, folded into one',
                 '; expression. Expected output and this program from t/models/bits.py.',
                 fold(logic_terms())[0]]
    elif test in ('031', '032'):
        op = 'shl' if test == '031' else 'shr'
        lines = [f'; bit/{op} over the edge values and counts that give a value, folded.',
                 '; Expected output and this program from t/models/bits.py.',
                 fold(shift_terms(op))[0]]
    else:
        call, _, why = FAULTS[test]
        lines = [f'; {call} faults: {why}. It follows a value, and the fault ends',
                 '; the program before anything prints. From t/models/bits.py.',
                 f'(+ (* 2 3) {call})']
    return '\n'.join(lines) + '\n'

def expected(test):
    if test == '030':
        return f'{fold(logic_terms())[1]}\n'
    if test in ('031', '032'):
        return f'{fold(shift_terms("shl" if test == "031" else "shr"))[1]}\n'
    return f'fault: {FAULTS[test][1]}\nexit: 1\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    test = args[0] if args else '030'
    sys.stdout.write(program(test) if '--program' in sys.argv else expected(test))

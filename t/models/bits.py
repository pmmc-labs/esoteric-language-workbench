#!/usr/bin/env python3
"""t/030 to t/036: the five bit operations (D15, D16) and the faults the
decisions name (D17, and D11 for the booleans).

030: bit/and, bit/or and bit/xor over every pair of the edge values, each
     term folded into one expression as 010 folds the arithmetic.
031: bit/shl over every value and every count 0 to 62 that gives a value.
032: bit/shr over every value and every count 0 to 62.
033: (bit/shl 1 62) faults overflow: 2^62 is past the range (D4, D16).
034: (bit/shl 1 63) faults bad shift: the count is past 62 (D16).
035: (bit/shr 7 -1) faults bad shift: a negative count (D16).
036: (bit/shl #true 1) faults not an integer: a boolean is not an integer
     (D11, D15).

The definitions this computes from, and nothing else:

- bit/and, bit/or, bit/xor are Python's &, | and ^, which are two's
  complement of any width (D15), so a result is the mathematical bit
  operation on the sign-extended values. The model asserts the result is
  in range, since D15 says these never leave it.
- bit/shl a n is a * 2^n, and faults overflow when that is past the range
  (D4, D16).
- bit/shr a n is a divided by 2^n rounded toward negative infinity (D16),
  which is Python's // on integers, not the truncating division of D5.
- A count outside 0 to 62 faults bad shift (D16), and a boolean as an
  argument faults not an integer (D15). Python's bool is a subclass of
  int, so the model looks for a boolean before anything else.

The model reports one fault per call. Where a call could fault two ways
(a boolean as the value and a bad count, say) the decisions don't say which
reports, so no test has one: the model would report the first it checks.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/bits.py --program 030 > t/030-bit-logic.lang
    python3 t/models/bits.py 030 > t/030-bit-logic.expected
    python3 t/models/bits.py --program 031 > t/031-shl.lang
    python3 t/models/bits.py 031 > t/031-shl.expected
    python3 t/models/bits.py --program 032 > t/032-shr.lang
    python3 t/models/bits.py 032 > t/032-shr.expected
    python3 t/models/bits.py --program 033 > t/033-shl-overflow.lang
    python3 t/models/bits.py 033 > t/033-shl-overflow.expected
    python3 t/models/bits.py --program 034 > t/034-shl-bad-shift.lang
    python3 t/models/bits.py 034 > t/034-shl-bad-shift.expected
    python3 t/models/bits.py --program 035 > t/035-shr-bad-shift.lang
    python3 t/models/bits.py 035 > t/035-shr-bad-shift.expected
    python3 t/models/bits.py --program 036 > t/036-not-int.lang
    python3 t/models/bits.py 036 > t/036-not-int.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
PRIME = 1000000007  # the fold reduces by this, so no fold leaves the range
VALUES = [0, 1, -1, 2, -2, 7, -8, 2**31, -(2**31), 2**61, -(2**61), MAX, MIN]
COUNTS = range(63)  # 0 to 62 (D16)
LOGIC = ['bit/and', 'bit/or', 'bit/xor']
SHIFTS = ['bit/shl', 'bit/shr']

class Fault(Exception):
    """A fault, its message as D17 names it in the args."""

def lit(x):
    """A value as the language writes it."""
    if x is True:
        return '#true'
    if x is False:
        return '#false'
    return str(x)

def tdiv(a, b):
    """Division truncating toward zero (D5), for the fold only."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def tmod(a, b):
    """The remainder with the dividend's sign (D5), for the fold only."""
    return a - tdiv(a, b) * b

def op(name, a, b):
    """The value of (name a b), or raise Fault with the message."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise Fault('not an integer')
    if name == 'bit/and':
        r = a & b
    elif name == 'bit/or':
        r = a | b
    elif name == 'bit/xor':
        r = a ^ b
    elif name in SHIFTS:
        if not 0 <= b <= 62:
            raise Fault('bad shift')
        if name == 'bit/shl':
            r = a * 2**b
        else:
            return a // 2**b  # rounded toward negative infinity, and in range
    else:
        raise ValueError(name)
    if name in LOGIC:
        assert MIN <= r <= MAX, (name, a, b)  # D15: these never leave the range
        return r
    if not MIN <= r <= MAX:
        raise Fault('overflow')
    return r

def pairs(name):
    """(a, b, value) for every pair that gives a value, in order."""
    out = []
    bs = COUNTS if name in SHIFTS else VALUES
    for a in VALUES:
        for b in bs:
            try:
                out.append((a, b, op(name, a, b)))
            except Fault:
                pass
    return out

def fold(terms):
    """The terms, each reduced mod PRIME before it's added, folded into one
    expression: (% (+ acc (% t p)) p). Returns the text and the value."""
    text, v = terms[0]
    acc_text = f'(% {text} {PRIME})'
    acc = tmod(v, PRIME)
    for text, v in terms[1:]:
        acc_text = f'(% (+ {acc_text} (% {text} {PRIME})) {PRIME})'
        acc = tmod(acc + tmod(v, PRIME), PRIME)
    return acc_text, acc

def folded(names):
    terms = []
    for name in names:
        for a, b, v in pairs(name):
            terms.append((f'({name} {lit(a)} {lit(b)})', v))
    return fold(terms)

FAULT_TESTS = {
    '033': ('bit/shl', 1, 62),
    '034': ('bit/shl', 1, 63),
    '035': ('bit/shr', 7, -1),
    '036': ('bit/shl', True, 1),
}

def fault_of(test):
    name, a, b = FAULT_TESTS[test]
    try:
        op(name, a, b)
    except Fault as f:
        return name, a, b, str(f.args[0])
    raise AssertionError(f'{test}: ({name} {lit(a)} {lit(b)}) does not fault')

def program(test):
    if test == '030':
        text, _ = folded(LOGIC)
        lines = [
            '; Every bit operation over every pair of edge values, folded into one',
            '; expression. Expected output and this program from t/models/bits.py.',
            text,
        ]
    elif test == '031':
        text, _ = folded(['bit/shl'])
        lines = [
            '; bit/shl over every edge value and every count 0 to 62 that gives a',
            '; value, folded into one expression. From t/models/bits.py.',
            text,
        ]
    elif test == '032':
        text, _ = folded(['bit/shr'])
        lines = [
            '; bit/shr over every edge value and every count 0 to 62, folded into',
            '; one expression. From t/models/bits.py.',
            text,
        ]
    else:
        name, a, b, _ = fault_of(test)
        lines = [
            f'; ({name} {lit(a)} {lit(b)}) faults, after a value is computed: the fault',
            '; ends the program before anything prints. From t/models/bits.py.',
            f'(+ (* 2 3) ({name} {lit(a)} {lit(b)}))',
        ]
    return '\n'.join(lines) + '\n'

def expected(test):
    if test == '030':
        return f'{folded(LOGIC)[1]}\n'
    if test == '031':
        return f'{folded(["bit/shl"])[1]}\n'
    if test == '032':
        return f'{folded(["bit/shr"])[1]}\n'
    _, _, _, message = fault_of(test)
    return f'fault: {message}\nexit: 1\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    if not args:
        sys.exit(__doc__)
    test = args[0]
    sys.stdout.write(program(test) if '--program' in sys.argv else expected(test))

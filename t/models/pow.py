#!/usr/bin/env python3
"""t/040 to t/045: exponentiation, (** a b) (D18, D19), and the faults the
decisions name (D17, D19, and D11 for the booleans).

040: ** over every edge base and a spread of exponents that give a value,
     folded into one expression (fold below; bits.py folds the same way, as
     a balanced tree, for clang's bracket limit).
041: (** 2 62) faults overflow: 2^62 is past the range (D4).
042: (** 2 4611686018427387903) faults overflow, and quickly: the exponent
     is the largest integer, so a runtime that multiplies b times never ends.
043: (** 2 -1) faults bad exponent: a negative exponent (D19).
044: (** #true 2) faults not an integer (D11).
045: (** 1 -1) faults bad exponent, though 1^-1 is 1: the rule is on the
     exponent, not on the result (D19).

The definitions this computes from, and nothing else:

- a ** b for b >= 0 is the product of b copies of a, with a ** 0 = 1 for
  every a including 0 (D19). Python's ** on integers is exactly that, and
  the model then applies the range (D4): a result outside it faults
  overflow.
- A negative b faults bad exponent (D19), whatever a is.
- A boolean as either argument faults not an integer (D11). Python's bool
  is a subclass of int, so the model looks for a boolean before anything
  else.
- One shortcut, which is arithmetic and not an implementation detail: for
  |a| >= 2 and b >= 63, |a ** b| >= 2^63, past the range, so the model
  reports overflow without computing a power that may have 2^62 digits. The
  shortcut is asserted against the real power on the exponents where both
  are cheap (b up to 200).

The model reports one fault per call. Where a call could fault two ways (a
boolean and a negative exponent, say) the decisions don't say which
reports, so no test has one.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/pow.py --program 040 > t/040-pow.lang
    python3 t/models/pow.py 040 > t/040-pow.expected
    python3 t/models/pow.py --program 041 > t/041-pow-overflow.lang
    python3 t/models/pow.py 041 > t/041-pow-overflow.expected
    python3 t/models/pow.py --program 042 > t/042-pow-overflow-huge.lang
    python3 t/models/pow.py 042 > t/042-pow-overflow-huge.expected
    python3 t/models/pow.py --program 043 > t/043-pow-bad-exponent.lang
    python3 t/models/pow.py 043 > t/043-pow-bad-exponent.expected
    python3 t/models/pow.py --program 044 > t/044-pow-not-int.lang
    python3 t/models/pow.py 044 > t/044-pow-not-int.expected
    python3 t/models/pow.py --program 045 > t/045-pow-bad-exponent-one.lang
    python3 t/models/pow.py 045 > t/045-pow-bad-exponent-one.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
PRIME = 1000000007  # the fold reduces by this, so no fold leaves the range
BASES = [0, 1, -1, 2, -2, 3, -3, 7, -8, 10, 2**31, -(2**31), 2**61, -(2**61), MAX, MIN]
# Exponents that find the edges: 0 and 1, the small ones, where a power of 2
# or 3 or 10 crosses the range (62, 63), and the largest integer, where only
# 0, 1 and -1 give a value.
EXPONENTS = [0, 1, 2, 3, 4, 5, 10, 20, 31, 32, 38, 39, 61, 62, 63, 64, MAX - 1, MAX]

class Fault(Exception):
    """A fault, its message as D17 and D19 name it in the args."""

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

def power(a, b):
    """a ** b for b >= 0, in range or raising Fault overflow."""
    if abs(a) >= 2 and b >= 63:
        if b <= 200:
            assert not MIN <= a**b <= MAX, (a, b)
        raise Fault('overflow')
    r = a**b
    if not MIN <= r <= MAX:
        raise Fault('overflow')
    return r

def op(a, b):
    """The value of (** a b), or raise Fault with the message."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise Fault('not an integer')
    if b < 0:
        raise Fault('bad exponent')
    return power(a, b)

def pairs():
    """(a, b, value) for every pair that gives a value, in order."""
    out = []
    for a in BASES:
        for b in EXPONENTS:
            try:
                out.append((a, b, op(a, b)))
            except Fault:
                pass
    return out

def fold(terms):
    """The terms, each reduced mod PRIME before anything is added, summed
    pairwise into one expression: (% (+ L R) p) at each join, so nothing in
    the sum leaves the range. A balanced tree and not a chain, since a chain
    nests one bracket per term and clang stops at 256. Returns the text and
    the value."""
    level = [(f'(% {text} {PRIME})', tmod(v, PRIME)) for text, v in terms]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            (lt, lv), (rt, rv) = level[i], level[i + 1]
            nxt.append((f'(% (+ {lt} {rt}) {PRIME})', tmod(lv + rv, PRIME)))
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]

def folded():
    return fold([(f'(** {lit(a)} {lit(b)})', v) for a, b, v in pairs()])

FAULT_TESTS = {
    '041': (2, 62),
    '042': (2, MAX),
    '043': (2, -1),
    '044': (True, 2),
    '045': (1, -1),
}

def fault_of(test):
    a, b = FAULT_TESTS[test]
    try:
        op(a, b)
    except Fault as f:
        return a, b, str(f.args[0])
    raise AssertionError(f'{test}: (** {lit(a)} {lit(b)}) does not fault')

def program(test):
    if test == '040':
        lines = [
            '; ** over every edge base and a spread of exponents that give a value,',
            '; folded into one expression. Expected output and this program from',
            '; t/models/pow.py.',
            folded()[0],
        ]
    else:
        a, b, _ = fault_of(test)
        lines = [
            f'; (** {lit(a)} {lit(b)}) faults, after a value is computed: the fault',
            '; ends the program before anything prints. From t/models/pow.py.',
            f'(+ (* 2 3) (** {lit(a)} {lit(b)}))',
        ]
    return '\n'.join(lines) + '\n'

def expected(test):
    if test == '040':
        return f'{folded()[1]}\n'
    _, _, message = fault_of(test)
    return f'fault: {message}\nexit: 1\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    if not args:
        sys.exit(__doc__)
    test = args[0]
    sys.stdout.write(program(test) if '--program' in sys.argv else expected(test))

#!/usr/bin/env python3
"""t/040 to t/043: exponentiation (D18), with the faults it can give (D4,
D11, D14, D17 and D19).

040: (** a b) over every edge value and every exponent in EXPONENTS that
     gives a value, folded into one expression. 10^18 + 7 is past anything
     a loop could run, so the program only finishes for bases 0, 1 and -1
     if the power is computed by squaring, which is what the runtime does.
041: (** 2 62) faults overflow: 2^62 is one past the range (D4).
042: (** 2 -1) faults bad exponent: a negative exponent (D19).
043: (** #true 2) faults not an integer: a boolean is not an integer (D11, D14).

The definition this computes from, and nothing else:

- a ** b for b >= 0 is the power of the mathematical integers, exact
  (D18). Python's ** on integers is that power.
- A result out of the 63-bit range faults overflow (D4). The model
  computes the power and then checks the range, as arith.py does, with one
  shortcut: when |a| >= 2 and b >= 63 the power is past the range in
  magnitude (2^63 is past 2^62 - 1), so the model says overflow without
  building a number of as many bits as the power has.
- 0 to the power 0 is 1 (D19): the empty product, written here rather than
  left to Python's convention.
- A negative exponent faults bad exponent (D19), whatever the base.
- A boolean as either argument faults not an integer (D11, D14). The model
  looks for a boolean first, since Python's bool is a subclass of int.

The model reports one fault per call. A call that could fault two ways
(a boolean base and a negative exponent, say) isn't in any test, since the
decisions don't say which reports.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/pow.py --program 040 > t/040-pow.lang
    python3 t/models/pow.py 040 > t/040-pow.expected
    python3 t/models/pow.py --program 041 > t/041-pow-overflow.lang
    python3 t/models/pow.py 041 > t/041-pow-overflow.expected
    python3 t/models/pow.py --program 042 > t/042-pow-bad-exponent.lang
    python3 t/models/pow.py 042 > t/042-pow-bad-exponent.expected
    python3 t/models/pow.py --program 043 > t/043-pow-not-int.lang
    python3 t/models/pow.py 043 > t/043-pow-not-int.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
PRIME = 1000000007  # the fold reduces by this, so no fold leaves the range
VALUES = [0, 1, -1, 2, -2, 3, -3, 7, -7, 2**31, -(2**31), MAX, MIN]
EXPONENTS = [0, 1, 2, 3, 7, 31, 32, 61, 62, 63, 64, 1000, 10**18 + 7]

class Fault(Exception):
    """A fault, its message as D17 and D19 name it in the args."""

def lit(x):
    """A value as the language writes it."""
    if x is True:
        return '#true'
    if x is False:
        return '#false'
    return str(x)

def tmod(a, b):
    """The remainder with the dividend's sign (D5), for the fold only."""
    q = abs(a) // abs(b)
    q = q if (a < 0) == (b < 0) else -q
    return a - q * b

def op(a, b):
    """The value of (** a b), or raise Fault with the message."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise Fault('not an integer')
    if b < 0:
        raise Fault('bad exponent')
    if b == 0:
        return 1  # D19: the empty product, whatever the base
    if abs(a) >= 2 and b >= 63:
        raise Fault('overflow')  # past the range by magnitude; see the docstring
    r = a ** b
    if not MIN <= r <= MAX:
        raise Fault('overflow')
    return r

def pairs():
    """(a, b, value) for every pair that gives a value, in order."""
    out = []
    for a in VALUES:
        for b in EXPONENTS:
            try:
                out.append((a, b, op(a, b)))
            except Fault:
                pass
    return out

def fold(terms):
    """The terms, each reduced mod PRIME before anything is added, then
    summed pairwise: (% (+ L R) p) at each join, so nothing in the sum
    leaves the range. A balanced tree and not a chain, since a chain nests
    a bracket per term and clang stops at 256. Returns the text and the
    value, the value computed here from the same tree."""
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
    '042': (2, -1),
    '043': (True, 2),
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
        text, _ = folded()
        lines = [
            '; (** a b) over every edge value and every exponent that gives a value,',
            '; folded into one expression. Expected output and this program from',
            '; t/models/pow.py.',
            text,
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

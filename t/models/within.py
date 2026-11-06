#!/usr/bin/env python3
"""t/050-within-every-op: every operator and `if`, each inside a budget of
exactly one, over the operand pairs that give a value (D20 to D26).

A term is (within 1 (OP a b)) with both operands literals. A literal costs
nothing and `within` costs nothing (D23), so the term performs one
operation: the budget of one is exactly spent, and none of the seventeen
operators nor `if` faults `budget spent`. A cost is one however large the
work (D23): (** 2 62) is not here, being past the range, but (** 1 MAX)
is, and so is (bit/shl 1 62) beside (bit/shl 1 0). The `if` terms are
(within 1 (if #true a b)) and (within 1 (if #false a b)): a literal test
costs nothing, so the `if` is the one operation and the branch not taken
costs nothing either (D23).

The fold's own operations (the % and + that sum the terms) are outside
every `within`, so nothing counts them: a program without a budget around
an operation is what it was (D24). A comparison's boolean is counted by an
`if` outside the budget, (if (within 1 (< a b)) 1 0), as compare.py counts
them, so no boolean has to be a term of the sum.

The model computes each value from its decision and nothing else:

- + - * and the range: Python's integers, then the range (D4).
- / and %: truncating toward zero, the remainder with the dividend's sign
  (D5), by tdiv and tmod below, not Python's // and %.
- < <= > >=: Python's comparison on the two integers (D12). == and !=: equal
  when the two are the same value of the same type, and values of different
  types are unequal (D12). Python's True == 1, so the model compares types
  first.
- bit/and bit/or bit/xor: Python's &, | and ^ on integers, which are the
  mathematical ones in two's complement (D15). bit/shl is a times 2^n, bit/shr
  is a divided by 2^n rounded toward negative infinity (D16), which is
  Python's // by a positive power; the count is 0 to 62 (D16).
- **: Python's ** for b >= 0, with the range applied after (D19). The model
  keeps only pairs that give a value, and a base of absolute value 2 or more
  with an exponent of 63 or more is left out without computing the power.
- if: the branch the test selects (D13).

Only the pairs that give a value are terms; the faults have tests of their
own (011 to 015, 033 to 036 and 040 to 045), and the budget's are 052, 055,
057, 058 and 061, by hand.

Each term is reduced mod PRIME before it is added, and the sum is a balanced
tree, as pow.py's is, so no part of the fold leaves the range.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/within.py --program > t/050-within-every-op.lang
    python3 t/models/within.py > t/050-within-every-op.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
PRIME = 1000000007
VALUES = [0, 1, -1, 7, -7, 3037000499, -3037000500, MAX, MIN]
COUNTS = [0, 1, 2, 31, 61, 62, 63, -1]
BASES = [0, 1, -1, 2, -2, 3, -3, MAX, MIN]
EXPONENTS = [0, 1, 2, 3, 62, 63, MAX]
IF_VALUES = [0, 1, -7, MAX, MIN]

def lit(x):
    """A value as the language writes it."""
    if x is True:
        return '#true'
    if x is False:
        return '#false'
    return str(x)

def isint(x):
    return not isinstance(x, bool)

class Fault(Exception):
    pass

def tdiv(a, b):
    """Division truncating toward zero (D5)."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def tmod(a, b):
    """The remainder with the dividend's sign (D5)."""
    return a - tdiv(a, b) * b

def inrange(r):
    if not MIN <= r <= MAX:
        raise Fault('overflow')
    return r

def apply(op, a, b):
    """The value of (op a b) on two values, or raise Fault. Only the cases a
    term uses are asked for; a boolean to an operator that wants integers
    faults, which no term has."""
    if op in ('==', '!='):
        same = type(a) is type(b) and a == b
        return same if op == '==' else not same
    if not (isint(a) and isint(b)):
        raise Fault('not an integer')
    if op == '+': return inrange(a + b)
    if op == '-': return inrange(a - b)
    if op == '*': return inrange(a * b)
    if op == '/':
        if b == 0: raise Fault('division by zero')
        return inrange(tdiv(a, b))
    if op == '%':
        if b == 0: raise Fault('division by zero')
        return tmod(a, b)
    if op == '<': return a < b
    if op == '<=': return a <= b
    if op == '>': return a > b
    if op == '>=': return a >= b
    if op == 'bit/and': return a & b
    if op == 'bit/or': return a | b
    if op == 'bit/xor': return a ^ b
    if op in ('bit/shl', 'bit/shr'):
        if not 0 <= b <= 62: raise Fault('bad shift')
        return inrange(a * 2**b) if op == 'bit/shl' else a // 2**b
    if op == '**':
        if b < 0: raise Fault('bad exponent')
        if abs(a) >= 2 and b >= 63: raise Fault('overflow')
        return inrange(a**b)
    raise AssertionError(op)

ARITH = ['+', '-', '*', '/', '%', 'bit/and', 'bit/or', 'bit/xor']
ORDERINGS = ['<', '<=', '>', '>=']
EQUALITIES = ['==', '!=']

def operand_pairs(op):
    if op in ('bit/shl', 'bit/shr'):
        return [(a, n) for a in VALUES for n in COUNTS]
    if op == '**':
        return [(a, b) for a in BASES for b in EXPONENTS]
    if op in EQUALITIES:
        every = VALUES + [True, False]
        return [(a, b) for a in every for b in every]
    return [(a, b) for a in VALUES for b in VALUES]

def terms():
    """(text, value) for every term, in order."""
    out = []
    for op in ARITH + ORDERINGS + EQUALITIES + ['bit/shl', 'bit/shr', '**']:
        for a, b in operand_pairs(op):
            try:
                v = apply(op, a, b)
            except Fault:
                continue
            call = f'(within 1 ({op} {lit(a)} {lit(b)}))'
            if isinstance(v, bool):
                out.append((f'(if {call} 1 0)', 1 if v else 0))
            else:
                out.append((call, v))
    for test in (True, False):
        for a in IF_VALUES:
            for b in IF_VALUES:
                out.append((f'(within 1 (if {lit(test)} {lit(a)} {lit(b)}))', a if test else b))
    # An if that gives a boolean, counted by an if outside the budget.
    for test in (True, False):
        for a in (True, False):
            for b in (True, False):
                v = a if test else b
                out.append((f'(if (within 1 (if {lit(test)} {lit(a)} {lit(b)})) 1 0)', 1 if v else 0))
    return out

def fold(ts):
    """Sum the terms as a balanced tree of (% (+ L R) PRIME), each term first
    reduced mod PRIME. Returns the text and the value."""
    level = [(f'(% {text} {PRIME})', tmod(v, PRIME)) for text, v in ts]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            (lt, lv), (rt, rv) = level[i], level[i + 1]
            nxt.append((f'(% (+ {lt} {rt}) {PRIME})', tmod(lv + rv, PRIME)))
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]

def program():
    return '\n'.join([
        '; Every operator and `if`, each inside a budget of exactly one, over the',
        '; operand pairs that give a value; a comparison counted by an `if` outside',
        '; the budget; folded into one expression. Expected output and this',
        '; program from t/models/within.py.',
        fold(terms())[0],
    ]) + '\n'

def expected():
    return f'{fold(terms())[1]}\n'

if __name__ == '__main__':
    sys.stdout.write(program() if '--program' in sys.argv else expected())

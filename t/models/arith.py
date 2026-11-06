#!/usr/bin/env python3
"""Step 1's golden tests, 050 to 065: the four operators and their faults,
from the decisions (D20 to D28), not from codegen.ts or rt.c.

Each test is a program held here as a tree, written out as the `.lang`
text, and evaluated with Python's unbounded integers: the exact result
of each operation is computed, and then the 63-bit range of D23 is
applied to it. So an overflow is found by the definition (is the true
value in [-2^62, 2^62 - 1]?), whatever a 64-bit machine would wrap it to
(D26). Division truncates toward zero (D24): Python's `//` floors, so it
is used only on magnitudes, and the sign is put back. A zero divisor is
`division by zero` (D24); `-2^62 / -1` is out of range, so an overflow
(D25). Operands are evaluated left to right, and an operator's own fault
comes after both of its operands' (D27). Nothing is folded at compile
time (D28): every fault here is a run-time event, so a test's expected
output is the value and a newline, or `fault: MESSAGE` and `exit: 1`
(D3; stdout and stderr together, as t/run.sh compares them).

    python3 t/models/arith.py --program 050 > t/050-add.lang
    python3 t/models/arith.py 050 > t/050-add.expected
    python3 t/models/arith.py --program 051 > t/051-sub.lang
    python3 t/models/arith.py 051 > t/051-sub.expected
    python3 t/models/arith.py --program 052 > t/052-mul.lang
    python3 t/models/arith.py 052 > t/052-mul.expected
    python3 t/models/arith.py --program 053 > t/053-nested.lang
    python3 t/models/arith.py 053 > t/053-nested.expected
    python3 t/models/arith.py --program 054 > t/054-div-truncates.lang
    python3 t/models/arith.py 054 > t/054-div-truncates.expected
    python3 t/models/arith.py --program 055 > t/055-div-negative-divisor.lang
    python3 t/models/arith.py 055 > t/055-div-negative-divisor.expected
    python3 t/models/arith.py --program 056 > t/056-in-range-edge.lang
    python3 t/models/arith.py 056 > t/056-in-range-edge.expected
    python3 t/models/arith.py --program 057 > t/057-add-overflow.lang
    python3 t/models/arith.py 057 > t/057-add-overflow.expected
    python3 t/models/arith.py --program 058 > t/058-sub-overflow.lang
    python3 t/models/arith.py 058 > t/058-sub-overflow.expected
    python3 t/models/arith.py --program 059 > t/059-mul-wraps.lang
    python3 t/models/arith.py 059 > t/059-mul-wraps.expected
    python3 t/models/arith.py --program 060 > t/060-mul-overflow.lang
    python3 t/models/arith.py 060 > t/060-mul-overflow.expected
    python3 t/models/arith.py --program 061 > t/061-div-zero.lang
    python3 t/models/arith.py 061 > t/061-div-zero.expected
    python3 t/models/arith.py --program 062 > t/062-div-overflow.lang
    python3 t/models/arith.py 062 > t/062-div-overflow.expected
    python3 t/models/arith.py --program 063 > t/063-left-fault-first.lang
    python3 t/models/arith.py 063 > t/063-left-fault-first.expected
    python3 t/models/arith.py --program 064 > t/064-operand-fault-first.lang
    python3 t/models/arith.py 064 > t/064-operand-fault-first.expected
    python3 t/models/arith.py --program 065 > t/065-left-overflow-first.lang
    python3 t/models/arith.py 065 > t/065-left-overflow-first.expected
"""

import sys

# D23: the range of a value, the one the literals have (step 0).
LO = -(2 ** 62)
HI = 2 ** 62 - 1

class Fault(Exception):
    pass

def checked(n):
    """D23: a result outside the range is a fault, whatever its size."""
    if not LO <= n <= HI:
        raise Fault('integer overflow')
    return n

def quotient(a, b):
    """D24: truncate toward zero. D25: the quotient is range-checked like
    any other result, and only after the zero check."""
    if b == 0:
        raise Fault('division by zero')
    q = abs(a) // abs(b)
    return checked(-q if (a < 0) != (b < 0) else q)

OPS = {
    '+': lambda a, b: checked(a + b),
    '-': lambda a, b: checked(a - b),
    '*': lambda a, b: checked(a * b),
    '/': quotient,
}

def evaluate(e):
    """D20: a form is (op a b), a nested form an operand. D27: the left
    operand, then the right, then the operator; the first fault wins,
    which raising gives."""
    if isinstance(e, int):
        # A literal past the range is a compile error (D21), which a
        # golden test can't hold (D4): the model refuses to write one.
        assert LO <= e <= HI, f'literal out of range: {e}'
        return e
    op, a, b = e
    left = evaluate(a)
    right = evaluate(b)
    return OPS[op](left, right)

def text(e):
    return '(' + ' '.join(map(text, e)) + ')' if isinstance(e, tuple) else str(e)

MAX, MIN = HI, LO

# number: (name, what it checks, the decisions, the program)
TESTS = {
    '050': ('add', 'two plus three', 'D20', ('+', 2, 3)),
    '051': ('sub', 'a difference below zero', 'D20', ('-', 2, 7)),
    '052': ('mul', 'a negative operand', 'D20', ('*', -3, 4)),
    '053': ('nested', 'a form as an operand', 'D20', ('*', ('+', 1, 2), ('-', 10, 4))),
    '054': ('div-truncates', 'a negative dividend truncates toward zero, not down', 'D24', ('/', -7, 2)),
    '055': ('div-negative-divisor', 'a negative divisor truncates toward zero, not down', 'D24', ('/', 7, -2)),
    '056': ('in-range-edge', 'a sum that reaches the largest integer and no further', 'D23', ('+', MAX - 1, 1)),
    '057': ('add-overflow', 'one past the largest integer', 'D23', ('+', MAX, 1)),
    '058': ('sub-overflow', 'one below the smallest integer', 'D23', ('-', MIN, 1)),
    '059': ('mul-wraps', '2^32 * 2^32 is 2^64, which 64 bits wrap to 0', 'D23, D26', ('*', 2 ** 32, 2 ** 32)),
    '060': ('mul-overflow', 'negating the smallest integer', 'D23, D26', ('*', -1, MIN)),
    '061': ('div-zero', 'a zero divisor', 'D24', ('/', 1, 0)),
    '062': ('div-overflow', 'the one quotient out of range', 'D25', ('/', MIN, -1)),
    '063': ('left-fault-first', 'the left operand faults before the right', 'D27', ('+', ('/', 1, 0), ('+', MAX, 1))),
    '064': ('operand-fault-first', "an operand's fault before its operator's", 'D27', ('+', MAX, ('/', 1, 0))),
    '065': ('left-overflow-first', 'the left operand faults before the right', 'D27', ('+', ('+', MAX, 1), ('/', 1, 0))),
}

def program(n):
    name, what, decisions, e = TESTS[n]
    return (f'; Step 1 ({decisions}): {what}.\n'
            f'; The program and its expected output are from t/models/arith.py.\n'
            f'{text(e)}\n')

def expected(n):
    try:
        return f'{evaluate(TESTS[n][3])}\n'
    except Fault as f:
        return f'fault: {f}\nexit: 1\n'

def main(argv):
    if len(argv) == 2 and argv[0] == '--program' and argv[1] in TESTS:
        sys.stdout.write(program(argv[1]))
    elif len(argv) == 1 and argv[0] in TESTS:
        sys.stdout.write(expected(argv[0]))
    else:
        sys.exit('usage: arith.py [--program] NNN')

if __name__ == '__main__':
    main(sys.argv[1:])

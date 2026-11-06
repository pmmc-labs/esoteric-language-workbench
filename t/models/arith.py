#!/usr/bin/env python3
"""t/010-arith: the five operators on 63-bit integers, nested, over the
values that find the edges: zero, one, minus one, the smallest and largest
integers, and a few that multiply past the range. Each test is a program
of its own, since a fault ends the program: 010 is the pairs that give a
value, in one nested expression per operator, and 011 to 015 each end in
a fault (overflow by +, -, * and /, and division by zero), so that
the fault's message and the exit code are checked too.

The model is Python's integers, which never overflow, with the range
checked after (D4), and division truncating toward zero with the
remainder taking the dividend's sign (D5), which Python's // and % don't
do, hence the two functions below.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/arith.py --program 010 > t/010-arith.lang
    python3 t/models/arith.py 010 > t/010-arith.expected
    python3 t/models/arith.py --program 011 > t/011-overflow-add.lang
    python3 t/models/arith.py 011 > t/011-overflow-add.expected
    python3 t/models/arith.py --program 012 > t/012-overflow-sub.lang
    python3 t/models/arith.py 012 > t/012-overflow-sub.expected
    python3 t/models/arith.py --program 013 > t/013-overflow-mul.lang
    python3 t/models/arith.py 013 > t/013-overflow-mul.expected
    python3 t/models/arith.py --program 014 > t/014-overflow-div.lang
    python3 t/models/arith.py 014 > t/014-overflow-div.expected
    python3 t/models/arith.py --program 015 > t/015-div-zero.lang
    python3 t/models/arith.py 015 > t/015-div-zero.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1
VALUES = [0, 1, -1, 7, -7, 3037000499, -3037000500, MAX, MIN]
OPS = ['+', '-', '*', '/', '%']

def div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def mod(a, b):
    return a - div(a, b) * b

def apply(op, a, b):
    """The value, or the fault's message."""
    if op in '/%' and b == 0:
        return 'division by zero'
    r = {'+': a + b, '-': a - b, '*': a * b, '/': div, '%': mod}[op]
    if callable(r):
        r = r(a, b)
    return r if MIN <= r <= MAX else 'overflow'

# 010: for each operator, every pair that gives a value, folded into one
# expression, each term reduced mod a prime before it's added so nothing
# in the fold overflows: (% (+ acc (% term p)) p). The first term is
# reduced on its own below.
def pairs(op):
    return [(a, b) for a in VALUES for b in VALUES if isinstance(apply(op, a, b), int)]

def expr(op):
    terms = [f'({op} {a} {b})' for a, b in pairs(op)]
    acc = f'(% {terms[0]} 1000000007)'
    for t in terms[1:]:
        acc = f'(% (+ {acc} (% {t} 1000000007)) 1000000007)'
    return acc

def value(op):
    acc = mod(apply(op, *pairs(op)[0]), 1000000007)
    for a, b in pairs(op)[1:]:
        acc = mod(acc + mod(apply(op, a, b), 1000000007), 1000000007)
    return acc

# 011 to 015: one expression that faults, after some that don't.
FAULTS = {
    '011': ('+', MAX, 1), '012': ('-', MIN, 1), '013': ('*', 3037000500, 3037000500),
    '014': ('/', MIN, -1), '015': ('%', 5, 0),
}

def program(test):
    if test == '010':
        # One nested expression per operator, folded with + and % so the
        # sum stays in range; the fold itself is checked by the model.
        acc = f'(% {expr(OPS[0])} 1000000007)'
        for op in OPS[1:]:
            acc = f'(% (+ {acc} (% {expr(op)} 1000000007)) 1000000007)'
        lines = [
            '; Every operator over every pair of edge values that gives a value,',
            '; folded into one expression. Expected output and this program from',
            '; t/models/arith.py.',
            acc,
        ]
    else:
        op, a, b = FAULTS[test]
        lines = [
            f'; ({op} {a} {b}) faults, after a value is computed: the fault ends the',
            '; program before anything prints. From t/models/arith.py.',
            f'(+ (* 2 3) ({op} {a} {b}))',
        ]
    return '\n'.join(lines) + '\n'

def expected(test):
    if test == '010':
        acc = mod(value(OPS[0]), 1000000007)
        for op in OPS[1:]:
            acc = mod(acc + mod(value(op), 1000000007), 1000000007)
        return f'{acc}\n'
    op, a, b = FAULTS[test]
    return f'fault: {apply(op, a, b)}\nexit: 1\n'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    test = args[0] if args else '010'
    sys.stdout.write(program(test) if '--program' in sys.argv else expected(test))

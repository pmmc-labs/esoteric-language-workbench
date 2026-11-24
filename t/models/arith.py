#!/usr/bin/env python3
"""t/010 to t/026: integer arithmetic (step 1; D23, the Int half).

The definition, which is all this file knows of the language: an Int is
a whole number from -2^63 to 2^63 - 1. `+`, `-`, `*` and unary minus give
the exact answer, or fault `integer overflow` when it isn't an Int. `%`
gives the remainder with the sign of its right operand (-7 % 3 is 2,
7 % -3 is -2), or faults `modulus by zero`. A fault stops the program:
what it had printed, then `fault: MESSAGE at FILE line N.` on stderr, N
the line its statement starts on, and exit status 1.

The model is Python's integers, which don't overflow, with the range
checked after each operation; and Python's `%`, which is the same
remainder. Nothing here is taken from the compiler or from perl. perl is
the second derivation: t/checks.py oracle runs every program this writes
under perl 5.42 and holds each .expected of 010 to 014 to what perl
prints, and each fault test's output to the start of it. Where this model
and perl disagree, neither file is patched: it is a finding about D23.

010 to 013 are every pair of the edge values under one operator each, a
line a pair, wherever the answer is an Int; 014 is each value negated. A
test an operator, and not one test of them all, because a C compiler
slows down more than in proportion over one long run of statements (gcc
took 36 seconds over all 10,592 lines at once). A fault ends a program,
so each of 015 to 026 is a program of its own that faults once, at an
edge: the line before the fault is the nearest expression that still fits.

Every line is written `say(EXPR);`, because an expression that starts
with a bracket after a bare `say` is read by perl as say's whole argument
list (T25). There are no negative literals: -5 is `(-5)`, a minus applied
to 5, and -2^63 is `(-9223372036854775807 - 1)`.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/arith.py --program 010 > t/010-add.pl
    python3 t/models/arith.py 010 > t/010-add.expected
    python3 t/models/arith.py --program 011 > t/011-sub.pl
    python3 t/models/arith.py 011 > t/011-sub.expected
    python3 t/models/arith.py --program 012 > t/012-mul.pl
    python3 t/models/arith.py 012 > t/012-mul.expected
    python3 t/models/arith.py --program 013 > t/013-mod.pl
    python3 t/models/arith.py 013 > t/013-mod.expected
    python3 t/models/arith.py --program 014 > t/014-neg.pl
    python3 t/models/arith.py 014 > t/014-neg.expected
    python3 t/models/arith.py --program 015 > t/015-overflow-add.pl
    python3 t/models/arith.py 015 > t/015-overflow-add.expected
    python3 t/models/arith.py --program 016 > t/016-overflow-add-down.pl
    python3 t/models/arith.py 016 > t/016-overflow-add-down.expected
    python3 t/models/arith.py --program 017 > t/017-overflow-sub.pl
    python3 t/models/arith.py 017 > t/017-overflow-sub.expected
    python3 t/models/arith.py --program 018 > t/018-overflow-sub-up.pl
    python3 t/models/arith.py 018 > t/018-overflow-sub-up.expected
    python3 t/models/arith.py --program 019 > t/019-overflow-mul.pl
    python3 t/models/arith.py 019 > t/019-overflow-mul.expected
    python3 t/models/arith.py --program 020 > t/020-overflow-mul-down.pl
    python3 t/models/arith.py 020 > t/020-overflow-mul-down.expected
    python3 t/models/arith.py --program 021 > t/021-overflow-mul-min.pl
    python3 t/models/arith.py 021 > t/021-overflow-mul-min.expected
    python3 t/models/arith.py --program 022 > t/022-overflow-mul-far.pl
    python3 t/models/arith.py 022 > t/022-overflow-mul-far.expected
    python3 t/models/arith.py --program 023 > t/023-overflow-neg.pl
    python3 t/models/arith.py 023 > t/023-overflow-neg.expected
    python3 t/models/arith.py --program 024 > t/024-mod-zero.pl
    python3 t/models/arith.py 024 > t/024-mod-zero.expected
    python3 t/models/arith.py --program 025 > t/025-mod-zero-computed.pl
    python3 t/models/arith.py 025 > t/025-mod-zero-computed.expected
    python3 t/models/arith.py --program 026 > t/026-overflow-inner.pl
    python3 t/models/arith.py 026 > t/026-overflow-inner.expected
"""

import sys

MIN, MAX = -(2**63), 2**63 - 1

class Fault(Exception):
    pass

def fits(n):
    if not MIN <= n <= MAX:
        raise Fault('integer overflow')
    return n

# An expression is a number, ('-', e), or (op, left, right).
def value(e):
    if isinstance(e, int):
        return e
    if len(e) == 2:
        return fits(-value(e[1]))
    op, left, right = e
    a = value(left)         # the left operand first: its fault is the one reported
    b = value(right)
    if op == '+':
        return fits(a + b)
    if op == '-':
        return fits(a - b)
    if op == '*':
        return fits(a * b)
    if b == 0:
        raise Fault('modulus by zero')
    return a % b            # Python's %: the sign of the right operand

def text(e, top=True):
    """The expression as source. A negative number is a minus applied to a
    literal, in brackets; the smallest Int can't be written that way,
    since its digits alone are past the largest."""
    if isinstance(e, int):
        if e == MIN:
            return f'(-{MAX} - 1)'
        return f'(-{-e})' if e < 0 else str(e)
    if len(e) == 2:
        return f'-{text(e[1], False)}'
    op, left, right = e
    s = f'{text(left, False)} {op} {text(right, False)}'
    return s if top else f'({s})'

# The values that find the edges: around zero; around 2^31 and 2^32, where
# a 32-bit path would turn; around 2^53, where a double stops holding every
# integer and perl's own arithmetic changes path; the square roots of 2^63
# and the thirds and sevenths of it, which multiply to just inside and just
# outside; 2^62, whose double is 2^63; the two ends; and powers of ten,
# which D23 cares about.
def edges():
    out = {0, 1, 2, 3, 7, 10}
    for p in (31, 32, 53, 62):
        out |= {2**p - 1, 2**p, 2**p + 1}
    out |= {3037000499, 3037000500}             # floor(sqrt(2^63)) and the next
    out |= {MAX // 3, MAX // 3 + 1, MAX // 7, MAX // 7 + 1}
    out |= {10**15, 10**15 + 1, 10**18}
    out |= {MAX - 1, MAX}
    out |= {-v for v in out}
    out |= {MIN, MIN + 1}
    return sorted(out)

# number: the operator; None is unary minus
SAME = {'010': '+', '011': '-', '012': '*', '013': '%', '014': None}

def same_lines(op):
    """(expression, value) for every line of an operator's test: every
    pair of the edges, or every edge negated, that gives an Int."""
    vals = edges()
    tried = [('-', a) for a in vals] if op is None else [(op, a, b) for a in vals for b in vals]
    lines = []
    for e in tried:
        try:
            lines.append((e, value(e)))
        except Fault:
            pass
    return lines

# number: (name, the nearest expression that fits, the one that faults)
FAULTS = {
    '015': ('overflow-add', ('+', MAX - 1, 1), ('+', MAX, 1)),
    '016': ('overflow-add-down', ('+', MIN + 1, -1), ('+', MIN, -1)),
    '017': ('overflow-sub', ('-', MIN + 1, 1), ('-', MIN, 1)),
    '018': ('overflow-sub-up', ('-', MAX - 1, -1), ('-', MAX, -1)),
    '019': ('overflow-mul', ('*', 3037000499, 3037000499), ('*', 3037000500, 3037000500)),
    '020': ('overflow-mul-down', ('*', 2**62, -2), ('*', 2**62 + 1, -2)),
    '021': ('overflow-mul-min', ('*', MIN + 1, -1), ('*', MIN, -1)),
    '022': ('overflow-mul-far', ('*', MAX, 1), ('*', MAX, MAX)),
    '023': ('overflow-neg', ('-', MIN + 1), ('-', MIN)),
    '024': ('mod-zero', ('%', 7, 1), ('%', 7, 0)),
    '025': ('mod-zero-computed', ('%', 7, ('-', 3, 2)), ('%', 7, ('-', 3, 3))),
    # Two faults in one expression: the left operand is evaluated first,
    # so its overflow is the one reported, not the modulus by zero.
    '026': ('overflow-inner', ('+', ('*', 2, 3), ('%', 7, 2)), ('+', ('*', MAX, 2), ('%', 7, 0))),
}

def program(lines, header):
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + ''.join(f'say({text(e)});\n' for e in lines)

def main(argv):
    want_program = argv[0] == '--program'
    number = argv[-1]
    if number in SAME:
        lines = same_lines(SAME[number])
        if want_program:
            sys.stdout.write(program([e for e, _ in lines], ['model: t/models/arith.py']))
        else:
            sys.stdout.write(''.join(f'{v}\n' for _, v in lines))
        return
    name, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault', 'model: t/models/arith.py']
    # A line that fits, the nearest that fits, the fault, and a line the
    # program never reaches (which perl does: the output is the start of
    # perl's, not all of it).
    lines = [1, near, far, 2]
    if want_program:
        sys.stdout.write(program(lines, header))
        return
    out = ''
    for n, e in enumerate(lines):
        try:
            out += f'{value(e)}\n'
        except Fault as f:
            line = len(header) + 1 + n + 1      # the headers, `use v5.42;`, the lines before
            out += f'fault: {f} at {path} line {line}.\nexit: 1\n'
            break
    sys.stdout.write(out)

if __name__ == '__main__':
    main(sys.argv[1:])

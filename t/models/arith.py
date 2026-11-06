"""Model for golden tests 012 to 026 (step 1, arithmetic): writes each
test's program and its expected output, from D8 to D12 and not from the
compiler or the runtime.

The definition, as the model has it:

- An expression is an integer or a list (op a b), op one of + - * / %
  (D8). A program is one expression.
- Every operation is computed exactly, in Python's unbounded integers,
  and a result outside -2**62 .. 2**62 - 1 is the fault `integer
  overflow`, checked after every operation, the intermediate ones
  included (D9). The range is 63 bits, so it is not int64's.
- `/` and `%` truncate toward zero and `%` takes the dividend's sign
  (D10). Python's // and % floor, so the model works on the magnitudes
  and puts the sign back: the quotient is negative when the signs
  differ, the remainder has the dividend's sign. A divisor of 0 is the
  fault `division by zero`, checked before the division.
- The left operand is evaluated, then the right, then the operation, and
  the first fault ends the program (D11).
- A fault is `fault: MESSAGE` on stderr and `exit: 1`, with nothing on
  stdout, since the value is printed only at the end (D3, D12). A value
  is its decimal digits and a newline.

The programs are written below as trees of tuples, (op, a, b), with
integers as leaves, and rendered to source text; the evaluator reads the
tuples, so the text and the answer come from one description.

Commands (one a line; `t/checks.py` runs each and compares the file):

    python3 t/models/arith.py 012-div-signs --program > t/012-div-signs.lang
    python3 t/models/arith.py 012-div-signs > t/012-div-signs.expected
    python3 t/models/arith.py 013-rem-signs --program > t/013-rem-signs.lang
    python3 t/models/arith.py 013-rem-signs > t/013-rem-signs.expected
    python3 t/models/arith.py 014-max-result --program > t/014-max-result.lang
    python3 t/models/arith.py 014-max-result > t/014-max-result.expected
    python3 t/models/arith.py 015-min-result --program > t/015-min-result.lang
    python3 t/models/arith.py 015-min-result > t/015-min-result.expected
    python3 t/models/arith.py 016-rem-min --program > t/016-rem-min.lang
    python3 t/models/arith.py 016-rem-min > t/016-rem-min.expected
    python3 t/models/arith.py 017-add-overflow --program > t/017-add-overflow.lang
    python3 t/models/arith.py 017-add-overflow > t/017-add-overflow.expected
    python3 t/models/arith.py 018-sub-overflow --program > t/018-sub-overflow.lang
    python3 t/models/arith.py 018-sub-overflow > t/018-sub-overflow.expected
    python3 t/models/arith.py 019-mul-overflow --program > t/019-mul-overflow.lang
    python3 t/models/arith.py 019-mul-overflow > t/019-mul-overflow.expected
    python3 t/models/arith.py 020-mul-wrap --program > t/020-mul-wrap.lang
    python3 t/models/arith.py 020-mul-wrap > t/020-mul-wrap.expected
    python3 t/models/arith.py 021-div-overflow --program > t/021-div-overflow.lang
    python3 t/models/arith.py 021-div-overflow > t/021-div-overflow.expected
    python3 t/models/arith.py 022-div-zero --program > t/022-div-zero.lang
    python3 t/models/arith.py 022-div-zero > t/022-div-zero.expected
    python3 t/models/arith.py 023-rem-zero --program > t/023-rem-zero.lang
    python3 t/models/arith.py 023-rem-zero > t/023-rem-zero.expected
    python3 t/models/arith.py 024-order-left --program > t/024-order-left.lang
    python3 t/models/arith.py 024-order-left > t/024-order-left.expected
    python3 t/models/arith.py 025-order-right --program > t/025-order-right.lang
    python3 t/models/arith.py 025-order-right > t/025-order-right.expected
    python3 t/models/arith.py 026-intermediate --program > t/026-intermediate.lang
    python3 t/models/arith.py 026-intermediate > t/026-intermediate.expected
"""
import sys

LO, HI = -(2 ** 62), 2 ** 62 - 1


class Fault(Exception):
    pass


def check(n):
    if n < LO or n > HI:
        raise Fault('integer overflow')
    return n


def trunc_div(a, b):
    # On the magnitudes, the sign put back: not Python's floor.
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def trunc_rem(a, b):
    r = abs(a) % abs(b)
    return -r if a < 0 else r


def ev(e):
    if isinstance(e, int):
        return e
    op, a, b = e
    x = ev(a)  # left, then right, then the operation (D11)
    y = ev(b)
    if op == '+':
        return check(x + y)
    if op == '-':
        return check(x - y)
    if op == '*':
        return check(x * y)
    if y == 0:
        raise Fault('division by zero')
    return check(trunc_div(x, y) if op == '/' else trunc_rem(x, y))


def render(e):
    if isinstance(e, int):
        return str(e)
    return '(' + ' '.join([e[0], render(e[1]), render(e[2])]) + ')'


def signs(op):
    # Weighted so that a floored result shows: each of the four sign
    # cases gets its own decimal place.
    return ('+', ('*', 1000, (op, -7, 2)),
            ('+', ('*', 100, (op, 7, -2)),
             ('+', ('*', 10, (op, -7, -2)), (op, 7, 2))))


# name: (what it checks, decision, program)
TESTS = {
    '012-div-signs': ('/ truncates toward zero in all four sign cases, weighted so a floored one shows', 'D10', signs('/')),
    '013-rem-signs': ('% takes the dividend\'s sign in all four sign cases, weighted so a floored one shows', 'D10', signs('%')),
    '014-max-result': ('a result at the top of the range is not a fault', 'D9', ('+', HI - 1, 1)),
    '015-min-result': ('a result at the bottom of the range is not a fault', 'D9', ('*', -(2 ** 61), 2)),
    '016-rem-min': ('the remainder of the minimum by -1 is 0 and does not fault, though the quotient would', 'D9, D10', ('%', LO, -1)),
    '017-add-overflow': ('one past the top of the range is a fault', 'D9', ('+', HI, 1)),
    '018-sub-overflow': ('one past the bottom of the range is a fault', 'D9', ('-', LO, 1)),
    '019-mul-overflow': ('2**62 faults though int64 holds it: the range is 63 bits', 'D9', ('*', 2 ** 31, 2 ** 31)),
    '020-mul-wrap': ('2**64 faults though int64 wraps it to 0, which is in range', 'D9', ('*', 2 ** 32, 2 ** 32)),
    '021-div-overflow': ('the minimum divided by -1 is 2**62 and faults', 'D9, D10', ('/', LO, -1)),
    '022-div-zero': ('a divisor of zero is a fault', 'D10', ('/', 1, 0)),
    '023-rem-zero': ('a remainder by zero is a fault', 'D10', ('%', 1, 0)),
    '024-order-left': ('the first fault in left to right order is reported: here the left one, division by zero', 'D11', ('+', ('/', 1, 0), ('+', HI, 1))),
    '025-order-right': ('the first fault in left to right order is reported: here the left one, integer overflow, the operands of 024 swapped', 'D11', ('+', ('+', HI, 1), ('/', 1, 0))),
    '026-intermediate': ('an intermediate result that overflows faults though the whole would be 0', 'D9', ('*', ('+', HI, 1), 0)),
}


def program(name):
    what, decision, tree = TESTS[name]
    return f'; Step 1, written by t/models/arith.py ({decision}): {what}.\n{render(tree)}\n'


def expected(name):
    try:
        return f'{ev(TESTS[name][2])}\n'
    except Fault as f:
        return f'fault: {f}\nexit: 1\n'


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in TESTS or sys.argv[2:] not in ([], ['--program']):
        sys.exit('usage: arith.py NAME [--program]')
    sys.stdout.write(program(sys.argv[1]) if len(sys.argv) == 3 else expected(sys.argv[1]))

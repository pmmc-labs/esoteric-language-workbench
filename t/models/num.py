#!/usr/bin/env python3
"""t/040 to t/074: Num, `/`, `**`, and the two kinds of number together
(step 2; D35 to D38).

The definition, which is all this file knows of the language. A number is
an Int, a whole number from -2^63 to 2^63 - 1, or a Num, a finite double.
An operand is *integral* when it is an Int, or a Num that is whole and
below 2^53. Then (D35):

  + -   both integral: the exact answer, an Int, or `integer overflow`.
        Otherwise the doubles added: a Num.
  *     both integral: the exact answer if it is an Int. If not, two Ints
        overflow, and so does an answer from 2^63 to 2^64 - 1; past that,
        and whenever an operand isn't integral, the doubles multiplied.
  /     by zero, `division by zero`. An Int past 2^53 that the right
        operand divides exactly: the exact Int. Otherwise the doubles
        divided, a Num.
  %     each operand cut to its whole part, which must be an Int
        (`modulus of a number outside the integers`); by zero, `modulus by
        zero`; the remainder has the sign of the right operand.
  **    both integral and the power 0 or more: a base of 0, 1, -1 or plus
        or minus a power of two gives a Num, exact; another base gives the
        exact Int when its bits times the power are at most 64. Otherwise
        C's pow, a Num.
  -x    an Int negated (or `integer overflow`); a Num's sign changed.

A Num is finite (D37): a result that would be an infinity is `float
overflow`, a NaN `not a number`. `say` prints a Num as C's %.15g does,
and a zero of either sign as 0; but a whole Num from 10^15 up to 2^53
faults when printed (D36), because perl prints it two ways.

The model is Python's integers and floats, whose arithmetic is IEEE's as
perl's and C's is, and the C library's own pow, called through ctypes,
since that is the function the definition names. perl is the second
derivation: t/checks.py oracle holds every .expected of 040 to 047 to
what perl 5.42 prints, and each fault test's output to the start of it.
Where this model and perl disagree, neither file is patched: it is a
finding about D35.

Two C libraries can differ in the last bit of a pow, and these files are
written on one machine and checked on others. So a line with `**` is in a
test only if its answer prints the same one double up and one double
down: no last bit can change it.

040 to 045 are an operator each, over every pair of an Int and a Num, a
Num and an Int, and two Nums (and two Ints for `/` and `**`, which step 1
didn't have), a line a pair, wherever there is an answer that prints.
046 is each Num negated and 047 is Nums printed. 048 to 074 each fault
once, the line before the fault being the nearest thing that doesn't.

Every line is `say(EXPR);` (T25). A negative number is a minus applied to
a literal, in brackets. A Num is written as Python's repr of it, the
shortest decimal that reads back to the same double; perl reads a decimal
to the nearest double too (docs/briefs/step2-literals.py).

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/num.py --program 040 > t/040-num-add.pl
    python3 t/models/num.py 040 > t/040-num-add.expected
    python3 t/models/num.py --program 041 > t/041-num-sub.pl
    python3 t/models/num.py 041 > t/041-num-sub.expected
    python3 t/models/num.py --program 042 > t/042-num-mul.pl
    python3 t/models/num.py 042 > t/042-num-mul.expected
    python3 t/models/num.py --program 043 > t/043-num-div.pl
    python3 t/models/num.py 043 > t/043-num-div.expected
    python3 t/models/num.py --program 044 > t/044-num-mod.pl
    python3 t/models/num.py 044 > t/044-num-mod.expected
    python3 t/models/num.py --program 045 > t/045-num-pow.pl
    python3 t/models/num.py 045 > t/045-num-pow.expected
    python3 t/models/num.py --program 046 > t/046-num-neg.pl
    python3 t/models/num.py 046 > t/046-num-neg.expected
    python3 t/models/num.py --program 047 > t/047-num-print.pl
    python3 t/models/num.py 047 > t/047-num-print.expected
    python3 t/models/num.py --program 048 > t/048-overflow-num-add.pl
    python3 t/models/num.py 048 > t/048-overflow-num-add.expected
    python3 t/models/num.py --program 049 > t/049-overflow-num-sub.pl
    python3 t/models/num.py 049 > t/049-overflow-num-sub.expected
    python3 t/models/num.py --program 050 > t/050-overflow-num-mul.pl
    python3 t/models/num.py 050 > t/050-overflow-num-mul.expected
    python3 t/models/num.py --program 051 > t/051-overflow-int-num-mul.pl
    python3 t/models/num.py 051 > t/051-overflow-int-num-mul.expected
    python3 t/models/num.py --program 052 > t/052-overflow-div.pl
    python3 t/models/num.py 052 > t/052-overflow-div.expected
    python3 t/models/num.py --program 053 > t/053-overflow-pow.pl
    python3 t/models/num.py 053 > t/053-overflow-pow.expected
    python3 t/models/num.py --program 054 > t/054-div-zero.pl
    python3 t/models/num.py 054 > t/054-div-zero.expected
    python3 t/models/num.py --program 055 > t/055-div-zero-num.pl
    python3 t/models/num.py 055 > t/055-div-zero-num.expected
    python3 t/models/num.py --program 056 > t/056-div-zero-negative.pl
    python3 t/models/num.py 056 > t/056-div-zero-negative.expected
    python3 t/models/num.py --program 057 > t/057-div-zero-zero.pl
    python3 t/models/num.py 057 > t/057-div-zero-zero.expected
    python3 t/models/num.py --program 058 > t/058-mod-zero-num.pl
    python3 t/models/num.py 058 > t/058-mod-zero-num.expected
    python3 t/models/num.py --program 059 > t/059-mod-outside-left.pl
    python3 t/models/num.py 059 > t/059-mod-outside-left.expected
    python3 t/models/num.py --program 060 > t/060-mod-outside-right.pl
    python3 t/models/num.py 060 > t/060-mod-outside-right.expected
    python3 t/models/num.py --program 061 > t/061-float-overflow-mul.pl
    python3 t/models/num.py 061 > t/061-float-overflow-mul.expected
    python3 t/models/num.py --program 062 > t/062-float-overflow-add.pl
    python3 t/models/num.py 062 > t/062-float-overflow-add.expected
    python3 t/models/num.py --program 063 > t/063-float-overflow-div.pl
    python3 t/models/num.py 063 > t/063-float-overflow-div.expected
    python3 t/models/num.py --program 064 > t/064-float-overflow-pow.pl
    python3 t/models/num.py 064 > t/064-float-overflow-pow.expected
    python3 t/models/num.py --program 065 > t/065-float-overflow-zero-pow.pl
    python3 t/models/num.py 065 > t/065-float-overflow-zero-pow.expected
    python3 t/models/num.py --program 066 > t/066-float-overflow-vast-pow.pl
    python3 t/models/num.py 066 > t/066-float-overflow-vast-pow.expected
    python3 t/models/num.py --program 067 > t/067-not-a-number.pl
    python3 t/models/num.py 067 > t/067-not-a-number.expected
    python3 t/models/num.py --program 068 > t/068-print-whole-float.pl
    python3 t/models/num.py 068 > t/068-print-whole-float.expected
    python3 t/models/num.py --program 069 > t/069-print-whole-float-negative.pl
    python3 t/models/num.py 069 > t/069-print-whole-float-negative.expected
    python3 t/models/num.py --program 070 > t/070-print-whole-float-top.pl
    python3 t/models/num.py 070 > t/070-print-whole-float-top.expected
    python3 t/models/num.py --program 071 > t/071-print-whole-float-pow.pl
    python3 t/models/num.py 071 > t/071-print-whole-float-pow.expected
    python3 t/models/num.py --program 072 > t/072-print-whole-float-div.pl
    python3 t/models/num.py 072 > t/072-print-whole-float-div.expected
    python3 t/models/num.py --program 073 > t/073-fault-order.pl
    python3 t/models/num.py 073 > t/073-fault-order.expected
    python3 t/models/num.py --program 074 > t/074-print-whole-float-power-of-two.pl
    python3 t/models/num.py 074 > t/074-print-whole-float-power-of-two.expected
"""

import ctypes
import ctypes.util
import math
import random
import sys

MIN, MAX = -(2**63), 2**63 - 1

libm = ctypes.CDLL(ctypes.util.find_library('m'))
libm.pow.restype = ctypes.c_double
libm.pow.argtypes = [ctypes.c_double, ctypes.c_double]

class Fault(Exception):
    pass

def Int(n):
    if not MIN <= n <= MAX:
        raise Fault('integer overflow')
    return n

def Num(x):
    if math.isinf(x):
        raise Fault('float overflow')
    if math.isnan(x):
        raise Fault('not a number')
    return x

def is_num(v):
    return isinstance(v, float)

def integral(v):
    """The whole number an operand stands for, or None."""
    if not is_num(v):
        return v
    return int(v) if v == math.trunc(v) and abs(v) < 2**53 else None

def operate(op, a, b):
    x, y = integral(a), integral(b)
    fa, fb = float(a), float(b)
    if op in ('+', '-'):
        if x is not None and y is not None:
            return Int(x + y if op == '+' else x - y)
        return Num(fa + fb if op == '+' else fa - fb)
    if op == '*':
        if x is not None and y is not None:
            p = x * y
            if MIN <= p <= MAX:
                return p
            if not is_num(a) and not is_num(b) or 2**63 <= p <= 2**64 - 1:
                raise Fault('integer overflow')
        return Num(fa * fb)
    if op == '/':
        if fb == 0.0:
            raise Fault('division by zero')
        if not is_num(a) and abs(a) > 2**53 and y is not None and a % y == 0:
            return Int(a // y)
        return Num(fa / fb)
    if op == '%':
        cut = []
        for v in (a, b):
            t = math.trunc(v)
            if not MIN <= t <= MAX:
                raise Fault('modulus of a number outside the integers')
            cut.append(t)
        if cut[1] == 0:
            raise Fault('modulus by zero')
        return cut[0] % cut[1]          # Python's %: the sign of the right operand
    if op == '**':
        if x is not None and y is not None and y >= 0:
            if abs(x) & (abs(x) - 1) == 0:
                # 0, 1, -1 and plus or minus a power of two: a Num, and
                # exact, since every factor is a power of two.
                if abs(x) <= 1:
                    return float(x) ** (y % 2) if x == -1 else (1.0 if y == 0 or x == 1 else 0.0)
                if y * (abs(x).bit_length() - 1) > 1023:
                    raise Fault('float overflow')
                return float(x ** y)
            if y * abs(x).bit_length() <= 64:
                return Int(x ** y)
        return Num(libm.pow(fa, fb))
    raise AssertionError(op)

# An expression is a number, ('-', e), or (op, left, right).
def value(e):
    if not isinstance(e, tuple):
        return e
    if len(e) == 2:
        v = value(e[1])
        return -v if is_num(v) else Int(-v)
    op, left, right = e
    a = value(left)         # the left operand first: its fault is the one reported
    b = value(right)
    return operate(op, a, b)

def printed(v):
    """What say prints for a value, or the fault."""
    if not is_num(v):
        return str(v)
    if v == math.trunc(v) and 10**15 <= abs(v) < 2**53:
        raise Fault('a whole float this size prints two ways in perl (add 0 to print the integer)')
    return '0' if v == 0 else '%.15g' % v

def text(e, top=True):
    """The expression as source."""
    if not isinstance(e, tuple):
        if is_num(e):
            # repr is the shortest decimal that reads back to this double.
            # math.copysign: a negative zero is negative too.
            return f'(-{abs(e)!r})' if math.copysign(1, e) < 0 else repr(e)
        if e == MIN:
            return f'(-{MAX} - 1)'
        return f'(-{-e})' if e < 0 else str(e)
    if len(e) == 2:
        # In brackets when it is an operand: two minus signs together are
        # a decrement to perl (T27).
        s = f'-{text(e[1], False)}'
        return s if top else f'({s})'
    op, left, right = e
    s = f'{text(left, False)} {op} {text(right, False)}'
    return s if top else f'({s})'

# The Ints that find the edges of "integral" and of the Int range, and the
# Nums: zeros of both signs; halves; whole Nums small, at 10^15 where
# printing changes, and on each side of 2^53 where integral stops; on each
# side of 2^63 and 2^64, where perl's unsigned integers begin and end; and
# the ends of the doubles.
INTS = [0, 1, -1, 2, 3, -3, 7, -7, 10, 16, 2**31, 2**32 + 1, 3037000500, 10**15, 10**15 + 1,
        2**53 - 1, 2**53, 2**53 + 1, -(2**53), 2**62, MAX // 3, MAX - 1, MAX, MIN + 1, MIN]
NUMS = [0.0, -0.0, 0.5, -0.5, 1.0, 1.5, -2.5, 3.0, 3.7, 0.1, 1e-5, 1000.0, 4294967296.0, 999999999999999.0,
        1e15, -1e15, 2e15, 2.0**53 - 1, 2.0**53, 2.0**53 + 2, -(2.0**53), 1e16, -1e16, 2.0**62,
        2.0**63 - 1024, 2.0**63, 1e19, 1.8e19, 2.0**64, 1e20, 1e300, -1e300, 5e-324, 1.7976931348623157e308]
# For `**`: bases of every number of bits the rule turns on, with the
# powers on each side of "bits times power is at most 64" (2 bits and 32
# or 33, 3 and 21 or 22, 4 and 16 or 17, 5 and 12 or 13, 8 and 8 or 9, 16
# and 4 or 5, 32 and 2 or 3); and powers of two large enough that an Int
# and a Num of the same value print differently (1024 ** 5, 2^31 ** 2).
BASES = [0, 1, -1, 2, -2, 3, -3, 7, 10, 15, 16, 17, 31, 255, 1024, -1024, 65535, 2**31, 3037000499, 4294967295,
         4294967296, 2**53 + 1, MAX, MIN,
         0.0, 0.5, 1.5, -1.5, 2.0, 3.0, -8.0, 10.0, 0.1, 1e15, 2.0**53, 1e16, 1e300]
POWERS = [0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 15, 16, 17, 20, 21, 22, 32, 33, 39, 40, 50, 62, 63, 64, 1023, -1, -2, -3,
          0.0, 0.5, -0.5, 1.5, 2.0, 3.0, 62.0, 0.1]

def pairs(op):
    if op == '**':
        return [(a, b) for a in BASES for b in POWERS]
    mixed = [(a, b) for a in INTS for b in NUMS] + [(a, b) for a in NUMS for b in INTS] + [(a, b) for a in NUMS for b in NUMS]
    return [(a, b) for a in INTS for b in INTS] + mixed if op == '/' else mixed

def steady(v):
    """Whether a last-bit difference in v would print the same."""
    if not is_num(v):
        return True
    try:
        return printed(v) == printed(math.nextafter(v, math.inf)) == printed(math.nextafter(v, -math.inf))
    except Fault:
        return False

def lines_with_answers(exprs, pow_too=False):
    """(expression, what it prints) for each that has an answer that prints."""
    out = []
    for e in exprs:
        try:
            v = value(e)
            if pow_too and not steady(v):
                continue
            out.append((e, printed(v)))
        except Fault:
            pass
    return out

def print_values():
    """Nums to print: the edges, and doubles from all over, the same ones
    every time."""
    rng = random.Random(2)
    out = list(NUMS) + [0.3, 1 / 3, 2 / 3, 1e21, 1e-7, 123456789012345.6, 0.1 + 0.2, 100.0, 1e14, 99999999999999.9,
                        999999999999999.9, 0.000123, 123456.789, 2.5e-10, 9.999999999999999e22, 1e23, 4.35, 0.15, 2.675]
    for _ in range(600):
        mantissa = rng.randrange(1, 10**rng.randrange(1, 18))
        out.append(float(f'{mantissa}e{rng.randrange(-320, 300)}'))
    for _ in range(200):
        out.append(rng.randrange(1, 10**15) / 10**rng.randrange(0, 15))
    return [v for v in out if math.isfinite(v)]

# number: (name, the operator, or None)
SAME = {
    '040': ('num-add', '+'), '041': ('num-sub', '-'), '042': ('num-mul', '*'), '043': ('num-div', '/'),
    '044': ('num-mod', '%'), '045': ('num-pow', '**'), '046': ('num-neg', None), '047': ('num-print', None),
}

def same_lines(number):
    op = SAME[number][1]
    if number == '046':
        return lines_with_answers([('-', v) for v in NUMS] + [('-', ('-', v)) for v in NUMS])
    if number == '047':
        return lines_with_answers(print_values())
    return lines_with_answers([(op, a, b) for a, b in pairs(op)], pow_too=op == '**')

# number: (name, the nearest expression that prints, the one that faults)
FAULTS = {
    '048': ('overflow-num-add', ('+', MAX - 1, 1.0), ('+', MAX, 1.0)),
    '049': ('overflow-num-sub', ('-', MIN + 1, 1.0), ('-', MIN, 1.0)),
    '050': ('overflow-num-mul', ('*', 1e9, 1e9), ('*', 1e10, 1e9)),
    '051': ('overflow-int-num-mul', ('*', MAX, 3.0), ('*', MAX, 2.0)),
    '052': ('overflow-div', ('/', MIN, 1), ('/', MIN, -1)),
    '053': ('overflow-pow', ('**', 3037000499, 2), ('**', 4294967295, 2)),
    '054': ('div-zero', ('/', 1, 2), ('/', 1, 0)),
    '055': ('div-zero-num', ('/', 1.5, 0.5), ('/', 1.5, 0.0)),
    '056': ('div-zero-negative', ('/', 1, -0.5), ('/', 1, -0.0)),
    '057': ('div-zero-zero', ('/', 0, 5), ('/', 0, ('-', 0.5, 0.5))),
    '058': ('mod-zero-num', ('%', 7, 1.5), ('%', 7, 0.5)),
    '059': ('mod-outside-left', ('%', 9.2e18, 7), ('%', 1e20, 7)),
    '060': ('mod-outside-right', ('%', 7, 9.2e18), ('%', 7, 1e20)),
    '061': ('float-overflow-mul', ('*', 1e307, 10), ('*', 1e308, 10)),
    '062': ('float-overflow-add', ('+', 1.7976931348623157e308, 1e291), ('+', 1.7976931348623157e308, 1e292)),
    '063': ('float-overflow-div', ('/', 1e307, 0.1), ('/', 1e308, 0.1)),
    '064': ('float-overflow-pow', ('**', 2, 1023), ('**', 2, 1024)),
    '065': ('float-overflow-zero-pow', ('**', 0, 1), ('**', 0, -1)),
    # perl prints 0 here: its test for an answer that fits wraps (T77).
    '066': ('float-overflow-vast-pow', ('**', 10, 16), ('**', 10, 2**62)),
    '067': ('not-a-number', ('**', 8, 0.5), ('**', -8.0, 0.5)),
    '068': ('print-whole-float', 999999999999999.0, 1e15),
    '069': ('print-whole-float-negative', ('-', 999999999999999.0), ('-', 1e15)),
    '070': ('print-whole-float-top', 2.0**53, 2.0**53 - 1),
    '071': ('print-whole-float-pow', ('**', 2, 49.5), ('**', 2, 50)),
    '072': ('print-whole-float-div', ('/', 4000000000000001, 2), ('/', 4000000000000000, 2)),
    # The left operand's fault is the one that happens.
    '073': ('fault-order', ('+', ('/', 1, 2), ('**', 2, 0.5)), ('+', ('/', 1, 0), ('**', -8.0, 0.5))),
    # A power of two to a whole power is a Num whatever its size: as an
    # Int, which the bits would allow, this one would print.
    '074': ('print-whole-float-power-of-two', ('**', 1024, 4), ('**', 1024, 5)),
}

def program(lines, header):
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + ''.join(f'say({text(e)});\n' for e in lines)

def main(argv):
    want_program = argv[0] == '--program'
    number = argv[-1]
    if number in SAME:
        lines = same_lines(number)
        if want_program:
            sys.stdout.write(program([e for e, _ in lines], ['model: t/models/num.py']))
        else:
            sys.stdout.write(''.join(f'{p}\n' for _, p in lines))
        return
    name, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault', 'model: t/models/num.py']
    # A line that prints, the nearest that prints, the fault, and a line
    # the program never reaches (which perl does).
    lines = [1, near, far, 2]
    if want_program:
        sys.stdout.write(program(lines, header))
        return
    out = ''
    for n, e in enumerate(lines):
        try:
            out += f'{printed(value(e))}\n'
        except Fault as f:
            line = len(header) + 1 + n + 1      # the headers, `use v5.42;`, the lines before
            out += f'fault: {f} at {path} line {line}.\nexit: 1\n'
            break
    assert 'fault:' in out and out.count('\n') == 4, (number, out)
    sys.stdout.write(out)

if __name__ == '__main__':
    main(sys.argv[1:])

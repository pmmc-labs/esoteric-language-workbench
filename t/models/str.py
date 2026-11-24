#!/usr/bin/env python3
"""t/100 to t/169: strings (step 3; D39 to D45).

The definition, which is all this file knows of the language beyond
t/models/num.py (the numbers, which it imports). A value is an Int, a Num
or a Str: a sequence of Unicode scalar values (D42), which is Python's
`str` less the surrogates.

A number where a string is wanted is what `say` prints for it (D36's
fault included).

A string where a number is wanted (D40) must be, in full: blanks (space,
tab, newline, carriage return, form feed, vertical tab); a sign or none;
digits with a point among them or not, at least one digit; an exponent or
none (`e` or `E`, a sign or none, digits); blanks. Anything else is `not a
numeric string`. Then, by how it is written:

  digits only          the Int, or `integer overflow`
  with an exponent     the nearest double (or `float overflow`). Whole and
                       below 2^53: the Int. Whole and larger: a fault, perl
                       having two values for it. Otherwise the Num.
  with a point and     the Num. If it is whole and below 2^53 it is *soft*:
  no exponent          see below.

Arithmetic is num.py's on those numbers, with two things added, each a
place where perl has two answers by what was done with a value before:

  D45   in `+ - *` on two integral operands, a whole number of 2^53 or
        more that a double holds exactly faults unless the other operand
        is an Int (and not a string that is one).
  soft  in `+ - * / **`, a soft string with an integral operand beside it
        is float arithmetic, a Num, and faults when either whole number,
        or the exact answer of `+ - *` or of `**` to a power of 0 or
        more, is 2^53 or more. (`%` cuts its operands to whole numbers
        anyway.) With an operand that isn't integral it is num.py's rule.

  -s    a minus before a string: the string must be a number; it faults
        if the string's first character is `+`, or its number is whole and
        2^53 or more; otherwise the Num, negated.
  +s    the operand, whatever it is.

Where a whole number is wanted (the count of `x`, a position or a length
of `substr` and `index`), the number is cut toward zero, and must then be
an Int.

  a . b            the two as strings, joined
  s x n            s as a string, n times. A count below zero (before it is
                   cut: -0.5 too) is `negative repeat count`; n times the
                   length may not pass 2^31 - 1.
  length(v)        the number of characters of v as a string
  uc(v), lc(v)     v as a string, its ASCII letters changed; a character
                   past ASCII faults (T45)
  ord(v)           the first character's number, 0 for the empty string
  chr(n)           the character whose number is n cut toward zero; a
                   number below zero, a surrogate or one past U+10FFFF is
                   `not a character`
  substr(s, o)     from o, counted from the end if negative, to the end
  substr(s, o, n)  n characters from there, or to n from the end if n is
                   negative. A start past the end is `substr outside of
                   string`, and so is a piece that starts and ends before
                   the beginning. Otherwise a start before the beginning,
                   and an end past the end or before the start, are moved
                   in.
  index(s, t)      where t first is in s, or -1
  index(s, t, p)   at or after p, which is moved into the string

`say` prints a value as a string and a newline, `print` without one, as
UTF-8. A character past ASCII is a fault unless the program has `use open
':std', ':encoding(UTF-8)';` (D39), and a noncharacter always is (D42).
An operator's operands and a builtin's arguments are worked out left
before right, and made strings or numbers in that order.

The model is Python's `str`, integers and floats. perl is the second
derivation: t/checks.py oracle holds every .expected of a test without a
`kind:` to what perl 5.42 prints, and each fault test's output to the
start of it. Where the two disagree neither file is patched: it is a
finding about the definition.

A string is written in single quotes when it is plain, and otherwise in
double quotes with `\\n`, `\\t`, a backslash before `" \\ $ @`, and
`\\x{...}` for anything else: so these files are ASCII, and need no `use
utf8`. A test that prints a character past ASCII has the `use open` line.

100 to 105 are an operator each over strings and numbers, both ways round,
and two strings. 106 is the minus and the plus; 107 `.`; 108 `x`; 109
`length`, `ord` and `chr`; 110 `uc` and `lc`; 111 and 112 `substr`; 113
`index`; 114 whole numbers wanted; 115 printing; 116 every way of writing
a number in a string. 120 to 169 each fault once, the line before the
fault being a near thing that doesn't.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/str.py --program 100 > t/100-str-add.pl
    python3 t/models/str.py 100 > t/100-str-add.expected
    python3 t/models/str.py --program 101 > t/101-str-sub.pl
    python3 t/models/str.py 101 > t/101-str-sub.expected
    python3 t/models/str.py --program 102 > t/102-str-mul.pl
    python3 t/models/str.py 102 > t/102-str-mul.expected
    python3 t/models/str.py --program 103 > t/103-str-div.pl
    python3 t/models/str.py 103 > t/103-str-div.expected
    python3 t/models/str.py --program 104 > t/104-str-mod.pl
    python3 t/models/str.py 104 > t/104-str-mod.expected
    python3 t/models/str.py --program 105 > t/105-str-pow.pl
    python3 t/models/str.py 105 > t/105-str-pow.expected
    python3 t/models/str.py --program 106 > t/106-str-neg.pl
    python3 t/models/str.py 106 > t/106-str-neg.expected
    python3 t/models/str.py --program 107 > t/107-str-concat.pl
    python3 t/models/str.py 107 > t/107-str-concat.expected
    python3 t/models/str.py --program 108 > t/108-str-repeat.pl
    python3 t/models/str.py 108 > t/108-str-repeat.expected
    python3 t/models/str.py --program 109 > t/109-str-chars.pl
    python3 t/models/str.py 109 > t/109-str-chars.expected
    python3 t/models/str.py --program 110 > t/110-str-case.pl
    python3 t/models/str.py 110 > t/110-str-case.expected
    python3 t/models/str.py --program 111 > t/111-str-substr.pl
    python3 t/models/str.py 111 > t/111-str-substr.expected
    python3 t/models/str.py --program 112 > t/112-str-substr-length.pl
    python3 t/models/str.py 112 > t/112-str-substr-length.expected
    python3 t/models/str.py --program 113 > t/113-str-index.pl
    python3 t/models/str.py 113 > t/113-str-index.expected
    python3 t/models/str.py --program 114 > t/114-str-whole.pl
    python3 t/models/str.py 114 > t/114-str-whole.expected
    python3 t/models/str.py --program 115 > t/115-str-print.pl
    python3 t/models/str.py 115 > t/115-str-print.expected
    python3 t/models/str.py --program 116 > t/116-str-forms.pl
    python3 t/models/str.py 116 > t/116-str-forms.expected
    python3 t/models/str.py --program 120 > t/120-not-numeric.pl
    python3 t/models/str.py 120 > t/120-not-numeric.expected
    python3 t/models/str.py --program 121 > t/121-not-numeric-empty.pl
    python3 t/models/str.py 121 > t/121-not-numeric-empty.expected
    python3 t/models/str.py --program 122 > t/122-not-numeric-trailing.pl
    python3 t/models/str.py 122 > t/122-not-numeric-trailing.expected
    python3 t/models/str.py --program 123 > t/123-not-numeric-hex.pl
    python3 t/models/str.py 123 > t/123-not-numeric-hex.expected
    python3 t/models/str.py --program 124 > t/124-not-numeric-underscore.pl
    python3 t/models/str.py 124 > t/124-not-numeric-underscore.expected
    python3 t/models/str.py --program 125 > t/125-not-numeric-inf.pl
    python3 t/models/str.py 125 > t/125-not-numeric-inf.expected
    python3 t/models/str.py --program 126 > t/126-not-numeric-nan.pl
    python3 t/models/str.py 126 > t/126-not-numeric-nan.expected
    python3 t/models/str.py --program 127 > t/127-not-numeric-but-true.pl
    python3 t/models/str.py 127 > t/127-not-numeric-but-true.expected
    python3 t/models/str.py --program 128 > t/128-not-numeric-nul.pl
    python3 t/models/str.py 128 > t/128-not-numeric-nul.expected
    python3 t/models/str.py --program 129 > t/129-not-numeric-digit.pl
    python3 t/models/str.py 129 > t/129-not-numeric-digit.expected
    python3 t/models/str.py --program 130 > t/130-string-overflow.pl
    python3 t/models/str.py 130 > t/130-string-overflow.expected
    python3 t/models/str.py --program 131 > t/131-string-overflow-negative.pl
    python3 t/models/str.py 131 > t/131-string-overflow-negative.expected
    python3 t/models/str.py --program 132 > t/132-string-float-overflow.pl
    python3 t/models/str.py 132 > t/132-string-float-overflow.expected
    python3 t/models/str.py --program 133 > t/133-string-exponent.pl
    python3 t/models/str.py 133 > t/133-string-exponent.expected
    python3 t/models/str.py --program 134 > t/134-two-answers-string.pl
    python3 t/models/str.py 134 > t/134-two-answers-string.expected
    python3 t/models/str.py --program 135 > t/135-two-answers-two-strings.pl
    python3 t/models/str.py 135 > t/135-two-answers-two-strings.expected
    python3 t/models/str.py --program 136 > t/136-soft-add.pl
    python3 t/models/str.py 136 > t/136-soft-add.expected
    python3 t/models/str.py --program 137 > t/137-soft-operand.pl
    python3 t/models/str.py 137 > t/137-soft-operand.expected
    python3 t/models/str.py --program 138 > t/138-soft-mul.pl
    python3 t/models/str.py 138 > t/138-soft-mul.expected
    python3 t/models/str.py --program 139 > t/139-soft-pow.pl
    python3 t/models/str.py 139 > t/139-soft-pow.expected
    python3 t/models/str.py --program 140 > t/140-soft-div.pl
    python3 t/models/str.py 140 > t/140-soft-div.expected
    python3 t/models/str.py --program 141 > t/141-neg-plus.pl
    python3 t/models/str.py 141 > t/141-neg-plus.expected
    python3 t/models/str.py --program 142 > t/142-neg-large.pl
    python3 t/models/str.py 142 > t/142-neg-large.expected
    python3 t/models/str.py --program 143 > t/143-neg-not-numeric.pl
    python3 t/models/str.py 143 > t/143-neg-not-numeric.expected
    python3 t/models/str.py --program 144 > t/144-substr-outside.pl
    python3 t/models/str.py 144 > t/144-substr-outside.expected
    python3 t/models/str.py --program 145 > t/145-substr-outside-length.pl
    python3 t/models/str.py 145 > t/145-substr-outside-length.expected
    python3 t/models/str.py --program 146 > t/146-repeat-negative.pl
    python3 t/models/str.py 146 > t/146-repeat-negative.expected
    python3 t/models/str.py --program 147 > t/147-repeat-negative-fraction.pl
    python3 t/models/str.py 147 > t/147-repeat-negative-fraction.expected
    python3 t/models/str.py --program 148 > t/148-repeat-too-long.pl
    python3 t/models/str.py 148 > t/148-repeat-too-long.expected
    python3 t/models/str.py --program 149 > t/149-chr-past-unicode.pl
    python3 t/models/str.py 149 > t/149-chr-past-unicode.expected
    python3 t/models/str.py --program 150 > t/150-chr-surrogate.pl
    python3 t/models/str.py 150 > t/150-chr-surrogate.expected
    python3 t/models/str.py --program 151 > t/151-chr-negative.pl
    python3 t/models/str.py 151 > t/151-chr-negative.expected
    python3 t/models/str.py --program 152 > t/152-whole-outside.pl
    python3 t/models/str.py 152 > t/152-whole-outside.expected
    python3 t/models/str.py --program 153 > t/153-whole-outside-index.pl
    python3 t/models/str.py 153 > t/153-whole-outside-index.expected
    python3 t/models/str.py --program 154 > t/154-whole-outside-repeat.pl
    python3 t/models/str.py 154 > t/154-whole-outside-repeat.expected
    python3 t/models/str.py --program 155 > t/155-print-past-ascii.pl
    python3 t/models/str.py 155 > t/155-print-past-ascii.expected
    python3 t/models/str.py --program 156 > t/156-print-noncharacter.pl
    python3 t/models/str.py 156 > t/156-print-noncharacter.expected
    python3 t/models/str.py --program 157 > t/157-print-noncharacter-high.pl
    python3 t/models/str.py 157 > t/157-print-noncharacter-high.expected
    python3 t/models/str.py --program 158 > t/158-uc-past-ascii.pl
    python3 t/models/str.py 158 > t/158-uc-past-ascii.expected
    python3 t/models/str.py --program 159 > t/159-lc-past-ascii.pl
    python3 t/models/str.py 159 > t/159-lc-past-ascii.expected
    python3 t/models/str.py --program 160 > t/160-concat-whole-float.pl
    python3 t/models/str.py 160 > t/160-concat-whole-float.expected
    python3 t/models/str.py --program 161 > t/161-length-whole-float.pl
    python3 t/models/str.py 161 > t/161-length-whole-float.expected
    python3 t/models/str.py --program 162 > t/162-fault-order.pl
    python3 t/models/str.py 162 > t/162-fault-order.expected
    python3 t/models/str.py --program 163 > t/163-fault-order-arguments.pl
    python3 t/models/str.py 163 > t/163-fault-order-arguments.expected
    python3 t/models/str.py --program 164 > t/164-fault-order-operands.pl
    python3 t/models/str.py 164 > t/164-fault-order-operands.expected
    python3 t/models/str.py --program 165 > t/165-fault-order-conversions.pl
    python3 t/models/str.py 165 > t/165-fault-order-conversions.expected
    python3 t/models/str.py --program 166 > t/166-substr-outside-before.pl
    python3 t/models/str.py 166 > t/166-substr-outside-before.expected
    python3 t/models/str.py --program 167 > t/167-substr-outside-before-negative.pl
    python3 t/models/str.py 167 > t/167-substr-outside-before-negative.expected
    python3 t/models/str.py --program 168 > t/168-substr-outside-empty.pl
    python3 t/models/str.py 168 > t/168-substr-outside-empty.expected
    python3 t/models/str.py --program 169 > t/169-neg-whole-float.pl
    python3 t/models/str.py 169 > t/169-neg-whole-float.expected
"""

import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import num
from num import Fault, MIN, MAX, is_num, libm

NOT_NUMERIC = 'not a numeric string'
EXPONENT = 'a string with an exponent that is a whole number this large has two values in perl'
SOFT = 'a string like "3.0" in arithmetic this large has two answers in perl'
NEG_PLUS = 'a minus before a string that starts with a plus'
NEG_LARGE = 'a minus before a string that is a whole number this large has two answers in perl'
OUTSIDE = 'a number outside the integers where a whole number is wanted'
NEGATIVE_COUNT = 'negative repeat count'
TOO_LONG = 'repeated string too long'
NOT_A_CHARACTER = 'not a character'
SUBSTR = 'substr outside of string'
PAST_ASCII = "a character past ASCII printed without 'use open'"
NONCHARACTER = 'a noncharacter printed'

NUMERIC = re.compile(r'[ \t\n\r\f\v]*([+-]?)(?:([0-9]+)(?:(\.)([0-9]*))?|(\.)([0-9]+))(?:[eE]([+-]?[0-9]+))?[ \t\n\r\f\v]*\Z')

def is_str(v):
    return isinstance(v, str)

def as_number(v):
    """A value where a number is wanted: (the Int or the Num, whether it is
    a soft string)."""
    if not is_str(v):
        return v, False
    m = NUMERIC.match(v)
    if not m:
        raise Fault(NOT_NUMERIC)
    sign, whole, point, frac, lead_point, lead_frac, exponent = m.groups()
    if exponent is None and not (point or lead_point):
        n = int(sign + whole)
        if not MIN <= n <= MAX:
            raise Fault('integer overflow')
        return n, False
    x = float(sign + (whole or '') + '.' + (frac or lead_frac or '') + 'e' + (exponent or '0'))
    if math.isinf(x):
        raise Fault('float overflow')
    is_whole = x == math.trunc(x)
    if exponent is not None:
        if is_whole and abs(x) < 2**53:
            return int(x), False
        if is_whole:
            raise Fault(EXPONENT)
        return x, False
    return x, is_whole and abs(x) < 2**53

def arith(op, a, b):
    p, soft_p = as_number(a)        # the left operand first: its fault is the one reported
    q, soft_q = as_number(b)
    x, y = num.integral(p), num.integral(q)
    both = x is not None and y is not None
    if both and op in ('+', '-', '*'):
        num.two_answers(x, y, not is_num(a) and not is_str(a), not is_num(b) and not is_str(b))
    if not (both and (soft_p or soft_q)) or op == '%':
        return num.operate(op, p, q)
    if abs(x) >= 2**53 or abs(y) >= 2**53:
        raise Fault(SOFT)
    exact = 0
    if op == '+': exact = x + y
    if op == '-': exact = x - y
    if op == '*': exact = x * y
    if op == '**' and y >= 0 and abs(x) > 1: exact = x ** min(y, 64)
    if abs(exact) >= 2**53:
        raise Fault(SOFT)
    fa, fb = float(p), float(q)
    if op == '+': return num.Num(fa + fb)
    if op == '-': return num.Num(fa - fb)
    if op == '*': return num.Num(fa * fb)
    if op == '**': return num.Num(libm.pow(fa, fb))
    if fb == 0.0:
        raise Fault('division by zero')
    return num.Num(fa / fb)

def negate(v):
    if not is_str(v):
        return -v if is_num(v) else num.Int(-v)
    n, _ = as_number(v)
    if v.startswith('+'):
        raise Fault(NEG_PLUS)
    x = float(n)
    if x == math.trunc(x) and abs(x) >= 2**53:
        raise Fault(NEG_LARGE)
    return -x

def to_str(v):
    return v if is_str(v) else num.printed(v)

def whole(v):
    n, _ = as_number(v)
    t = math.trunc(n)
    if not MIN <= t <= MAX:
        raise Fault(OUTSIDE)
    return t

def repeat(a, b):
    s = to_str(a)
    n, _ = as_number(b)
    if n < 0:
        raise Fault(NEGATIVE_COUNT)
    count = whole(n)
    if count * len(s) > 2**31 - 1:
        raise Fault(TOO_LONG)
    return s * count

def length(v):
    return len(to_str(v))

def case(change, name):
    def f(v):
        s = to_str(v)
        if any(ord(c) > 0x7f for c in s):
            raise Fault(f'{name} of a character past ASCII')
        return change(s)
    return f

def ord_(v):
    s = to_str(v)
    return ord(s[0]) if s else 0

def chr_(v):
    n, _ = as_number(v)
    if n < 0:
        raise Fault(NOT_A_CHARACTER)
    t = math.trunc(n)
    if t > 0x10ffff or 0xd800 <= t <= 0xdfff:
        raise Fault(NOT_A_CHARACTER)
    return chr(t)

def substr(v, offset, count=None):
    s = to_str(v)
    off = whole(offset)
    n = None if count is None else whole(count)
    size = len(s)
    start = off + size if off < 0 else off
    end = size if n is None else start + n if n >= 0 else size + n
    if start > size or (start < 0 and end < 0):
        raise Fault(SUBSTR)
    start = max(start, 0)
    end = min(end, size)
    end = max(end, start)
    return s[start:end]

def index(v, w, position=0):
    s = to_str(v)
    t = to_str(w)
    p = whole(position)
    p = min(max(p, 0), len(s))
    return s.find(t, p)

BUILTINS = {
    'length': length, 'uc': case(str.upper, 'uc'), 'lc': case(str.lower, 'lc'), 'ord': ord_, 'chr': chr_,
    'substr': substr, 'index': index,
}

# An expression is a value; ('-', e) or ('+', e); (op, left, right); or
# ('call', name, [arguments]).
def value(e):
    if not isinstance(e, tuple):
        return e
    if e[0] == 'call':
        args = [value(a) for a in e[2]]
        return BUILTINS[e[1]](*args)
    if len(e) == 2:
        v = value(e[1])
        return v if e[0] == '+' else negate(v)
    op, left, right = e
    a = value(left)
    b = value(right)
    if op == '.':
        s = to_str(a)
        return s + to_str(b)
    if op == 'x':
        return repeat(a, b)
    return arith(op, a, b)

def noncharacter(c):
    return 0xfdd0 <= ord(c) <= 0xfdef or ord(c) & 0xfffe == 0xfffe

def printed(v, use_open):
    """What `print` writes for a value, as a string, or the fault."""
    s = to_str(v)
    if any(noncharacter(c) for c in s):
        raise Fault(NONCHARACTER)
    if not use_open and any(ord(c) > 0x7f for c in s):
        raise Fault(PAST_ASCII)
    return s

def literal(s):
    if s and all(' ' <= c <= '~' and c not in "'\\" for c in s):
        return f"'{s}'"
    out = ''
    for c in s:
        if c == '\n': out += '\\n'
        elif c == '\t': out += '\\t'
        elif c in '"\\$@': out += '\\' + c
        elif ' ' <= c <= '~': out += c
        else: out += '\\x{%X}' % ord(c)
    return f'"{out}"'

def text(e, top=True):
    """The expression as source."""
    if is_str(e):
        return literal(e)
    if not isinstance(e, tuple):
        return num.text(e, top)
    if e[0] == 'call':
        return f'{e[1]}({", ".join(text(a) for a in e[2])})'
    if len(e) == 2:
        s = f'{e[0]}{text(e[1], False)}'
        return s if top else f'({s})'
    op, left, right = e
    s = f'{text(left, False)} {op} {text(right, False)}'
    return s if top else f'({s})'

# ---- the values

# Strings that are numbers, or nearly: each way of writing one, and the
# edges of each class: 2^53, where a double stops holding every whole
# number; 10^15, where a whole Num stops printing one way; the ends of the
# Ints.
DIGITS = ['0', '1', '7', '12', '-12', '+12', ' 12 ', '012', '-0', '00', '12\n', '2147483648', '999999999999999',
          '1000000000000000', '9007199254740991', '9007199254740992', '9007199254740993', '-9007199254740992',
          '10000000000000000', '4611686018427387904', '9223372036854775807', '-9223372036854775807',
          '-9223372036854775808']
POINTS = ['3.0', '5.', '0.0', '-0.0', '10.00', '+3.0', ' 3.0 ', '2.0', '-1.0', '.5', '1.5', '-2.5', '0.1', '3.7',
          '999999999999999.0', '1000000000000000.0', '9007199254740991.0', '9007199254740992.0',
          '10000000000000000.0', '0.000001']
EXPONENTS = ['1e3', '1.5e1', '1e0', '1E3', '-1e3', '+1e2', '0e0', '-0e0', '1e15', '9007199254740991e0', '1e16',
             '1e-3', '1.5e-1', '2.5e0', '1e300', '1e-400', '.5e1', '5.e1']
STRINGS = DIGITS + POINTS + EXPONENTS
NUMBERS = [0, 1, -1, 2, 3, 7, 10, 2**31, 10**15, 9007199254740988, 9007199254740990, 2**53 - 1, 2**53, 2**53 + 1,
           10**16, 10**16 + 1, 2**62, MAX, MIN + 1, MIN,
           0.0, -0.0, 0.5, 1.0, 1.5, -2.5, 3.0, 0.1, 1e15, 2.0**53, 1e16, 1e300]
# For `**`, which turns on the base's bits and the power.
BASES = ['0', '1', '-1', '2', '-2', '3', '10', '2.0', '3.0', '-3.0', '10.0', '1.5', '1e1', '2e0', '0.0', ' 7 ']
POWERS = [0, 1, 2, 3, 10, 15, 16, 33, 34, 52, 53, 62, 63, 64, -1, -2, 0.5, 2.0, '0', '2', '2.0', '3.0', '-1', '-1.0',
          '0.5', '1e1', '33', '34', '53.0', '64']
# Every way of writing a number in a string that perl takes in silence.
FORMS = ['0', '00', '007', '12', '+12', '-12', ' 12', '12 ', '\t12\n', '\n12', '12\r', '\f12', '12\v', '\v12\f',
         ' \t\n\r\f\v12 \t\n\r\f\v', '-0', '+0', '1.5', '+1.5', '-1.5', '.5', '-.5', '+.5', '5.', '-5.', '0.5', '00.5',
         '1.50', '1.0', '100.000', '0.0', '-0.0', '.0', '0.', '1e3', '1E3', '1e+3', '1e-3', '1e03', '1e0', '1e00',
         '-1e3', '+1e3', '1.5e3', '.5e3', '5.e3', '1.5E-3', ' 1e3 ', '0e0', '0e5', '0.0e0', '-0e0', '1e-400', '-1e-400',
         '4.9e-324', '1e308', '1.7976931348623157e308', '0.1', '0.30000000000000004', '123456789012345678',
         '0.000001', '1e15', '123456.789e-3', '9007199254740991', '9007199254740991.5', '12345678901234567890.5',
         '100000000000000000000.0', '1e21', '1.5e300', '000000000000000000000000000012', '0000000000000000000000.5']
# Strings for the string operators: empty, plain, with every kind of
# character (one, two, three and four bytes of UTF-8), a NUL, a newline,
# and what a double-quoted literal has to escape.
TEXTS = ['', 'a', 'abc', 'Hello, World', ' ', 'a b', '12', '3.0', '-5', 'it\'s', 'say "hi"', '$x @y \\', 'a\nb', '\t',
         '\x00', 'a\x00b', '\x7f', '\xe9', 'h\xe9llo', '☺', 'a\xe9☺\U0001f600z', '\x80\xffĀ', '�']
VALUES = [0, 7, -12, MAX, MIN, 0.0, -0.0, 0.5, -2.5, 1.5e300, 1e-5, 0.1, 999999999999999.0, 2.0**53, 1e21, 1 / 3]

def with_answers(exprs, use_open=True, steady_only=False):
    """(expression, what say prints) for each that has an answer that
    prints."""
    out = []
    for e in exprs:
        try:
            v = value(e)
            if steady_only and not num.steady(v):
                continue
            out.append((e, printed(v, use_open)))
        except Fault:
            pass
    return out

def pairs(op):
    if op == '**':
        return [(a, b) for a in BASES for b in POWERS] + [(a, b) for a in (2, 3, 10, 2.0, 1.5) for b in POWERS if is_str(b)]
    # Thinned, to keep a test to about three thousand lines: every string
    # is a left operand of every number, and every class of string is on
    # the right.
    mixed = [(a, b) for a in STRINGS for b in NUMBERS] + [(a, b) for a in NUMBERS for b in STRINGS[::2]]
    return mixed + [(a, b) for a in STRINGS for b in STRINGS[1::3]]

def bracketed(e):
    return ('.', ('.', '[', e), ']')

def substr_cases(two):
    out = []
    for s in ['abcde', '', 'a', 'h\xe9llo☺', 12345, 2.5]:
        size = len(to_str(s))
        for off in range(-size - 3, size + 4):
            if two:
                out.append(bracketed(('call', 'substr', [s, off])))
            else:
                out += [bracketed(('call', 'substr', [s, off, n])) for n in range(-size - 3, size + 4)]
    return out

def index_cases():
    out = []
    for s in ['abcabc', '', 'a', 'h\xe9llo☺\xe9', 121]:
        for t in ['', 'a', 'bc', 'c', 'abcabc', 'abcabcd', '\xe9', '☺\xe9', 'x', 1, 12]:
            out.append(('call', 'index', [s, t]))
            out += [('call', 'index', [s, t, p]) for p in range(-3, len(to_str(s)) + 4)]
    return out

# Where a whole number is wanted: Nums and strings that have to be cut.
WHOLES = [0, 1, 2, 3, 0.0, -0.0, 0.5, 0.999, 1.0, 1.9, 2.0, 2.7, 3.999999, '0', '1', '2', ' 2 ', '2.0', '2.7', '1e0',
          '2e0', '.9', '1.9', '+1', '02', '2.', '25e-1', '9223372036854775807']
BELOW = [-1, -2, -0.5, -1.5, -2.9, '-1', '-0.5', '-1.9', '-2', '-1e0', '-0', '-0.0', -9223372036854775807]

def whole_cases():
    out = [bracketed(('x', 'ab', n)) for n in WHOLES[:-1]]
    out += [('call', 'ord', [('call', 'chr', [n])]) for n in WHOLES[:-1] + [65.9, '65', '65.9', ' 65 ', '6.5e1', 1114111.9]]
    for n in WHOLES + BELOW:
        out.append(bracketed(('call', 'substr', ['abcde', n])))
        out.append(bracketed(('call', 'substr', ['abcde', 1, n])))
        out.append(('call', 'index', ['abcabc', 'c', n]))
    return out

def print_cases():
    """(print or say, expression): what goes to stdout, a statement after
    another."""
    out = [('say', t) for t in TEXTS] + [('print', t) for t in TEXTS] + [('say', '')]
    out += [('print', 'a'), ('print', 'b'), ('print', 1), ('print', 2.5), ('say', ('.', 'c', 'd')), ('print', '\n'),
            ('print', ('x', 'ab', 3)), ('print', ''), ('say', ('call', 'chr', [0x10fffd])), ('say', ('call', 'chr', [0xfdcf])),
            ('say', ('call', 'chr', [0xfdf0])), ('say', ('call', 'chr', [0xd7ff])), ('say', ('call', 'chr', [0xe000])),
            ('say', ('call', 'chr', [0x80])), ('say', ('call', 'chr', [0x7ff])), ('say', ('call', 'chr', [0x800])),
            ('say', ('call', 'chr', [0xffff - 2])), ('say', ('call', 'chr', [0x10000])), ('say', '\x85\xa0 ')]
    return out

# number: (name, the expressions)
def same(number):
    arithmetic = {'100': ('str-add', '+'), '101': ('str-sub', '-'), '102': ('str-mul', '*'), '103': ('str-div', '/'),
                  '104': ('str-mod', '%'), '105': ('str-pow', '**')}
    if number in arithmetic:
        name, op = arithmetic[number]
        return name, with_answers([(op, a, b) for a, b in pairs(op)], steady_only=op == '**')
    if number == '106':
        every = STRINGS + FORMS + TEXTS
        return 'str-neg', with_answers([('-', s) for s in every] + [('+', s) for s in every] + [('-', ('-', s)) for s in STRINGS])
    if number == '107':
        every = TEXTS + VALUES
        return 'str-concat', with_answers([('.', a, b) for a in every for b in every])
    if number == '108':
        counts = [0, 1, 2, 3, 10]
        return 'str-repeat', with_answers([bracketed(('x', a, n)) for a in TEXTS + VALUES for n in counts]
                                          + [('call', 'length', [('x', 'abc', n)]) for n in (1000, 65536, 715827882)]
                                          + [bracketed(('x', '', n)) for n in (2**31, 2**62, MAX)])
    if number == '109':
        every = TEXTS + VALUES + STRINGS
        codes = [0, 1, 9, 10, 32, 65, 97, 126, 127, 128, 255, 256, 0x7ff, 0x800, 0xd7ff, 0xe000, 0xfdcf, 0xfdd0, 0xfdef,
                 0xfdf0, 0xfffd, 0xfffe, 0xffff, 0x10000, 0x1f600, 0x1fffe, 0x10fffd, 0x10ffff]
        return 'str-chars', with_answers(
            [('call', 'length', [v]) for v in every] + [('call', 'ord', [v]) for v in every]
            + [('call', 'ord', [('call', 'chr', [c])]) for c in codes] + [('call', 'length', [('call', 'chr', [c])]) for c in codes]
            + [('call', 'length', [('.', ('call', 'chr', [c]), ('call', 'chr', [d]))]) for c in codes for d in codes[::5]])
    if number == '110':
        ascii_ = ''.join(chr(c) for c in range(128))
        every = [t for t in TEXTS + VALUES] + [ascii_, 'MiXeD 123 case', 'ALL CAPS', 'no caps']
        return 'str-case', with_answers([bracketed(('call', f, [v])) for f in ('uc', 'lc') for v in every]
                                        + [('call', 'uc', [('call', 'lc', ['MiXeD'])]), ('call', 'lc', [('call', 'uc', ['MiXeD'])])])
    if number == '111':
        return 'str-substr', with_answers(substr_cases(True))
    if number == '112':
        return 'str-substr-length', with_answers(substr_cases(False))
    if number == '113':
        return 'str-index', with_answers(index_cases())
    if number == '114':
        return 'str-whole', with_answers(whole_cases())
    if number == '116':
        out = []
        for s in FORMS:
            out += [('+', s, 0), ('*', s, 1), ('-', 0, s), ('/', s, 1), ('%', s, 7), ('+', s, 0.5), ('.', s, ''),
                    ('call', 'length', [s]), ('*', s, '1'), ('+', s, s)]
        return 'str-forms', with_answers(out)
    raise KeyError(number)

SAME = {'100': 'str-add', '101': 'str-sub', '102': 'str-mul', '103': 'str-div', '104': 'str-mod', '105': 'str-pow',
        '106': 'str-neg', '107': 'str-concat', '108': 'str-repeat', '109': 'str-chars', '110': 'str-case',
        '111': 'str-substr', '112': 'str-substr-length', '113': 'str-index', '114': 'str-whole', '116': 'str-forms'}

def call(name, *args):
    return ('call', name, list(args))

# number: (name, a near expression that prints, the one that faults,
# whether the program has the `use open` line)
FAULTS = {
    '120': ('not-numeric', ('+', '12', 1), ('+', 'abc', 1)),
    '121': ('not-numeric-empty', ('.', '', 1), ('*', 2, '')),
    '122': ('not-numeric-trailing', ('+', '12 ', 1), ('+', '12abc', 1)),
    '123': ('not-numeric-hex', ('+', '10', 1), ('+', '0x10', 1)),
    '124': ('not-numeric-underscore', ('+', '1000', 1), ('+', '1_000', 1)),
    '125': ('not-numeric-inf', ('+', '1.5', 1), ('+', 'Inf', 1)),
    '126': ('not-numeric-nan', ('*', '0', 0), ('*', 'NaN', 0)),
    '127': ('not-numeric-but-true', ('+', '0', 5), ('+', '0 but true', 5)),
    '128': ('not-numeric-nul', ('+', '3\v', 1), ('+', '3\x00', 1)),
    '129': ('not-numeric-digit', ('+', '3', 1), ('+', '٣', 1)),
    '130': ('string-overflow', ('+', '9223372036854775807', 0), ('+', '9223372036854775808', 0)),
    '131': ('string-overflow-negative', ('+', '-9223372036854775808', 0), ('+', '-9223372036854775809', 0)),
    '132': ('string-float-overflow', ('*', '1' + '0' * 308 + '.0', 1), ('*', '1e309', 1)),
    '133': ('string-exponent', ('+', '9007199254740991e0', 1), ('+', '1e16', 1)),
    '134': ('two-answers-string', ('+', 9007199254740993, '1'), ('+', 9007199254740992, '1')),
    '135': ('two-answers-two-strings', ('*', '9007199254740993', '1'), ('*', '9007199254740992', '1')),
    '136': ('soft-add', ('+', '3.0', 999999999999996), ('+', '3.0', 9007199254740990)),
    '137': ('soft-operand', ('-', '3.0', 999999999999999), ('-', '3.0', 9007199254740993)),
    '138': ('soft-mul', ('*', '3.0', 333333333333333), ('*', '3.0', 3002399751580331)),
    '139': ('soft-pow', ('**', '3.0', 31), ('**', '3.0', 34)),
    '140': ('soft-div', ('/', '6.0', 3), ('/', '6.0', 9007199254740993)),
    '141': ('neg-plus', ('-', '5'), ('-', '+5')),
    '142': ('neg-large', ('-', '999999999999999'), ('-', '9007199254740992')),
    '143': ('neg-not-numeric', ('+', 'foo'), ('-', 'foo')),
    # The answer is a Num, whatever the string: as an Int this one would print.
    '169': ('neg-whole-float', ('-', '999999999999999'), ('-', '1000000000000000')),
    '144': ('substr-outside', bracketed(call('substr', 'abc', 3)), call('substr', 'abc', 4)),
    '145': ('substr-outside-length', bracketed(call('substr', 'abc', 3, 1)), call('substr', 'abc', 4, 1)),
    '166': ('substr-outside-before', bracketed(call('substr', 'abc', -5, 2)), call('substr', 'abc', -5, 1)),
    '167': ('substr-outside-before-negative', bracketed(call('substr', 'abc', -5, -3)), call('substr', 'abc', -5, -4)),
    '168': ('substr-outside-empty', bracketed(call('substr', '', -1, 1)), call('substr', '', -1, 0)),
    '146': ('repeat-negative', bracketed(('x', 'a', -0.0)), ('x', 'a', -1)),
    '147': ('repeat-negative-fraction', bracketed(('x', 'a', 0.5)), ('x', 'a', -0.5)),
    '148': ('repeat-too-long', call('length', ('x', 'ab', 1000)), call('length', ('x', 'ab', 2**30))),
    '149': ('chr-past-unicode', call('length', call('chr', 0x10ffff)), call('length', call('chr', 0x110000))),
    '150': ('chr-surrogate', call('ord', call('chr', 0xd7ff)), call('ord', call('chr', 0xd800))),
    '151': ('chr-negative', call('ord', call('chr', -0.0)), call('ord', call('chr', -0.5))),
    '152': ('whole-outside', bracketed(call('substr', 'abc', 0, MAX)), call('substr', 'abc', 0, 1e30)),
    '153': ('whole-outside-index', call('index', 'abc', 'c', MAX), call('index', 'abc', 'c', 1e30)),
    '154': ('whole-outside-repeat', bracketed(('x', '', 2**62)), ('x', '', 1e30)),
    '155': ('print-past-ascii', '\x7f', '\xe9'),
    '156': ('print-noncharacter', '�', '￾', True),
    '157': ('print-noncharacter-high', call('chr', 0x1fffd), call('chr', 0x1ffff), True),
    '158': ('uc-past-ascii', call('uc', 'e'), call('uc', '\xe9')),
    '159': ('lc-past-ascii', call('lc', 'E'), call('lc', 'aİ')),
    '160': ('concat-whole-float', ('.', 'a', 999999999999999.0), ('.', 'a', 1e15)),
    '161': ('length-whole-float', call('length', 2.0**53), call('length', 2.0**52)),
    # The left operand's fault is the one that happens, and an argument's
    # before the next one's.
    '162': ('fault-order', ('.', ('+', '1', 1), ('x', 'a', 1)), ('.', ('+', 'abc', 1), ('x', 'a', -1))),
    '163': ('fault-order-arguments', call('substr', ('x', 'ab', 2), ('+', '1', 1)), call('substr', ('x', 'ab', -2), ('+', 'abc', 1))),
    # Each argument is worked out before any is made a string or a number;
    # then they are, the first first.
    '165': ('fault-order-conversions', call('substr', 1e14, '1'), call('substr', 1e15, 'x')),
    '164': ('fault-order-operands', ('+', '1', '2'), ('+', '', '1e16')),
}

def name_of(number):
    return SAME[number] if number in SAME else 'str-print' if number == '115' else FAULTS[number][0]

def commands():
    out = ''
    for number in sorted(list(SAME) + ['115'] + list(FAULTS)):
        stem = f't/{number}-{name_of(number)}'
        out += f'    python3 t/models/str.py --program {number} > {stem}.pl\n'
        out += f'    python3 t/models/str.py {number} > {stem}.expected\n'
    return out

OPEN = "use open ':std', ':encoding(UTF-8)';\n"

def program(statements, header, use_open):
    return (''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + (OPEN if use_open else '')
            + ''.join(f'{word}({text(e)});\n' for word, e in statements))

def main(argv):
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    # The list in the docstring is what t/checks.py reads, so it has to be
    # the whole list.
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/str.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/str.py']
    if number in SAME:
        name, lines = same(number)
        assert name == SAME[number]
        if want_program:
            out.write(program([('say', e) for e, _ in lines], model, True).encode())
        else:
            out.write(''.join(f'{p}\n' for _, p in lines).encode())
        return
    if number == '115':
        statements = print_cases()
        if want_program:
            out.write(program(statements, model, True).encode())
        else:
            out.write(''.join(printed(value(e), True) + ('\n' if word == 'say' else '') for word, e in statements).encode())
        return
    name, near, far, *rest = FAULTS[number]
    use_open = bool(rest)
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    # A line that prints, the near one that prints, the fault, and a line
    # the program never reaches (which perl does).
    lines = [1, near, far, 2]
    if want_program:
        out.write(program([('say', e) for e in lines], header, use_open).encode())
        return
    result = ''
    for n, e in enumerate(lines):
        try:
            result += printed(value(e), use_open) + '\n'
        except Fault as f:
            line = len(header) + 1 + (1 if use_open else 0) + n + 1
            result += f'fault: {f} at {path} line {line}.\nexit: 1\n'
            break
    assert 'fault:' in result and result.count('\n') == 4, (number, result)
    out.write(result.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

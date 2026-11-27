#!/usr/bin/env python3
"""t/2700 to t/2703: sprintf and printf (step 16b; D124 to D128, D131).

The definition, which is all this file knows of formats:

  the format     a string literal; its text as it is, and each conversion
                 replaced by what it makes of the next values
  %%             a percent sign
  %s             the value made a string as `.` makes one; a precision
                 keeps that many characters, a width pads to that many,
                 with blanks before (zeros with `0`), or after with `-`
  %c             the character whose number the value is
  %d             the value cut toward zero to a whole number: a sign
                 (`-`, or `+` or a blank by the flags), then the digits,
                 at least the precision of them; padded as %s, with zeros
                 between the sign and the digits under `0` when there is
                 no precision
  %u %o %x %X    the same with no sign: a negative Int as its 64 bits, a
  %b %B          Num up to 2^64 as the whole number it is; `#` puts 0x,
                 0X, 0b, 0B before a value that isn't zero, and makes
                 the first digit of an octal 0
  %e %E %f %g %G the value as a double, as C prints it; but a bare %.0f
                 (no flag, no width) is perl's own: add a half, cut, and
                 step back from an odd number the half made (T280)
  *              a width or precision taken from the list first; a
                 negative width is `-`, a negative precision none

Integers are formatted here by hand, and floats by Python's `%`, which is
C's for doubles (and not for integers: `%.0d`, `%#o`, `%u` of -1). perl
is the second derivation (t/checks.py oracle).

2700 is the integer conversions, 2701 the floats, 2702 strings,
characters, stars, printf and lists, 2703 the edges.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/fmt.py --program 2700 > t/2700-format-integers.pl
    python3 t/models/fmt.py 2700 > t/2700-format-integers.expected
    python3 t/models/fmt.py --program 2701 > t/2701-format-floats.pl
    python3 t/models/fmt.py 2701 > t/2701-format-floats.expected
    python3 t/models/fmt.py --program 2702 > t/2702-format-strings-stars-printf.pl
    python3 t/models/fmt.py 2702 > t/2702-format-strings-stars-printf.expected
    python3 t/models/fmt.py --program 2703 > t/2703-format-edges.pl
    python3 t/models/fmt.py 2703 > t/2703-format-edges.expected
"""

import math
import random
import struct
import sys

TWO_63 = 2 ** 63


# ---- values: (the language's spelling, its kind, what it is)
# kind 'int' an Int, 'num' a Num (a Python float), 'str' a string and the
# number it is, 'bool' true or false.
def num_text(x):
    """A Num as the language prints it (C's %.15g), for %s."""
    if x == 0:
        return '0'
    t = '%.15g' % x
    return t


def as_number(v):
    kind, val = v[1], v[2]
    if kind == 'str':
        return val[1]
    if kind == 'bool':
        return 1 if val else 0
    return val


def as_string(v):
    kind, val = v[1], v[2]
    if kind == 'str':
        return val[0]
    if kind == 'bool':
        return '1' if val else ''
    if kind == 'int':
        return str(val)
    return num_text(val)


def I(n):
    return (str(n) if n >= 0 else f'({n})' if n != -TWO_63 else '(-9223372036854775807 - 1)', 'int', n)


def N(x, text=None):
    return (text or repr(x), 'num', x)


def S(s, number):
    return ('"' + s + '"', 'str', (s, number))


TRUE = ('true', 'bool', True)
FALSE = ('false', 'bool', False)


# ---- the conversions
class Spec:
    def __init__(self, flags='', width=None, precision=None, conv='d'):
        self.flags, self.width, self.precision, self.conv = flags, width, precision, conv

    def text(self):
        w = '' if self.width is None else str(self.width)
        p = '' if self.precision is None else '.' + str(self.precision)
        return '%' + self.flags + w + p + self.conv


def pad(spec, sign, digits, zeros_ok=True):
    left = '-' in spec.flags
    width = spec.width or 0
    body = sign + digits
    n = max(0, width - len(body))
    if left:
        return body + ' ' * n
    if '0' in spec.flags and zeros_ok:
        return sign + '0' * n + digits
    return ' ' * n + body


def whole(v):
    """The value cut toward zero, as %d takes it."""
    x = as_number(v)
    return int(x) if isinstance(x, int) else int(math.trunc(x))


def fmt_integer(spec, v):
    conv = spec.conv
    n = whole(v)
    if conv == 'd':
        u, negative = abs(n), n < 0
    else:
        u, negative = n % (2 ** 64), False
    base = {'o': 8, 'x': 16, 'X': 16, 'b': 2, 'B': 2}.get(conv, 10)
    digits = ''
    if not (u == 0 and spec.precision == 0):
        w = u
        while True:
            digits = '0123456789abcdef'[w % base] + digits
            w //= base
            if w == 0:
                break
    if conv == 'X':
        digits = digits.upper()
    if spec.precision is not None and len(digits) < spec.precision:
        digits = '0' * (spec.precision - len(digits)) + digits
    sign = ''
    if conv == 'd':
        sign = '-' if negative else '+' if '+' in spec.flags else ' ' if ' ' in spec.flags else ''
    elif '#' in spec.flags and u != 0 and base == 16:
        sign = '0X' if conv == 'X' else '0x'
    elif '#' in spec.flags and u != 0 and base == 2:
        sign = '0B' if conv == 'B' else '0b'
    if conv == 'o' and '#' in spec.flags and not digits.startswith('0'):
        digits = '0' + digits
    return pad(spec, sign, digits, zeros_ok=spec.precision is None)


def f0convert(nv):
    neg = nv < 0
    if neg:
        nv = -nv
    if nv != 0.0 and nv < 18446744073709551615.0:
        uv = int(nv)
        if uv != nv:
            nv = nv + 0.5
            uv = int(nv)
            if uv & 1 and uv == nv:
                uv -= 1
        return ('-' if neg else '') + str(uv)
    return None


def fmt_float(spec, v):
    d = float(as_number(v))
    if spec.conv == 'f' and spec.flags == '' and spec.width is None and spec.precision == 0:
        r = f0convert(d)
        if r is not None:
            return r
    p = 6 if spec.precision is None else spec.precision
    return ('%' + spec.flags + str(spec.width or 0) + '.' + str(p) + spec.conv) % d


def fmt_string(spec, v):
    s = as_string(v)
    if spec.precision is not None:
        s = s[:spec.precision]
    return pad(spec, '', s)


def fmt(spec, v):
    if spec.conv in 'duoxXbB':
        return fmt_integer(spec, v)
    if spec.conv in 'eEfgG':
        return fmt_float(spec, v)
    if spec.conv == 'c':
        return chr(whole(v))
    return fmt_string(spec, v)


def perl_str(s):
    """s as a double-quoted literal of the language."""
    out = ''
    for ch in s:
        if ch in '"\\$@':
            out += '\\' + ch
        elif ch == '\n':
            out += '\\n'
        else:
            out += ch
    return '"' + out + '"'


# ---- the cases
INTS = [I(0), I(1), I(-1), I(7), I(-42), I(255), I(-255), I(4096), I(TWO_63 - 1), I(-TWO_63), I(123456789)]
NUMS = [N(3.7), N(-3.7), N(0.5), N(2.5), N(-0.4), N(1e10), N(1234.5), N(9.75)]
INT_FLAGS = ['', '-', '+', ' ', '0', '#', '-#', '+0', '0#', '-0', '+ ', '#0', '- ']


def case_integers(rnd):
    lines, out = [], []
    for conv in 'duoxXbB':
        for v in INTS + [N(3.7), N(-3.7), S('42', 42), S(' 12 ', 12), S('-9', -9), TRUE, FALSE]:
            for _ in range(3):
                spec = Spec(rnd.choice(INT_FLAGS), rnd.choice([None, None, 1, 4, 9, 24]), rnd.choice([None, None, 0, 1, 3, 12]), conv)
                lines.append(f'say "[", sprintf("{spec.text()}", {v[0]}), "]";')
                out.append('[' + fmt(spec, v) + ']')
        for spec in [Spec(precision=0, conv=conv), Spec('#', precision=0, conv=conv), Spec('#', conv=conv), Spec('+', precision=0, conv=conv)]:
            lines.append(f'say "[", sprintf("{spec.text()}", 0), "]";')
            out.append('[' + fmt(spec, I(0)) + ']')
    return lines, out


FLOATS = [I(0), I(1), I(-1), I(42), I(TWO_63 - 1), N(0.5), N(1.5), N(2.5), N(-2.5), N(0.1), N(1 / 3, '1/3'), N(1234.5), N(1e-5), N(1e100),
          N(-123.456), N(6.02e23), N(0.0001), N(100000.0, '100000.0'), N(1e15, '1e15'), N(9.999), S('3.25', 3.25), S('1e3', 1000), S(' -2 ', -2), TRUE, FALSE]
FLOAT_FLAGS = ['', '-', '+', ' ', '0', '#', '-+', '0#', '+0', '- #']


def case_floats(rnd):
    lines, out = [], []
    for conv in 'eEfgG':
        for v in FLOATS:
            for _ in range(2):
                spec = Spec(rnd.choice(FLOAT_FLAGS), rnd.choice([None, None, 1, 8, 15]), rnd.choice([None, None, 0, 1, 3, 10]), conv)
                lines.append(f'say "[", sprintf("{spec.text()}", {v[0]}), "]";')
                out.append('[' + fmt(spec, v) + ']')
    for v in FLOATS:
        spec = Spec(precision=0, conv='f')
        lines.append(f'say "[", sprintf("%.0f", {v[0]}), "]";')
        out.append('[' + fmt(spec, v) + ']')
    return lines, out


STRS = [S('abc', None), S('', None), S('héllo', None), S('☺x', None), I(42), I(-7), N(3.25), N(0.1), TRUE, FALSE]


def case_strings(rnd):
    lines, out = [], []
    for v in STRS:
        for _ in range(4):
            spec = Spec(rnd.choice(['', '-', '0', '-0']), rnd.choice([None, 1, 3, 8]), rnd.choice([None, 0, 1, 2, 10]), 's')
            lines.append(f'say "[", sprintf("{spec.text()}", {v[0]}), "]";')
            out.append('[' + fmt(spec, v) + ']')
    for n in [65, 97, 0x263A, 0xE9, 0x1F600, 48, 126]:
        lines.append(f'say "[", sprintf("%c", {n}), "]";')
        out.append('[' + chr(n) + ']')
    lines.append('say sprintf("%c%c|%c", 72, 105, 3.9 + 62);')
    out.append('Hi|A')
    # Stars: a width or a precision from the list, before the value.
    for w, p, conv, v in [(5, None, 'd', I(42)), (-5, None, 'd', I(42)), (None, 2, 'f', N(3.14159)), (None, -2, 'f', N(1.25)),
                          (6, 2, 'f', N(2.5)), (-6, 1, 'e', N(12345.0)), (4, None, 's', S('ab', None)), (-4, None, 's', S('ab', None)),
                          (None, 1, 's', S('abc', None)), (None, -1, 's', S('abc', None)), (0, None, 'x', I(255)), (3, 3, 'd', I(-7)),
                          (N(2.9), None, 's', S('a', None)), (S('3', 3), None, 'd', I(5))]:
        flags = ''
        width = None if w is None else (w if isinstance(w, int) else whole(w))
        spec = Spec(flags, None if width is None else abs(width), None if p is None or p < 0 else p, conv)
        if width is not None and width < 0:
            spec.flags = '-'
        star = '%' + ('*' if w is not None else '') + ('.*' if p is not None else '') + conv
        args = ([str(w) if isinstance(w, int) and w >= 0 else f'({w})' if isinstance(w, int) else w[0]] if w is not None else []) + \
               ([str(p) if p >= 0 else f'({p})'] if p is not None else []) + [v[0]]
        lines.append(f'say "[", sprintf("{star}", {", ".join(args)}), "]";')
        out.append('[' + fmt(spec, v) + ']')
    # The text around the conversions, %%, and the list.
    lines += [
        'say sprintf("%d%% of %s, 100%%", 50, "it");',
        'say sprintf("no conversion at all");',
        "say sprintf('%s-%s', 'single', 'quotes');",
        'say sprintf(q(%s|%s), "q", "too");',
        'say sprintf "%s and %s", "no", "brackets";',
        '{ my @l = (1, 2, 3); say sprintf("%d+%d=%d", @l); }',
        '{ my @l = ("a", "b"); say sprintf("%s%s%s", @l, scalar(@l)); }',
        '{ my %h = (k => "v"); say sprintf("%s=%s", "k", $h{k}); }',
        'say join(",", map { sprintf("%03d", $_) } 1 .. 3);',
        'say sprintf("%s", sprintf("%5s", "in")) . "|";',
        'printf("%s|%d\\n", "printf", 7);',
        'printf "%-4s|\\n", "no";',
        'printf("%s\\n", "under an if") if 1;',
        'printf("plain\\n");',
        'printf(<<END, "heredoc");\n%s format\nEND',
        'say sprintf("é%sé", "x");',
        'say sprintf("\\x25d", 5);',
    ]
    out += ['50% of it, 100%', 'no conversion at all', 'single-quotes', 'q|too', 'no and brackets', '1+2=3', 'ab2', 'k=v',
            '001,002,003', '   in|', 'printf|7', 'no  |', 'under an if', 'plain', 'heredoc format', 'éxé', '5']
    return lines, out


def case_edges(rnd):
    lines, out = [], []
    # perl's own %.0f (T280), and C's with a width or a flag.
    for x, text in [(0.5000000000000001, '0.5000000000000001'), (-0.5000000000000001, '-0.5000000000000001'), (0.5, '0.5'), (1.5, '1.5'),
                    (2.5, '2.5'), (3.5, '3.5'), (-2.5, '-2.5'), (4503599627370497.0, '4503599627370497.0'), (2.5000000000000004, '2.5000000000000004'),
                    (1.4999999999999998, '1.4999999999999998'), (1e20, '1e20'), (18446744073709549568.0, '18446744073709549568.0'), (0.49999999999999994, '0.49999999999999994')]:
        v = N(x, text)
        for spec in [Spec(precision=0, conv='f'), Spec(width=1, precision=0, conv='f'), Spec('+', precision=0, conv='f'), Spec(' ', precision=0, conv='f')]:
            lines.append(f'say "[", sprintf("{spec.text()}", {text}), "]";')
            out.append('[' + fmt(spec, v) + ']')
    lines.append('say "[", sprintf("%.*f", 0, 0.5000000000000001), "]";')
    out.append('[' + f0convert(0.5000000000000001) + ']')
    # The ends of the ranges (D127): %d an Int, the unsigned ones up to 2^64.
    for text, x in [('9223372036854774784.0', 9223372036854774784.0), ('-9223372036854775808.0', -9223372036854775808.0),
                    ('18446744073709549568.0', 18446744073709549568.0), ('9223372036854775808.0', 9223372036854775808.0), ('-1.5', -1.5)]:
        v = N(x, text)
        convs = 'duxob' if abs(x) < TWO_63 else 'uxob'
        for conv in convs:
            spec = Spec(conv=conv)
            lines.append(f'say "{conv}: ", sprintf("%{conv}", {text});')
            out.append(f'{conv}: ' + fmt(spec, v))
    for conv in 'uxXob':
        spec = Spec('#', conv=conv)
        lines.append(f'say sprintf("%#{conv}", -1);')
        out.append(fmt(spec, I(-1)))
    # Zero that is no negative zero: an Int, a string, a positive Num.
    for v in [I(0), N(0.0, '0.0'), S('0', 0), S('0.0', 0.0), FALSE]:
        for conv in 'efg':
            spec = Spec(conv=conv)
            lines.append(f'say sprintf("%{conv}", {v[0]});')
            out.append(fmt(spec, v))
    lines.append('{ my $z = 0; say sprintf("%g", -$z); }')
    out.append('0')
    # Repeated flags, as C has them.
    for f, v in [('--5', I(1)), ('++', I(1)), ('  ', I(1)), ('0-5', I(1)), ('#0#8', I(255))]:
        conv = 'x' if '#' in f else 'd'
        spec = Spec(''.join(sorted(set(f.rstrip('0123456789')) | ({'0'} if f.startswith('0') else set()))), int(''.join(ch for ch in f if ch.isdigit() and ch != '0') or 0) or None, None, conv)
        lines.append(f'say "[", sprintf("%{f}{conv}", {v[0]}), "]";')
        out.append('[' + fmt(spec, v) + ']')
    return lines, out


CASES = {2700: case_integers, 2701: case_floats, 2702: case_strings, 2703: case_edges}


def main(argv):
    program = argv[0] == '--program'
    n = int(argv[-1])
    lines, out = CASES[n](random.Random(n))
    if program:
        sys.stdout.write(f'# t/models/fmt.py {n}\nuse v5.42;\nuse utf8;\nuse open \':std\', \':encoding(UTF-8)\';\n' + '\n'.join(lines) + '\n')
    else:
        sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])

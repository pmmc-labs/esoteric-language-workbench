#!/usr/bin/env python3
"""t/070 to t/089: strings, D31 (the type), D32 (printing) and D33 (the six
operators), and what they lean on: D3, D6, D11, D12, D21 to D25.

070 print-escapes: a string holding every escape and every control character
    prints as D32 says: \\" \\\\ \\n \\t, the rest below U+0020 and U+007F as
    \\u{x}, lowercase and unpadded, whether the source wrote them as \\u{X}
    in capitals or padded or got them from str/char.
071 print-nonascii: characters past ASCII print as themselves, raw or from
    \\u{...} in the source: a combining accent, U+1F600, a ZWJ sequence,
    U+E000, U+FFFF, U+10000, U+10FFFF, and the C1 controls, U+2028, U+FEFF.
072 print-empty: the empty string prints "" (also from str/cat).
073 len: str/len of thirteen strings, packed into one integer (base 10).
074 at-all: str/at at every index of a string with characters past U+FFFF.
075 at-negative: (str/at s -1) faults bad index.
076 at-length: (str/at s 2) on a string of two characters faults bad index
    (a UTF-16 reading has three units, and index 2 would be a value).
077 lt: str/lt on pairs where code point order and UTF-16 order differ, on
    prefixes, and on equal strings, packed into one integer.
078 code-edges: str/code of the edge code points, as a weighted sum.
079 char-edges: str/char of the edge code points, joined and printed.
080 code-two: (str/code "e\\u{301}") faults not a character (two characters).
081 char-negative: (str/char -1) faults not a character.
082 char-surrogate: (str/char 55296), U+D800, faults not a character.
083 char-range: (str/char 1114112), U+110000, faults not a character.
084 not-a-string: (str/at 5 #true) faults not a string: operands are checked
    left to right, each for its type, before any range (D33).
085 not-an-integer: (str/at "ab" "x") faults not an integer.
086 eq-ne: == and != on strings, and on a string and another type, packed.
087 arith-string: an arithmetic operator given a string faults not an
    integer (D33, D11).
088 budget-edge: six string operators, each once, in a budget of exactly six.
089 budget-spent: five operators in a budget of five, then a sixth that would
    fault bad index: it faults budget spent instead (D21, D22).

The definitions this computes from, and nothing else:

- A string is a sequence of code points (D31). Python's str is one, so the
  model uses it for length, index and order; it asserts that on the strings
  where UTF-16 or bytes would differ, so a test tells them apart.
- Printing (D32) is written here from the decision, with no repr or json:
  " and \\ get a backslash, 10 is \\n, 9 is \\t, any other code point below
  0x20 and 0x7F is \\u{x} in lowercase hex without leading zeros, everything
  else is itself, written as UTF-8. Integers print in decimal, booleans as
  #true and #false (D11).
- The six operators (D33), their fault order (D33: each operand's type left
  to right, then the range), == and != on any two values (D12: different
  types are not equal, no fault), and an arithmetic operator or an
  ordering given a non-integer (D11, D33): not an integer.
- Evaluation is left to right (D25); an operator is charged to every budget
  in force after its operands and before its checks (D21 to D23); literals,
  if and within cost nothing; a within's budget is evaluated first, and a
  negative one or a non-integer faults (D24).
- Integers: the model only builds ones in range (D4) and asserts it.
- The bits of source: a literal's escapes are \\" \\\\ \\n \\t and \\u{X}
  with X in hex of one to six digits (D31). A literal here writes a
  character raw only where the test says so, and as \\u{X} otherwise.

Every command that regenerates a file is listed, one a line, so that
t/checks.py can run them all and diff (`make checks`), and `make models`
can write them:

    python3 t/models/strings.py --program 070 > t/070-print-escapes.lang
    python3 t/models/strings.py 070 > t/070-print-escapes.expected
    python3 t/models/strings.py --program 071 > t/071-print-nonascii.lang
    python3 t/models/strings.py 071 > t/071-print-nonascii.expected
    python3 t/models/strings.py --program 072 > t/072-print-empty.lang
    python3 t/models/strings.py 072 > t/072-print-empty.expected
    python3 t/models/strings.py --program 073 > t/073-str-len.lang
    python3 t/models/strings.py 073 > t/073-str-len.expected
    python3 t/models/strings.py --program 074 > t/074-str-at-all.lang
    python3 t/models/strings.py 074 > t/074-str-at-all.expected
    python3 t/models/strings.py --program 075 > t/075-str-at-negative.lang
    python3 t/models/strings.py 075 > t/075-str-at-negative.expected
    python3 t/models/strings.py --program 076 > t/076-str-at-length.lang
    python3 t/models/strings.py 076 > t/076-str-at-length.expected
    python3 t/models/strings.py --program 077 > t/077-str-lt.lang
    python3 t/models/strings.py 077 > t/077-str-lt.expected
    python3 t/models/strings.py --program 078 > t/078-str-code-edges.lang
    python3 t/models/strings.py 078 > t/078-str-code-edges.expected
    python3 t/models/strings.py --program 079 > t/079-str-char-edges.lang
    python3 t/models/strings.py 079 > t/079-str-char-edges.expected
    python3 t/models/strings.py --program 080 > t/080-str-code-two.lang
    python3 t/models/strings.py 080 > t/080-str-code-two.expected
    python3 t/models/strings.py --program 081 > t/081-str-char-negative.lang
    python3 t/models/strings.py 081 > t/081-str-char-negative.expected
    python3 t/models/strings.py --program 082 > t/082-str-char-surrogate.lang
    python3 t/models/strings.py 082 > t/082-str-char-surrogate.expected
    python3 t/models/strings.py --program 083 > t/083-str-char-range.lang
    python3 t/models/strings.py 083 > t/083-str-char-range.expected
    python3 t/models/strings.py --program 084 > t/084-not-a-string.lang
    python3 t/models/strings.py 084 > t/084-not-a-string.expected
    python3 t/models/strings.py --program 085 > t/085-str-not-an-integer.lang
    python3 t/models/strings.py 085 > t/085-str-not-an-integer.expected
    python3 t/models/strings.py --program 086 > t/086-str-eq.lang
    python3 t/models/strings.py 086 > t/086-str-eq.expected
    python3 t/models/strings.py --program 087 > t/087-arith-string.lang
    python3 t/models/strings.py 087 > t/087-arith-string.expected
    python3 t/models/strings.py --program 088 > t/088-str-budget-edge.lang
    python3 t/models/strings.py 088 > t/088-str-budget-edge.expected
    python3 t/models/strings.py --program 089 > t/089-str-budget-spent.lang
    python3 t/models/strings.py 089 > t/089-str-budget-spent.expected
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1

class Fault(Exception):
    """A fault, the message as the decisions name it in args[0]."""

class L:
    """A string literal in the source. `raw` is the set of characters the
    source writes as themselves (past printable ASCII); every other
    character past printable ASCII is written \\u{X}, in capitals, padded
    to four digits if `pad`."""
    def __init__(self, s, raw=(), pad=False):
        self.s, self.raw, self.pad = s, frozenset(raw), pad

def raw_all(s):
    return frozenset(c for c in s if ord(c) > 0x7F)

# ---- source (D31) ----

def src_lit(l):
    out = ['"']
    for c in l.s:
        o = ord(c)
        if c == '"':
            out.append('\\"')
        elif c == '\\':
            out.append('\\\\')
        elif o == 10:
            out.append('\\n')
        elif o == 9:
            out.append('\\t')
        elif 0x20 <= o <= 0x7E or c in l.raw:
            out.append(c)
        else:
            out.append('\\u{%s}' % (('%04X' if l.pad else '%X') % o))
    out.append('"')
    return ''.join(out)

def src(e):
    if e is True:
        return '#true'
    if e is False:
        return '#false'
    if isinstance(e, int):
        return str(e)
    if isinstance(e, L):
        return src_lit(e)
    if isinstance(e, str):
        return e   # an operator's name
    return '(' + ' '.join(src(x) for x in e) + ')'

# ---- printing (D32), written from the decision ----

def show(v):
    if v is True:
        return '#true'
    if v is False:
        return '#false'
    if isinstance(v, int):
        return str(v)
    out = ['"']
    for c in v:
        o = ord(c)
        if c == '"':
            out.append('\\"')
        elif c == '\\':
            out.append('\\\\')
        elif o == 10:
            out.append('\\n')
        elif o == 9:
            out.append('\\t')
        elif o < 0x20 or o == 0x7F:
            out.append('\\u{%x}' % o)
        else:
            out.append(c)
    out.append('"')
    return ''.join(out)

# ---- evaluation (D25, D33, D21 to D23) ----

def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)

def is_str(v):
    return isinstance(v, str)

def code_point(s):
    return ord(s)

class Run:
    def __init__(self):
        self.budgets = []   # what each budget in force has left
        self.ops = 0

    def charge(self):
        self.ops += 1
        if any(b == 0 for b in self.budgets):
            raise Fault('budget spent')
        self.budgets = [b - 1 for b in self.budgets]

    def ev(self, e):
        if e is True or e is False or is_int(e):
            if is_int(e):
                assert MIN <= e <= MAX
            return e
        if isinstance(e, L):
            return e.s
        op, args = e[0], e[1:]
        if op == 'if':
            t = self.ev(args[0])
            if t is not True and t is not False:
                raise Fault('not a boolean')
            return self.ev(args[1] if t else args[2])
        if op == 'within':
            n = self.ev(args[0])
            if not is_int(n):
                raise Fault('not an integer')
            if n < 0:
                raise Fault('bad budget')
            self.budgets.append(n)
            try:
                return self.ev(args[1])
            finally:
                self.budgets.pop()
        vals = [self.ev(a) for a in args]
        self.charge()
        if op in ('+', '-', '*', '<'):
            a, b = vals
            if not is_int(a) or not is_int(b):
                raise Fault('not an integer')
            r = {'+': lambda: a + b, '-': lambda: a - b, '*': lambda: a * b,
                 '<': lambda: a < b}[op]()
            if not isinstance(r, bool):
                assert MIN <= r <= MAX
            return r
        if op in ('==', '!='):
            a, b = vals
            same = type(a) is type(b) and a == b   # D12: other types, #false
            return same if op == '==' else not same
        # the six (D33): types left to right, then the range
        if op == 'str/len':
            if not is_str(vals[0]):
                raise Fault('not a string')
            return len(vals[0])
        if op == 'str/at':
            s, i = vals
            if not is_str(s):
                raise Fault('not a string')
            if not is_int(i):
                raise Fault('not an integer')
            if i < 0 or i >= len(s):
                raise Fault('bad index')
            return s[i]
        if op == 'str/cat':
            a, b = vals
            if not is_str(a) or not is_str(b):
                raise Fault('not a string')
            return a + b
        if op == 'str/lt':
            a, b = vals
            if not is_str(a) or not is_str(b):
                raise Fault('not a string')
            return a < b   # code point by code point; a prefix first
        if op == 'str/code':
            if not is_str(vals[0]):
                raise Fault('not a string')
            if len(vals[0]) != 1:
                raise Fault('not a character')
            return ord(vals[0])
        if op == 'str/char':
            n = vals[0]
            if not is_int(n):
                raise Fault('not an integer')
            if n < 0 or 0xD800 <= n <= 0xDFFF or n > 0x10FFFF:
                raise Fault('not a character')
            return chr(n)
        raise AssertionError(op)

def outcome(e):
    """(value, None) or (None, fault message)."""
    try:
        return Run().ev(e), None
    except Fault as f:
        return None, f.args[0]

# ---- building programs ----

def horner(parts):
    """A decimal number whose digits are the parts (each 0 to 9), after a
    leading 1 so a leading 0 is kept."""
    acc = 1
    for p in parts:
        acc = ('+', ('*', 10, acc), p)
    return acc

def cat(*xs):
    acc = xs[0]
    for x in xs[1:]:
        acc = ('str/cat', acc, x)
    return acc

def bit(test):
    return ('if', test, 1, 0)

ZWJ = '\U0001F468‍\U0001F469‍\U0001F467'   # man ZWJ woman ZWJ girl
CTRL = ''.join(chr(i) for i in range(0x20))
EDGES = [0, 0x7F, 0xD7FF, 0xE000, 0xFFFF, 0x10000, 0x10FFFF]

def t070():
    # every control character from a literal (padded in some), then two from
    # str/char, then the quote, backslash, newline and tab between ASCII
    lit = L('a"b\\c\nd\te' + CTRL + ' ~\x7f', pad=True)
    return cat(lit, ('str/char', 7), ('str/char', 127), ('str/char', 0), L('é', raw={'é'}))

def t071():
    a = 'é' + 'é' + '\U0001F600' + ZWJ + '￿\U00010000\U0010ffff'
    b = '\x80\x9f\xa0 ﻿퟿\U0010ffff\U0001F600'
    return cat(L(a, raw=raw_all(a)), L(b), L('|é', raw={'é'}))

def t072():
    return ('if', ('==', L(''), cat(L(''), L(''))), L(''), L('x'))

LEN_STRINGS = ['', 'abc', '\U0001F600', 'é', 'é', '￿\U00010000',
               '', ZWJ, 'a\U0001F600b', '\x00',
               '\U0010ffff\U0010ffff', '\U0001F600' * 3, '퟿']

def lit_alt(s, i):
    """A literal, raw for the even ones and escaped for the odd."""
    return L(s, raw=raw_all(s) if i % 2 == 0 else (), pad=(i % 3 == 0))

def t073():
    return horner([('str/len', lit_alt(s, i)) for i, s in enumerate(LEN_STRINGS)])

AT_STRING = 'a\U0001F600é￿\U00010000b'

def t074():
    parts = [L('')]
    for i in range(len(AT_STRING)):
        parts += [L('|'), ('str/at', lit_alt(AT_STRING, i), i)]
    return cat(*parts)

def t075():
    return cat(L('x'), ('str/at', L('a\U0001F600', raw={'\U0001F600'}), -1))

def t076():
    return cat(L('x'), ('str/at', L('a\U0001F600', raw={'\U0001F600'}), 2))

# (a, b, whether a sorts before b), the third written by hand; asserted
# against the model below. The comments say what a UTF-16 or byte reading
# would answer differently.
LT_PAIRS = [
    ('￿', '\U00010000', True),     # UTF-16: D800 < FFFF, so False
    ('\U00010000', '￿', False),    # UTF-16: True
    ('\U00010000', '', False),    # UTF-16: D800 < E000, True
    ('', '\U00010000', True),
    ('\U0001F600', '～', False),    # UTF-16: D83D < FF5E, True
    ('～', '\U0001F600', True),
    ('a', 'ab', True),                  # a prefix sorts first
    ('ab', 'a', False),
    ('', 'a', True),
    ('a', '', False),
    ('a', 'a', False),                  # equal
    ('', '', False),
    ('e', 'é', True),
    ('é', 'é', False),       # E9 > 65, though both read "e-acute"
    ('é', 'é', True),
    ('B', 'a', True),                   # 42 < 61
    ('\U0010ffff', '\U0010fffe', False),
]

def t077():
    for a, b, want in LT_PAIRS:
        assert (a < b) == want, (a, b)
    u16 = lambda x: x.encode('utf-16-be')
    for i in (0, 1, 2, 3, 4, 5):   # the pairs UTF-16 would answer the other way
        a, b, want = LT_PAIRS[i]
        assert (u16(a) < u16(b)) != want, (a, b)
    return horner([bit(('str/lt', lit_alt(a, i), lit_alt(b, i + 1)))
                   for i, (a, b, _) in enumerate(LT_PAIRS)])

def t078():
    srcs = ['\x00', '\x7f', '퟿', '', '￿', '\U00010000', '\U0010ffff', '\U0001F600']
    terms = [('*', i + 1, ('str/code', lit_alt(s, i))) for i, s in enumerate(srcs)]
    acc = terms[0]
    for t in terms[1:]:
        acc = ('+', acc, t)
    return acc

def t079():
    nums = EDGES + [0x41, 0x1F600, 0x20, 0x22, 0x5C]
    parts = [L('')]
    for n in nums:
        parts += [L('|'), ('str/char', n)]
    return cat(*parts)

def t080():
    return cat(L('x'), ('str/char', ('str/code', L('é'))))

def t081():
    return cat(L('x'), ('str/char', -1))

def t082():
    return cat(L('x'), ('str/char', 0xD800))

def t083():
    return cat(L('x'), ('str/char', 0x110000))

def t084():
    return ('str/at', 5, True)

def t085():
    return ('str/at', L('ab'), L('x'))

EQ_PAIRS = [
    ('==', 'é', 'é'),             # nothing is normalised: #false
    ('==', 'é', 'é'),
    ('==', 'a', 'a'),
    ('==', '', ''),
    ('==', '\U0001F600', '\U0001F600'),
    ('!=', 'é', 'é'),
    ('!=', '\U00010000', '￿'),
    ('==', 'ab', 'ba'),
    ('==', 'A', 'a'),
    ('==', 'a', 1),                     # other types: #false, no fault (D12)
    ('==', 1, 'a'),
    ('!=', 'a', 1),
    ('==', '1', 1),
    ('!=', '', 0),
    ('==', 'true', True),
    ('==', '', False),
]

def t086():
    def lit(x, i):
        return lit_alt(x, i) if isinstance(x, str) else x
    return horner([bit((op, lit(a, i), lit(b, i + 1))) for i, (op, a, b) in enumerate(EQ_PAIRS)])

def t087():
    return ('+', ('*', 2, 3), ('-', 1, L('1')))

def six_ops_ok():
    # len, at, code, char, cat, lt: one each, six in all
    return ('if',
            ('str/lt',
             ('str/char', ('str/code', ('str/at', L('a\U0001F600', raw={'\U0001F600'}), ('str/len', L('a'))))),
             ('str/cat', L('\U0001F601', raw={'\U0001F601'}), L(''))),
            L('\U0001F600 before \U0001F601', raw=raw_all('\U0001F600\U0001F601')),
            L('no'))

def t088():
    return ('within', 6, six_ops_ok())

def t089():
    # len, at, code, char, cat: five; the sixth, at index 9, would fault bad index
    five = ('str/cat', ('str/char', ('str/code', ('str/at', L('a\U0001F600', raw={'\U0001F600'}), ('str/len', L('a'))))), L(''))
    return ('within', 5, ('str/at', five, 9))

TESTS = {
    '070': ('print-escapes', 'D32: every escape and control character printed', t070),
    '071': ('print-nonascii', 'D31, D32: characters past ASCII print as themselves', t071),
    '072': ('print-empty', 'D32: the empty string prints as ""', t072),
    '073': ('str-len', 'D31, D33: str/len counts code points', t073),
    '074': ('str-at-all', 'D31, D33: str/at at every index', t074),
    '075': ('str-at-negative', 'D33: str/at faults bad index below 0', t075),
    '076': ('str-at-length', 'D33: str/at faults bad index at the length', t076),
    '077': ('str-lt', 'D33: str/lt compares code points, not UTF-16 units', t077),
    '078': ('str-code-edges', 'D33: str/code at the edges', t078),
    '079': ('str-char-edges', 'D33: str/char at the edges', t079),
    '080': ('str-code-two', 'D33: str/code of two characters is not a character', t080),
    '081': ('str-char-negative', 'D33: str/char of a negative is not a character', t081),
    '082': ('str-char-surrogate', 'D33: str/char of a surrogate is not a character', t082),
    '083': ('str-char-range', 'D33: str/char past 10FFFF is not a character', t083),
    '084': ('not-a-string', 'D33: operands are checked left to right, each for its type', t084),
    '085': ('str-not-an-integer', 'D33: str/at\'s index must be an integer', t085),
    '086': ('str-eq', 'D12, D33: == and != on strings and across types', t086),
    '087': ('arith-string', 'D11, D33: arithmetic given a string is not an integer', t087),
    '088': ('str-budget-edge', 'D21, D22, D33: six string operators in a budget of six', t088),
    '089': ('str-budget-spent', 'D21, D22, D33: the sixth is charged before its check', t089),
}

def program(test):
    name, what, build = TESTS[test]
    e = build()
    return (f'; {what}. test {test}.\n'
            f'; Expected output and this program from t/models/strings.py.\n'
            f'{src(e)}\n')

def expected(test):
    v, f = outcome(TESTS[test][2]())
    if f is not None:
        return f'fault: {f}\nexit: 1\n'
    return show(v) + '\n'

def self_check():
    # What the model is for: the strings where a host's reading differs.
    assert len('\U0001F600') == 1 and len('\U0001F600'.encode('utf-16-le')) // 2 == 2
    assert len('\U0001F600'.encode()) == 4
    assert 'é' != 'é' and len('é') == 2
    assert len(ZWJ) == 5
    # t073's digits, worked by hand: lengths 0 3 1 2 1 2 1 5 3 1 2 3 2
    assert Run().ev(t073()) == 10312121531232
    # t086's digits by hand: == é/e+accent 0, é/é 1, a/a 1, ""/"" 1, 😀/😀 1,
    # != same 0, != U+10000/U+FFFF 1, ab/ba 0, A/a 0, a/1 0, 1/a 0, != a/1 1,
    # '1'/1 0, != ""/0 1, 'true'/#true 0, ""/#false 0
    assert Run().ev(t086()) == 10111101000010100
    # t078: 1*0 + 2*127 + 3*55295 + 4*57344 + 5*65535 + 6*65536 + 7*1114111 + 8*128512
    assert Run().ev(t078()) == (2*127 + 3*55295 + 4*57344 + 5*65535 + 6*65536
                                + 7*1114111 + 8*128512)
    # the budget tests: six operations in 088, five and a sixth in 089
    r = Run(); r.ev(six_ops_ok()); assert r.ops == 6

self_check()

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--program']
    if not args:
        sys.exit(__doc__)
    test = args[0]
    text = program(test) if '--program' in sys.argv else expected(test)
    sys.stdout.buffer.write(text.encode('utf-8'))

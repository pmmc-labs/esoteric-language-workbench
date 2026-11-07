#!/usr/bin/env python3
"""Model for step 4 (strings): tests 400 to 410.

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python doing the same job natively on `bytes`, never by
running the compiler. A Ditto string is a sequence of bytes, so every
operation is the bytes operation: bytes compare unsigned, byte by byte,
prefix first (`<`); `in` is substring search; `bytes.lower` and
`bytes.upper` change ASCII letters only; indexing and slicing are bytes
indexing and slicing, and `len` is the byte count. Ints follow D14; the
programs here never overflow, and the model stops if one would (faults
are the hand-written 41x to 45x tests). `int()` accepts an optional `-`
and decimal digits in range, which is not what Python's `int` accepts, so
the model checks the text itself (`valid_int`) before using it.

Tests 400 to 409 are fixed programs: every escape and UTF-8 text; interpolation of
every type, nested, with calls, evaluated left to right; `+` and the six
comparisons over edge strings (empty, prefixes, case, bytes above 0x7f);
indexing and `for` over a string; `in` and `not in`; `int` and `str` round
trips; `lower`, `upper` and `slice`; `read()` on a text and on bytes with
NULs (the stdin files are written by the model too); and string
algorithms (reverse, palindromes, a Caesar cipher found by searching an
alphabet, run-length encoding). Test 410 is a random program: a generator
writes `print` lines of string, int and bool expressions and the model
evaluates the same tree in Python as it builds it. Seeds are fixed, so
reruns are identical.

    python3 t/models/strings.py --program escapes > t/400-escapes.ditto
    python3 t/models/strings.py escapes > t/400-escapes.expected
    python3 t/models/strings.py --program interpolation > t/401-interpolation.ditto
    python3 t/models/strings.py interpolation > t/401-interpolation.expected
    python3 t/models/strings.py --program compare > t/402-compare.ditto
    python3 t/models/strings.py compare > t/402-compare.expected
    python3 t/models/strings.py --program indexing > t/403-indexing.ditto
    python3 t/models/strings.py indexing > t/403-indexing.expected
    python3 t/models/strings.py --program membership > t/404-membership.ditto
    python3 t/models/strings.py membership > t/404-membership.expected
    python3 t/models/strings.py --program int-trips > t/405-int-trips.ditto
    python3 t/models/strings.py int-trips > t/405-int-trips.expected
    python3 t/models/strings.py --program case-slice > t/406-case-slice.ditto
    python3 t/models/strings.py case-slice > t/406-case-slice.expected
    python3 t/models/strings.py --program read > t/407-read.ditto
    python3 t/models/strings.py --stdin read > t/407-read.stdin
    python3 t/models/strings.py read > t/407-read.expected
    python3 t/models/strings.py --program read-nul > t/408-read-nul.ditto
    python3 t/models/strings.py --stdin read-nul > t/408-read-nul.stdin
    python3 t/models/strings.py read-nul > t/408-read-nul.expected
    python3 t/models/strings.py --program text-algos > t/409-text-algos.ditto
    python3 t/models/strings.py text-algos > t/409-text-algos.expected
    python3 t/models/strings.py --program random > t/410-random.ditto
    python3 t/models/strings.py random > t/410-random.expected
"""
import random
import re
import sys

MAX = 2**63 - 1
MIN = -(2**63)


def checked(n):
    assert MIN <= n <= MAX, 'a model program must not overflow'
    return n


def lit(s, alt=False):
    """The Ditto string literal for the text `s` (a Python str)."""
    out = []
    n = 0
    for c in s:
        if c == '\n': out.append('\\n')
        elif c == '\t': out.append('\\t')
        elif c == '\r': out.append('\\r')
        elif c == '\\': out.append('\\\\')
        elif c == '"': out.append('\\"')
        elif c == '{': out.append('\\{')
        elif c == '}':
            # A bare } is an ordinary byte outside an interpolation; \} means the same.
            out.append('\\}' if (n % 2 == 0) != alt else '}')
            n += 1
        else: out.append(c)
    return '"' + ''.join(out) + '"'


def show(v):
    """The printed form (what `str` gives) of a value at the top level."""
    if isinstance(v, bytes): return v
    if v is True: return b'true'
    if v is False: return b'false'
    if v is None: return b'nil'
    return str(v).encode()


class Prog:
    def __init__(self):
        self.src = []
        self.out = b''
        self.stdin = b''

    def line(self, s):
        self.src.append(s)

    def say(self, *vals):
        """The expected output of a print of these values."""
        self.out += b' '.join(show(v) for v in vals) + b'\n'

    def pr(self, srcs, vals):
        self.line('print(' + ', '.join(srcs) + ')')
        self.say(*vals)

    def program(self):
        return '\n'.join(self.src) + '\n'


def interp(*parts):
    """A literal with interpolations: each part is text (a str) or (src, value)."""
    s = '"'
    v = b''
    for p in parts:
        if isinstance(p, str):
            s += lit(p)[1:-1]
            v += p.encode()
        else:
            s += '{' + p[0] + '}'
            v += show(p[1])
    return s + '"', v


def valid_int(text):
    """int()'s definition: an optional -, decimal digits, in range."""
    return re.fullmatch(rb'-?[0-9]+', text) is not None and MIN <= int(text) <= MAX


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


# ---------------------------------------------------------------- 400

def escapes():
    p = Prog()
    strings = [
        'plain', '', 'tab\there', 'line\nbreak', 'cr\rhere', 'back\\slash', 'say "hi"',
        'braces {a} and }b{', '\\n is not a newline', '"\\"', 'café 日本 €',
        '// not a comment', '}}{{', 'a\tb\nc\rd\\e"f{g}h',
    ]
    for i, s in enumerate(strings):
        b = s.encode()
        p.line(f'print({lit(s, alt=i % 2 == 1)})')
        p.say(b)
        p.line(f'print(len({lit(s, alt=i % 2 == 1)}))')
        p.say(len(b))
    # Each escape alone, and a string made of nothing but escapes.
    p.pr(['"\\n"', '"\\t"', '"\\\\"', '"\\""', '"\\{"', '"\\}"', '"}"'],
         [b'\n', b'\t', b'\\', b'"', b'{', b'}', b'}'])
    p.pr(['len("\\n\\t\\r\\\\\\"\\{\\}")'], [7])
    return p


# ---------------------------------------------------------------- 401

def interpolation():
    p = Prog()
    a, b, name = 7, -3, 'Ada'
    p.line(f'let a = {a}')
    p.line(f'let b = -{-b}')
    p.line(f'let name = {lit(name)}')
    p.line('let flag = true')
    p.line('let nothing = nil')
    p.line('fn double(n) {')
    p.line('  return n * 2')
    p.line('}')
    p.line('fn say(s) {')
    p.line('  print("say " + s)')
    p.line('  return s')
    p.line('}')

    def pl(*parts):
        s, v = interp(*parts)
        p.line(f'print({s})')
        p.say(v)

    pl('a = ', ('a', a), ', b = ', ('b', b))
    pl(('name', name), ' is ', ('flag', True), ' and ', ('nothing', None))
    pl(('a * 2 + b', a * 2 + b))
    pl(('a / b', trunc_div(a, b)), ' ', ('a % b', a - b * trunc_div(a, b)))
    pl(('a < b', a < b), ' ', ('a == 7', a == 7), ' ', ('a != 7', a != 7))
    pl(('double(a)', 2 * a), ' ', ('double(double(b))', 4 * b))
    pl(('name + "!"', name + '!'))
    pl(('len(name)', len(name)), ' letters')
    pl(('upper(name)', name.upper()), ' ', ('lower(name)', name.lower()))
    pl(('name[0]', name[0]), ('name[1]', name[1]))
    pl(('slice(name, 1, 3)', name[1:3]))
    # An interpolation can hold a string with its own interpolation.
    pl(('"x{a}y"', f'x{a}y'), '/', ('"{b}"', str(b)))
    pl(('"<{"[{name}]"}>"', '<[Ada]>'))
    pl(('str(a) + str(b)', str(a) + str(b)))
    pl(('"7" in str(a)', True))
    pl(('int("42") + 1', 43))
    pl(('"}"', '}'), ' ', ('"\\{"', '{'))
    pl('only text \\{braces\\} and }')
    p.line('print("{a}")')
    p.say(a)
    p.line('print("{a}{b}{a}")')
    p.say(f'{a}{b}{a}')
    p.line('print("{name}{name}")')
    p.say(name * 2)
    p.line('print("" == "{""}")')
    p.say(True)
    # Parts are evaluated left to right, then the string is built.
    p.line('print("<{say("a")}{say("b")}-{say("c")}>")')
    p.out += b'say a\nsay b\nsay c\n<ab-c>\n'
    p.line('print("{say("x")}" + "{say("y")}")')
    p.out += b'say x\nsay y\nxy\n'
    return p


# ---------------------------------------------------------------- 402

def compare():
    p = Prog()
    edge = ['', 'a', 'b', 'A', 'B', 'ab', 'abc', 'abd', 'b\n', ' ', 'a b', 'z', 'Z', '0', '10', '9',
            'é', 'e', 'éa', '日', '€', 'café', 'cafe', '"', '{']
    rng = random.Random(402)
    pairs = [(x, y) for x in edge[:8] for y in edge[:8]]
    pairs += [(rng.choice(edge), rng.choice(edge)) for _ in range(60)]
    for x, y in pairs:
        bx, by = x.encode(), y.encode()
        ops = [('<', bx < by), ('<=', bx <= by), ('>', bx > by), ('>=', bx >= by),
               ('==', bx == by), ('!=', bx != by)]
        p.pr([f'{lit(x)} {o} {lit(y)}' for o, _ in ops], [r for _, r in ops])
    # Joining strings, and what the result is.
    for x, y in [('', ''), ('a', ''), ('', 'b'), ('ab', 'cd'), ('café', '!'), ('\n', '\t'),
                 ('x' * 40, 'y' * 40)]:
        z = (x + y).encode()
        p.pr([f'{lit(x)} + {lit(y)}', f'len({lit(x)} + {lit(y)})', f'{lit(x)} + {lit(y)} == {lit(x + y)}'],
             [z, len(z), True])
    p.pr(['"a" + "b" + "c" + "d"'], [b'abcd'])
    p.pr(['"a" + "b" == "ab"', '"1" + "2" == "12"', '"ab" < "a" + "c"'], [True, True, True])
    # Strings are never equal to other types.
    p.pr(['"1" == 1', '"" == nil', '"true" == true', '"a" != nil', '1 != "1"'],
         [False, False, False, True, True])
    return p


# ---------------------------------------------------------------- 403

def indexing():
    p = Prog()
    s = 'hello, world'
    b = s.encode()
    p.line(f'let s = {lit(s)}')
    p.pr(['len(s)'], [len(b)])
    p.line('for i in 0..len(s) {')
    p.line('  print(i, s[i])')
    p.line('}')
    for i in range(len(b)):
        p.say(i, b[i:i + 1])
    # for over a string walks its bytes as one-byte strings.
    p.line('let rev = ""')
    p.line('let seen = 0')
    p.line('for c in s {')
    p.line('  rev = c + rev')
    p.line('  seen += 1')
    p.line('  if c == "o" { print("o at", seen) }')
    p.line('}')
    for k, c in enumerate(b):
        if c == ord('o'): p.say('o at', k + 1)
    p.pr(['rev', 'seen'], [b[::-1], len(b)])
    # The loop sees the string as it was when it started.
    p.line('let t = "abc"')
    p.line('for c in t {')
    p.line('  t = t + c')
    p.line('  print(c, len(t))')
    p.line('}')
    for k, c in enumerate(b'abc'):
        p.say(bytes([c]), 4 + k)
    p.pr(['t'], [b'abcabc'])
    # Indexes can be any int expression; the result is a string of one byte.
    p.pr(['s[0] + s[len(s) - 1]', 's[1 + 2]', 's[12 / 4]', 's[0] == "h"', 's[5] == ","', 's[0] < s[1]'],
         [b[0:1] + b[-1:], b[3:4], b[3:4], True, True, False])
    p.pr(['"abc"[1]', '("a" + "bc")[2]', 'len("xyz"[0])', 'str(12345)[2]'], [b'b', b'c', 1, b'3'])
    # UTF-8 is bytes: an accented letter is two of them.
    u = 'café'.encode()
    p.line('let u = "café"')
    p.pr(['len(u)', 'u[3] == slice(u, 3, 4)', 'u[3] != u[4]', 'u[3] + u[4] == "é"'],
         [len(u), True, u[3] != u[4], True])
    p.line('let n = 0')
    p.line('for c in u { n += 1 }')
    p.pr(['n'], [len(u)])
    p.line('for c in "" { print("never") }')
    p.line('for c in "x" { print("once", c) }')
    p.say(b'once', b'x')
    return p


# ---------------------------------------------------------------- 404

def membership():
    p = Prog()
    hays = ['', 'abc', 'abcabc', 'aaa', 'hello, world', 'café', 'a\nb', '{x}', '日本語']
    needles = ['', 'a', 'abc', 'abcd', 'bc', 'c', 'ca', 'aa', 'aaaa', 'world', 'World', ', ', '\n',
               'é', '\xe9', 'fé', '本', '{', 'x}', 'b\n', ' ']
    for h in hays:
        for n in needles:
            bh, bn = h.encode(), n.encode()
            r = bn in bh
            p.pr([f'{lit(n)} in {lit(h)}', f'{lit(n)} not in {lit(h)}'], [r, not r])
    # `in` is a comparison: it combines with and/not, and + binds tighter on either side.
    p.pr(['"b" in "abc" and "z" not in "abc"', 'not ("q" in "abc")', '"a" + "b" in "xaby"',
          '"x" in "y" + "x"'],
         [True, True, True, True])
    # for over a string walks bytes, so this counts the bytes of the loop's string found in hay.
    p.line('let hay = "needle in a haystack"')
    p.line('let found = 0')
    p.line('for w in "hay needle straw nope" {')
    p.line('  if w in hay { found += 1 }')
    p.line('}')
    found = sum(1 for w in 'hay needle straw nope' if w.encode() in b'needle in a haystack')
    p.pr(['found'], [found])
    return p


# ---------------------------------------------------------------- 405

def int_trips():
    p = Prog()
    p.pr(['int("42")', 'int("-42")', 'int("0")', 'int("-0")', 'int("007")', 'int("00")'],
         [42, -42, 0, 0, 7, 0])
    p.pr(['int("9223372036854775807")', 'int("-9223372036854775807")', 'int("-9223372036854775808")'],
         [MAX, -MAX, MIN])
    vals = [0, 1, -1, 7, -7, 10, 99, 100, 12345, -12345, 2**31, -2**31, 2**32 + 1, 10**15, -10**15,
            MAX, MAX - 1, MIN, MIN + 1]
    p.line('let n = 0')
    for v in vals:
        text = str(v).encode()
        assert valid_int(text)
        sv = f'-{-v}' if v < 0 else str(v)
        if v == MIN: sv = '-9223372036854775807 - 1'
        p.line(f'n = {sv}')
        p.pr(['str(n)', 'len(str(n))', 'int(str(n)) == n', 'str(int(str(n)))'], [v, len(text), True, v])
    rng = random.Random(405)
    for _ in range(25):
        v = rng.randint(-10**rng.randint(1, 18), 10**rng.randint(1, 18))
        zeros = rng.randint(0, 3)
        text = ('-' if v < 0 else '') + '0' * zeros + str(abs(v))
        assert valid_int(text.encode())
        p.pr([f'int("{text}")', f'int("{text}") + 1' if v < MAX else '0', f'"{{int("{text}")}}"'],
             [v, v + 1 if v < MAX else 0, str(v)])
    p.pr(['str(5) + str(true) + str(nil) + str("q")', 'str(-9) == "-9"', 'str("x") == "x"',
          'str(str(7)) == "7"', 'len(str(nil))', 'int(str(12) + str(34)) + 1'],
         [b'5truenilq', True, True, True, 3, 1235])
    p.pr(['int("1" + "2")', 'int(slice("abc123", 3, 6)) * 2', 'int("12") < int("9")', '"12" < "9"'],
         [12, 246, False, True])
    return p


# ---------------------------------------------------------------- 406

def case_slice():
    p = Prog()
    strs = ['Hello, World!', 'abcXYZ', '', 'MiXeD cAsE 123', 'café ÉCOLE', '日本', 'a\tb\nc',
            'ZZZ zzz AAA aaa', '@[`{']
    for s in strs:
        b = s.encode()
        p.pr([f'lower({lit(s)})', f'upper({lit(s)})', f'len(upper({lit(s)})) == len({lit(s)})'],
             [b.lower(), b.upper(), True])
    p.pr(['lower(upper("aBc")) == "abc"', 'upper(lower("aBc")) == "ABC"', 'lower("") == ""'],
         [True, True, True])
    s = 'The quick brown fox'
    b = s.encode()
    p.line(f'let s = {lit(s)}')
    for i, j in [(0, len(b)), (0, 0), (len(b), len(b)), (4, 9), (0, 3), (16, 19), (10, 11), (3, 3)]:
        p.pr([f'slice(s, {i}, {j})', f'len(slice(s, {i}, {j}))'], [b[i:j], j - i])
    p.pr(['slice(s, 0, len(s)) == s', 'slice(s, 4, 9) + slice(s, 9, 10) == slice(s, 4, 10)',
          'slice(slice(s, 4, 9), 1, 3)', 'upper(slice(s, 4, 9))', 'slice(upper(s), 4, 9)'],
         [True, True, b[4:9][1:3], b[4:9].upper(), b.upper()[4:9]])
    # Slicing at a character boundary of UTF-8 text.
    u = 'café!'.encode()
    p.line('let u = "café!"')
    p.pr(['slice(u, 0, 3)', 'slice(u, 3, 5)', 'slice(u, 5, 6)', 'len(u)'], [u[0:3], u[3:5], u[5:6], len(u)])
    p.line('let i = 0')
    p.line('while i < len(s) {')
    p.line('  print(i, slice(s, i, i + 1) == s[i], slice(s, i, len(s)))')
    p.line('  i += 5')
    p.line('}')
    for i in range(0, len(b), 5):
        p.say(i, True, b[i:])
    return p


# ---------------------------------------------------------------- 407 / 408

READ_TEXT = (b'the quick brown fox\n'
             b'jumps over the lazy dog\n'
             b'\n'
             b'Pack my box with five dozen liquor jugs   \n'
             b'caf\xc3\xa9 \xe6\x97\xa5\xe6\x9c\xac\n'
             b'last line has no newline')


def read_text():
    p = Prog()
    p.stdin = READ_TEXT
    t = READ_TEXT
    p.line('let text = read()')
    p.line('print(len(text))')
    p.say(len(t))
    p.line('print(len(read()), read() == "")')
    p.say(0, True)
    # Split into lines by hand and print each, numbered, with its length.
    p.line('let line = ""')
    p.line('let lines = 0')
    p.line('for c in text {')
    p.line('  if c == "\\n" {')
    p.line('    lines += 1')
    p.line('    print("{lines}: [{line}] {len(line)}")')
    p.line('    line = ""')
    p.line('  } else {')
    p.line('    line += c')
    p.line('  }')
    p.line('}')
    p.line('print("{lines + 1}: [{line}] {len(line)}")')
    parts = t.split(b'\n')
    for k, ln in enumerate(parts):
        p.out += f'{k + 1}: ['.encode() + ln + f'] {len(ln)}\n'.encode()
    # Count some bytes, and upper-case the whole text.
    p.line('let spaces = 0')
    p.line('let vowels = 0')
    p.line('for c in lower(text) {')
    p.line('  if c == " " { spaces += 1 }')
    p.line('  if c in "aeiou" { vowels += 1 }')
    p.line('}')
    p.pr(['spaces', 'vowels'], [t.count(b' '), sum(t.lower().count(bytes([v])) for v in b'aeiou')])
    p.pr(['slice(upper(text), 0, 19)', 'slice(text, 20, 43) == "jumps over the lazy dog"',
          '"liquor" in text', '"liquor jugs   \\n" in text', '"dog\\ncat" in text'],
         [t.upper()[0:19], True, True, True, False])
    return p


NUL_TEXT = b'ab\x00cd\x00\x00e\n'


def read_nul():
    p = Prog()
    p.stdin = NUL_TEXT
    t = NUL_TEXT
    p.line('let t = read()')
    p.line('let nul = slice(t, 2, 3)')
    p.pr(['len(t)', 'len(nul)', 't[2] == nul', 'nul == slice(t, 5, 6)', 'nul == slice(t, 6, 7)',
          'nul == ""', 'nul != "a"'], [len(t), 1, True, True, True, False, True])
    p.pr(['"[" + nul + "]"'], [b'[\x00]'])
    p.pr(['len("a" + nul + "b")', '"a" + nul + "b" == slice(t, 1, 4)', '"a" + nul < "a" + nul + "b"',
          '"ab" < "ab" + nul', '"ab" + nul < "ab" + nul + nul', '"ab" + nul > "ab"', '"a" + nul < "a1"'],
         [3, False, True, True, True, True, True])
    p.pr(['nul in t', 'nul + nul in t', 'nul + nul + nul in t', '"b" + nul + "c" in t', '"c" + nul + "e" in t',
          'nul in "abc"', '"abc" + nul + "d" not in "abc"'],
         [b'\x00' in t, b'\x00\x00' in t, b'\x00\x00\x00' in t, b'b\x00c' in t, b'c\x00e' in t, False, True])
    p.line('let zeros = 0')
    p.line('let others = 0')
    p.line('for c in t {')
    p.line('  if c == nul { zeros += 1 } else { others += 1 }')
    p.line('}')
    p.pr(['zeros', 'others'], [t.count(b'\x00'), len(t) - t.count(b'\x00')])
    p.pr(['len(upper(t)) == len(t)', 'upper(t) == "AB" + nul + "CD" + nul + nul + "E\\n"',
          'lower(upper(t)) == t', 'len(slice(t, 2, 6))', 'slice(t, 3, 5)'],
         [True, True, True, 4, b'cd'])
    p.pr(['str(t) == t', 'len(str(t))', 'len("{t}")', '"{t}" == t'], [True, len(t), len(t), True])
    p.pr(['len(t + t)', '(t + t)[9] == nul'], [2 * len(t), (t + t)[9:10] == b'\x00'])
    return p


# ---------------------------------------------------------------- 409

def text_algos():
    p = Prog()
    p.line('fn reverse(s) {')
    p.line('  let r = ""')
    p.line('  for c in s { r = c + r }')
    p.line('  return r')
    p.line('}')
    p.line('fn is_palindrome(s) {')
    p.line('  return s == reverse(s)')
    p.line('}')
    p.line('fn count(s, ch) {')
    p.line('  let n = 0')
    p.line('  for c in s { if c == ch { n += 1 } }')
    p.line('  return n')
    p.line('}')
    p.line('fn index_of(s, ch) {')
    p.line('  for i in 0..len(s) {')
    p.line('    if s[i] == ch { return i }')
    p.line('  }')
    p.line('  return -1')
    p.line('}')
    p.line('fn caesar(s, shift) {')
    p.line('  let alphabet = "abcdefghijklmnopqrstuvwxyz"')
    p.line('  let out = ""')
    p.line('  for c in s {')
    p.line('    let at = index_of(alphabet, c)')
    p.line('    if at < 0 {')
    p.line('      out += c')
    p.line('    } else {')
    p.line('      out += alphabet[(at + shift) % 26]')
    p.line('    }')
    p.line('  }')
    p.line('  return out')
    p.line('}')
    p.line('fn rle(s) {')
    p.line('  if s == "" { return "" }')
    p.line('  let out = ""')
    p.line('  let cur = s[0]')
    p.line('  let run = 1')
    p.line('  for i in 1..len(s) {')
    p.line('    if s[i] == cur {')
    p.line('      run += 1')
    p.line('    } else {')
    p.line('      out += "{run}{cur}"')
    p.line('      cur = s[i]')
    p.line('      run = 1')
    p.line('    }')
    p.line('  }')
    p.line('  return out + "{run}{cur}"')
    p.line('}')
    p.line('fn repeat(s, n) {')
    p.line('  let out = ""')
    p.line('  for i in 0..n { out += s }')
    p.line('  return out')
    p.line('}')

    def rev(s): return s[::-1]

    def caesar(s, k):
        al = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join(al[(al.index(c) + k) % 26] if c in al else c for c in s)

    def rle(s):
        if not s: return ''
        out, cur, run = '', s[0], 1
        for c in s[1:]:
            if c == cur: run += 1
            else: out += f'{run}{cur}'; cur, run = c, 1
        return out + f'{run}{cur}'

    for w in ['level', 'hello', '', 'a', 'abba', 'abcba', 'Abba', 'ab cd dc ba', 'racecar!']:
        p.pr([f'reverse({lit(w)})', f'is_palindrome({lit(w)})'], [rev(w).encode(), w == rev(w)])
    for w in ['mississippi', 'banana', 'a b a']:
        p.pr([f'count({lit(w)}, "s")', f'count({lit(w)}, "a")', f'index_of({lit(w)}, "a")',
              f'index_of({lit(w)}, "z")'],
             [w.count('s'), w.count('a'), w.find('a'), w.find('z')])
    for w, k in [('hello, world', 3), ('xyz abc', 3), ('attack at dawn', 13), ('round trip', 0)]:
        c = caesar(w, k)
        p.pr([f'caesar({lit(w)}, {k})', f'caesar(caesar({lit(w)}, {k}), {26 - k}) == {lit(w)}'], [c.encode(), True])
    for w in ['aaabccdddd', 'abc', '', 'zzzzzzzzzzzz', 'aabbaabb']:
        p.pr([f'rle({lit(w)})'], [rle(w).encode()])
    p.pr(['repeat("ab", 5)', 'len(repeat("xyz", 100))', 'repeat("-", 0) == ""', 'repeat("=", 20)'],
         [b'ababababab', 300, True, b'=' * 20])
    # Build a number triangle as text.
    p.line('let row = ""')
    p.line('for i in 1..=9 {')
    p.line('  row += str(i)')
    p.line('  print(row + " " + reverse(row))')
    p.line('}')
    row = ''
    for i in range(1, 10):
        row += str(i)
        p.say((row + ' ' + rev(row)).encode())
    return p


# ---------------------------------------------------------------- 410

ALPHABET = 'abAB 1é-_'


class Gen:
    """Builds expressions as (source, value) pairs; the value is computed by
    Python's bytes and ints in step with the source."""

    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.vars = {}   # name -> bytes
        self.n = 0

    def lit(self):
        k = self.rng.randint(0, 5)
        s = ''.join(self.rng.choice(ALPHABET) for _ in range(k))
        return lit(s), s.encode()

    def string(self, d):
        r = self.rng
        opts = ['lit', 'var', 'var'] if d <= 0 else \
            ['lit', 'var', 'cat', 'cat', 'upper', 'lower', 'slice', 'str', 'interp', 'index', 'sl']
        k = r.choice(opts)
        if k == 'lit': return self.lit()
        if k == 'var':
            name = r.choice(sorted(self.vars))
            return name, self.vars[name]
        if k == 'cat':
            (sa, va), (sb, vb) = self.string(d - 1), self.string(d - 1)
            if len(va) + len(vb) > 120: return sa, va
            return f'{sa} + {sb}', va + vb
        if k == 'upper':
            s, v = self.string(d - 1)
            return f'upper({s})', v.upper()
        if k == 'lower':
            s, v = self.string(d - 1)
            return f'lower({s})', v.lower()
        if k == 'slice' or k == 'sl':
            s, v = self.string(d - 1)
            i = r.randint(0, len(v))
            j = r.randint(i, len(v))
            if k == 'sl': return f'slice({s}, {i}, len({s}))', v[i:]
            return f'slice({s}, {i}, {j})', v[i:j]
        if k == 'str':
            s, v = self.integer(d - 1)
            return f'str({s})', str(v).encode()
        if k == 'index':
            s, v = self.string(d - 1)
            if not v: return s, v
            i = r.randrange(len(v))
            return f'({s})[{i}]', v[i:i + 1]
        # interp: a few parts
        parts, val = '', b''
        for _ in range(r.randint(1, 3)):
            t = r.choice(['text', 's', 'n', 'b'])
            if t == 'text':
                x = r.choice(['x', ' - ', 'a b', '\\{}'])
                parts += x
                val += (b'{}' if x == '\\{}' else x.encode())
            elif t == 's':
                s, v = self.string(d - 1)
                parts += '{' + s + '}'
                val += v
            elif t == 'n':
                s, v = self.integer(d - 1)
                parts += '{' + s + '}'
                val += str(v).encode()
            else:
                s, v = self.boolean(d - 1)
                parts += '{' + s + '}'
                val += show(v)
        if len(val) > 200: return self.lit()
        return '"' + parts + '"', val

    def integer(self, d):
        r = self.rng
        k = r.choice(['lit', 'len'] if d <= 0 else ['lit', 'len', 'len', 'add', 'mul', 'round'])
        if k == 'lit':
            v = r.randint(-50, 5000)
            return (f'-{-v}' if v < 0 else str(v)), v
        if k == 'len':
            s, v = self.string(d - 1)
            return f'len({s})', len(v)
        if k == 'add':
            (sa, va), (sb, vb) = self.integer(d - 1), self.integer(d - 1)
            return f'({sa} + {sb})', checked(va + vb)
        if k == 'mul':
            (sa, va), (sb, vb) = self.integer(d - 1), self.integer(d - 1)
            if abs(va) > 10**6 or abs(vb) > 10**6: return sa, va
            return f'({sa} * {sb})', checked(va * vb)
        s, v = self.integer(d - 1)
        text = str(v).encode()
        assert valid_int(text)
        return f'int(str({s}))', v

    def boolean(self, d):
        r = self.rng
        k = r.choice(['cmp', 'cmp', 'in', 'notin', 'ncmp', 'eq'])
        if k == 'cmp' or k == 'eq':
            (sa, va), (sb, vb) = self.string(d - 1), self.string(d - 1)
            if k == 'eq' and r.random() < 0.5:
                sb, vb = sa, va
            op = r.choice(['<', '<=', '>', '>=', '==', '!='])
            res = {'<': va < vb, '<=': va <= vb, '>': va > vb, '>=': va >= vb,
                   '==': va == vb, '!=': va != vb}[op]
            return f'{sa} {op} {sb}', res
        if k == 'in' or k == 'notin':
            (sa, va), (sb, vb) = self.string(d - 1), self.string(d - 1)
            if r.random() < 0.4 and vb:
                i = r.randrange(len(vb))
                j = r.randint(i, len(vb))
                sa, va = f'slice({sb}, {i}, {j})', vb[i:j]
            return (f'{sa} in {sb}', va in vb) if k == 'in' else (f'{sa} not in {sb}', va not in vb)
        (sa, va), (sb, vb) = self.integer(d - 1), self.integer(d - 1)
        op = r.choice(['<', '<=', '>', '>=', '==', '!='])
        res = {'<': va < vb, '<=': va <= vb, '>': va > vb, '>=': va >= vb, '==': va == vb, '!=': va != vb}[op]
        return f'{sa} {op} {sb}', res


def random_prog(seed):
    g = Gen(seed)
    p = Prog()
    for name in ['s', 't', 'u']:
        src, v = g.lit()
        p.line(f'let {name} = {src}')
        g.vars[name] = v
    for _ in range(70):
        k = g.rng.choice(['print', 'print', 'print', 'printb', 'printn', 'set', 'add', 'multi'])
        if k == 'print':
            s, v = g.string(3)
            p.pr([s], [v])
        elif k == 'printb':
            s, v = g.boolean(2)
            p.pr([s], [v])
        elif k == 'printn':
            s, v = g.integer(3)
            p.pr([s], [v])
        elif k == 'set':
            name = g.rng.choice(sorted(g.vars))
            s, v = g.string(3)
            p.line(f'{name} = {s}')
            g.vars[name] = v
        elif k == 'add':
            name = g.rng.choice(sorted(g.vars))
            s, v = g.string(2)
            if len(g.vars[name]) + len(v) > 120: continue
            p.line(f'{name} += {s}')
            g.vars[name] += v
        else:
            (a, va), (b, vb), (c, vc) = g.string(2), g.integer(2), g.boolean(2)
            p.pr([a, b, c], [va, vb, vc])
    return p


# ---------------------------------------------------------------- the table

TESTS = {
    'escapes': ('400-escapes', escapes),
    'interpolation': ('401-interpolation', interpolation),
    'compare': ('402-compare', compare),
    'indexing': ('403-indexing', indexing),
    'membership': ('404-membership', membership),
    'int-trips': ('405-int-trips', int_trips),
    'case-slice': ('406-case-slice', case_slice),
    'read': ('407-read', read_text),
    'read-nul': ('408-read-nul', read_nul),
    'text-algos': ('409-text-algos', text_algos),
    'random': ('410-random', lambda: random_prog(410)),
}


def main(argv):
    mode = 'expected'
    if argv and argv[0] in ('--program', '--stdin'):
        mode = argv[0][2:]
        argv = argv[1:]
    if len(argv) != 1 or argv[0] not in TESTS:
        sys.exit('usage: strings.py [--program|--stdin] ' + '|'.join(TESTS))
    p = TESTS[argv[0]][1]()
    if mode == 'program':
        sys.stdout.buffer.write(p.program().encode())
    elif mode == 'stdin':
        sys.stdout.buffer.write(p.stdin)
    else:
        sys.stdout.buffer.write(p.out)


if __name__ == '__main__':
    main(sys.argv[1:])

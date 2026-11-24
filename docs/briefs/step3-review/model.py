#!/usr/bin/env python3
"""An independent model of the step-3 definition (strings), written from the
brief's words only.  parse(text) -> Program or raises Refuse; run(Program) ->
(stdout bytes, fault or None).

Values: Python int = Int, float = Num, str = Str.
"""
import re, math, ctypes

libm = ctypes.CDLL('libm.so.6')
libm.pow.restype = ctypes.c_double
libm.pow.argtypes = [ctypes.c_double, ctypes.c_double]

I63 = 2 ** 63
P53 = 2 ** 53
UNARY = {'length', 'uc', 'lc', 'ord', 'chr'}
FUNCS = {'substr', 'index'}
PUNCT = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ')

# Readings of the definition's ambiguous points, switchable so both can be tried.
OPT = {
    'dotdot_refused': True,     # ".." after a value: one perl token, refused (T27)
    'del_refused': True,        # U+007F counts as a control character
    'c1_refused': False,        # U+0080..U+009F in a literal
    # amendments: known findings turned into faults, so that mass runs show what is left
    'amend_x': False,
    # mutations: the definition made wrong on purpose, to see the checkers notice
    'mut_no_t92': False,
    'mut_no_soft': False,
    'mut_no_window': False,
    'amend_paren': False,
    'amend_uni': False,
    'amend_esc': False,
    'amend_pos': False,
    'amend_chr': False,
    'amend_substr': False,
}


class Refuse(Exception):
    pass


class Fault(Exception):
    pass


class Big(Exception):
    """not part of the definition: a string the model won't build, in mass runs"""


BIG = 10 ** 6


# ---------------------------------------------------------------- parsing

class P:
    def __init__(self, text):
        self.t = text
        self.i = 0
        self.line = 1
        self.utf8_line = None
        self.n = len(text)

    def refuse(self, why):
        raise Refuse('%d: %s' % (self.line, why))

    def ch(self, k=0):
        j = self.i + k
        return self.t[j] if j < self.n else ''

    def check_char(self, c, where):
        """c is inside a string literal or a comment"""
        o = ord(c)
        if c == '\t' or c == '\n':
            return
        if o < 0x20:
            self.refuse('control character in ' + where)
        if o == 0x7F and OPT['del_refused']:
            self.refuse('DEL in ' + where)
        if o >= 0x80:
            if 0x80 <= o <= 0x9F and OPT['c1_refused']:
                self.refuse('C1 control in ' + where)
            if self.utf8_line is None or self.utf8_line >= self.line:
                self.refuse('character past ASCII without use utf8 on an earlier line')

    def skip(self):
        t = self.t
        while self.i < self.n:
            c = t[self.i]
            if c == ' ' or c == '\t':
                self.i += 1
            elif c == '\n':
                self.i += 1
                self.line += 1
            elif c == '#':
                # a line whose first non-blank characters are #! is refused
                j = self.i - 1
                while j >= 0 and t[j] in ' \t':
                    j -= 1
                if (j < 0 or t[j] == '\n') and self.ch(1) == '!':
                    self.refuse('#! line')
                while self.i < self.n and t[self.i] != '\n':
                    self.check_char(t[self.i], 'comment')
                    self.i += 1
            else:
                o = ord(c)
                if o < 0x20 or o >= 0x7F:
                    self.refuse('character %r outside a literal' % c)
                return

    def word(self):
        m = re.compile(r'[A-Za-z_][A-Za-z0-9_]*').match(self.t, self.i)
        if not m:
            return None
        return m.group(0)

    def expect(self, s):
        self.skip()
        if not self.t.startswith(s, self.i):
            self.refuse('expected %r' % s)
        self.i += len(s)

    # ---- literals

    def digits(self, i, ds):
        t = self.t
        j = i
        if j >= self.n or t[j] not in ds:
            return None
        while j < self.n and (t[j] in ds or t[j] == '_'):
            if t[j] == '_' and not (t[j - 1] in ds and j + 1 < self.n and t[j + 1] in ds):
                self.refuse('underscore not between two digits')
            j += 1
        return j

    def number(self):
        t = self.t
        i = self.i
        D = '0123456789'
        isint = True
        if t[i] == '0' and self.ch(1) in 'xXbBoO' and self.ch(1) != '':
            ds = {'x': '0123456789abcdefABCDEF', 'b': '01', 'o': '01234567'}[t[i + 1].lower()]
            j = self.digits(i + 2, ds)
            if j is None:
                self.refuse('bad radix literal')
            v = int(t[i + 2:j].replace('_', ''), {'x': 16, 'b': 2, 'o': 8}[t[i + 1].lower()])
            if v > 0xFFFFFFFF:
                self.refuse('radix literal past 32 bits')
        else:
            j = i
            if t[i] != '.':
                if t[i] == '0' and (self.ch(1) in D + '_') and self.ch(1) != '':
                    self.refuse('leading zero')
                j = self.digits(i, D)
            if j < self.n and t[j] == '.':
                k = self.digits(j + 1, D)
                if k is None:
                    self.refuse('number directly followed by .')
                j = k
                isint = False
            if j < self.n and t[j] in 'eE':
                k = j + 1
                if k < self.n and t[k] in '+-':
                    k += 1
                k2 = self.digits(k, D)
                if k2 is None:
                    self.refuse('number followed by a letter')
                j = k2
                isint = False
            text = t[i:j].replace('_', '')
            if j - i > 250:
                self.refuse('number too long')
            if isint:
                v = int(text)
                if v > I63 - 1:
                    self.refuse('integer literal too large')
            else:
                v = float(text)
                if math.isinf(v):
                    self.refuse('float literal too large')
        if j < self.n and (t[j].isalnum() or t[j] in '_.') and ord(t[j]) < 128:
            self.refuse('number runs into %r' % t[j])
        self.i = j
        return ('lit', v)

    def scalar(self, v):
        if v > 0x10FFFF or 0xD800 <= v <= 0xDFFF:
            self.refuse('not a Unicode scalar value')
        return chr(v)

    def string(self):
        t = self.t
        q = t[self.i]
        self.i += 1
        out = []
        HEX = '0123456789abcdefABCDEF'
        while True:
            if self.i >= self.n:
                self.refuse('unterminated string')
            c = t[self.i]
            if c == q:
                self.i += 1
                break
            if c == '\\':
                d = self.ch(1)
                if d == '':
                    self.refuse('unterminated string')
                if q == "'":
                    if d in "\\'":
                        out.append(d)
                        self.i += 2
                    else:
                        out.append('\\')
                        self.i += 1
                    continue
                simple = {'n': '\n', 't': '\t', 'r': '\r', 'f': '\f', 'b': '\b', 'a': '\a', 'e': '\x1b'}
                if d in simple:
                    out.append(simple[d])
                    self.i += 2
                elif d in '01234567':
                    j = self.i + 1
                    while j < self.n and j < self.i + 4 and t[j] in '01234567':
                        j += 1
                    if OPT['amend_esc'] and j - self.i - 1 < 3 and j < self.n and t[j] in '89':
                        self.refuse('AMENDED: a short octal escape before 8 or 9')
                    out.append(self.scalar(int(t[self.i + 1:j], 8)))
                    self.i = j
                elif d == 'x':
                    if self.ch(2) == '{':
                        j = t.find('}', self.i + 3)
                        body = t[self.i + 3:j] if j >= 0 else ''
                        if j < 0 or not body or any(h not in HEX for h in body):
                            self.refuse('bad \\x{}')
                        out.append(self.scalar(int(body, 16)))
                        self.i = j + 1
                    else:
                        j = self.i + 2
                        while j < self.n and j < self.i + 4 and t[j] in HEX:
                            j += 1
                        if j == self.i + 2:
                            self.refuse('\\x with no hex digit')
                        if OPT['amend_esc'] and j == self.i + 3 and t[j:j + 1] != q:
                            self.refuse('AMENDED: \\x with one hex digit, not at the end of the string')
                        out.append(chr(int(t[self.i + 2:j], 16)))
                        self.i = j
                elif d == 'o':
                    j = t.find('}', self.i + 3)
                    body = t[self.i + 3:j] if j >= 0 else ''
                    if self.ch(2) != '{' or j < 0 or not body or any(h not in '01234567' for h in body):
                        self.refuse('bad \\o{}')
                    out.append(self.scalar(int(body, 8)))
                    self.i = j + 1
                elif d == 'N':
                    j = t.find('}', self.i + 5)
                    body = t[self.i + 5:j] if j >= 0 else ''
                    if t[self.i + 2:self.i + 5] != '{U+' or j < 0 or not body or any(h not in HEX for h in body):
                        self.refuse('bad \\N{U+}')
                    out.append(self.scalar(int(body, 16)))
                    self.i = j + 1
                elif d in PUNCT:
                    out.append(d)
                    self.i += 2
                else:
                    self.refuse('escape \\%s' % d)
                continue
            if q == '"' and c in '$@':
                self.refuse('unescaped %s in a double-quoted string' % c)
            self.check_char(c, 'string')
            if c == '\n':
                self.line += 1
            out.append(c)
            self.i += 1
        return ('lit', ''.join(out))

    # ---- expressions

    def primary(self):
        self.skip()
        c = self.ch()
        if c == '(':
            self.i += 1
            e = self.expr()
            self.expect(')')
            return ('paren', e)
        if c == '"' or c == "'":
            return self.string()
        if c != '' and (c in '0123456789' or (c == '.' and self.ch(1) != '' and self.ch(1) in '0123456789')):
            return self.number()
        w = self.word()
        if w in UNARY:
            self.i += len(w)
            self.skip()
            if self.ch() == '(':
                self.i += 1
                e = self.expr()
                self.expect(')')
                return ('call', w, [e], True)
            if OPT['amend_uni'] and self.ch() in ('-', '+') and (self.t[self.i - 1] not in ' \t' or self.ch(1) in (' ', '\t', '\n')):
                self.refuse('AMENDED: a named unary operator before a sign that is not hard against its operand, or is hard against the word')
            return ('call', w, [self.expr()], False)
        if w in FUNCS:
            self.i += len(w)
            self.expect('(')
            args = [self.expr()]
            self.expect(',')
            args.append(self.expr())
            self.skip()
            if self.ch() == ',':
                self.i += 1
                args.append(self.expr())
            self.expect(')')
            return ('call', w, args, True)
        self.refuse('expected a value at %r' % self.t[self.i:self.i + 10])

    def power(self):
        p = self.primary()
        self.skip()
        if self.ch() == '*' and self.ch(1) == '*':
            if self.ch(2) == '=':
                self.refuse('**=')
            self.i += 2
            return ('bin', '**', p, self.unary())
        return p

    def unary(self):
        self.skip()
        c = self.ch()
        if c == '-' or c == '+':
            if self.ch(1) == c:
                self.refuse(c + c)
            if self.ch(1) == '=' or (c == '-' and self.ch(1) == '>'):
                self.refuse('operator')
            self.i += 1
            return ('neg' if c == '-' else 'pos', self.unary())
        return self.power()

    def binop(self, ops):
        """the operator at the cursor if it is one of ops, consumed"""
        self.skip()
        c = self.ch()
        if c == '':
            return None
        if c == 'x' and 'x' in ops:
            if self.word() != 'x':
                self.refuse('x run into a word')
            if self.ch(1) == '=':
                self.refuse('x=')
            self.i += 1
            return 'x'
        if c in ops and c != 'x':
            d = self.ch(1)
            if d == '=':
                self.refuse(c + '=')
            if c == '*' and d == '*':
                self.refuse('**')
            if c in '+-' and d == c:
                self.refuse(c + c)
            if c == '-' and d == '>':
                self.refuse('->')
            if c == '/' and d == '/':
                self.refuse('//')
            if c == '.' and d == '.' and OPT['dotdot_refused']:
                self.refuse('..')
            self.i += 1
            return c
        return None

    def level4(self):
        e = self.unary()
        while True:
            op = self.binop('*/%x')
            if op is None:
                return e
            e = ('bin', op, e, self.unary())

    def expr(self):
        e = self.level4()
        while True:
            op = self.binop('+-.')
            if op is None:
                return e
            e = ('bin', op, e, self.level4())

    # ---- statements

    def program(self):
        t = self.t
        self.skip()
        if self.word() != 'use':
            self.refuse('use v5.42 first')
        self.i += 3
        if self.ch() not in (' ', '\t', '\n'):
            self.refuse('use')
        self.skip()
        if not t.startswith('v5.42', self.i):
            self.refuse('v5.42')
        self.i += 5
        if self.ch() not in (';', ' ', '\t', '\n'):
            self.refuse('v5.42 followed by something')
        self.expect(';')
        stmts = []
        use_open = False
        while True:
            self.skip()
            if self.i >= self.n:
                break
            w = self.word()
            line0 = self.line
            if w == 'use':
                if stmts:
                    self.refuse('use after a statement')
                self.i += 3
                if self.ch() not in (' ', '\t', '\n'):
                    self.refuse('use')
                self.skip()
                w2 = self.word()
                if w2 == 'utf8':
                    if self.utf8_line is not None:
                        self.refuse('use utf8 twice')
                    self.i += 4
                    self.expect(';')
                    self.utf8_line = self.line
                elif w2 == 'open':
                    if use_open:
                        self.refuse('use open twice')
                    self.i += 4
                    if self.ch() not in (' ', '\t', '\n'):
                        self.refuse('use open')
                    self.skip()
                    for k, arg in enumerate((':std', ':encoding(UTF-8)')):
                        if k:
                            self.expect(',')
                            self.skip()
                        q = self.ch()
                        if q not in ('"', "'") or t[self.i + 1:self.i + 2 + len(arg)] != arg + q:
                            self.refuse('use open spelling')
                        self.i += len(arg) + 2
                    self.expect(';')
                    use_open = True
                else:
                    self.refuse('use %s' % w2)
                continue
            if w not in ('say', 'print'):
                self.refuse('statement %r' % t[self.i:self.i + 10])
            self.i += len(w)
            oneblank = self.ch() == ' ' and self.ch(1) == '('
            if oneblank and OPT['amend_paren']:
                # perl's own scan: brackets counted as text, to the end of the line
                j = self.i + 2
                level = 1
                while j < self.n and t[j] != '\n' and level:
                    level += (t[j] == '(') - (t[j] == ')')
                    j += 1
                while j < self.n and t[j] in ' \t':
                    j += 1
                if level or t[j:j + 1] != ';':
                    self.refuse('AMENDED: %s ( with brackets that do not balance as text on the line' % w)
            self.skip()
            if self.ch() == '(':
                self.i += 1
                e = self.expr()
                self.expect(')')
                l1 = self.line
                self.skip()
                if self.ch() != ';':
                    self.refuse('after the bracket of %s must come ;' % w)
                if oneblank and (l1 != line0 or self.line != line0):
                    self.refuse('%s ( ... must end on its line' % w)
                self.i += 1
            else:
                e = self.expr()
                self.skip()
                if self.ch() != ';':
                    self.refuse('expected ; at %r' % t[self.i:self.i + 10])
                self.i += 1
            stmts.append((w, e, line0))
        return {'stmts': stmts, 'open': use_open, 'utf8': self.utf8_line is not None}


def parse(src):
    """src: bytes or str"""
    if isinstance(src, bytes):
        try:
            src = src.decode('utf-8')
        except UnicodeDecodeError:
            raise Refuse('invalid UTF-8')
    return P(src).program()


# ---------------------------------------------------------------- values

NUMRE = re.compile(r'[ \t\n\r\f\x0b]*([+-]?)(?:([0-9]+)(\.[0-9]*)?|(\.[0-9]+))([eE][+-]?[0-9]+)?[ \t\n\r\f\x0b]*')


def whole(x):
    return x == math.floor(x)


class Opnd:
    """a number operand: v is int or float; kind is 'int' (a true Int), 'num',
    'A', 'Cint', 'Cnum', 'B', 'soft'"""
    __slots__ = ('v', 'kind')

    def __init__(self, v, kind):
        self.v = v
        self.kind = kind

    @property
    def isint(self):
        return self.kind in ('int', 'A', 'Cint')

    @property
    def integral(self):
        if self.isint:
            return True
        if self.kind == 'soft':
            return False
        return whole(self.v) and abs(self.v) < P53

    @property
    def trueint(self):
        return self.kind == 'int'


def str2num(s):
    m = NUMRE.fullmatch(s)
    if not m:
        raise Fault('not a numeric string')
    body = s.strip(' \t\n\r\f\x0b')
    if m.group(5) is None and m.group(3) is None and m.group(4) is None:
        v = int(body)
        if abs(v) > I63 - 1:
            raise Fault('numeric string outside the integers')
        return Opnd(v, 'A')
    v = float(body)
    if math.isinf(v):
        raise Fault('float overflow')
    if m.group(5) is not None:
        if whole(v):
            if abs(v) < P53:
                return Opnd(int(v), 'Cint')
            raise Fault('exponent string whole and 2^53 or more')
        return Opnd(v, 'Cnum')
    if whole(v) and abs(v) < P53:
        return Opnd(v, 'soft')
    return Opnd(v, 'B')


def num(v):
    if isinstance(v, str):
        return str2num(v)
    if isinstance(v, int):
        return Opnd(v, 'int')
    return Opnd(v, 'num')


def integer(v, what=''):
    """a value where an integer is wanted: cut toward zero"""
    o = num(v)
    n = o.v if isinstance(o.v, int) else int(o.v)
    if OPT['amend_pos'] and o.kind in ('B', 'soft'):
        mm = NUMRE.fullmatch(v)
        if int(mm.group(1) + (mm.group(2) or '0')) != n:
            raise Fault('AMENDED: a string with a point whose digits before the point are not its double, cut')
    if OPT['amend_pos'] and what in ('pos', 'chr') and not fits(n):
        raise Fault('AMENDED: a position, length or chr argument outside the Ints')
    if OPT['amend_chr'] and what == 'chr' and o.v < 0:
        raise Fault('AMENDED: chr of a negative number, before cutting')
    return n


def tostr(v):
    if isinstance(v, str):
        return v
    if isinstance(v, int):
        return str(v)
    if v == 0:
        return '0'
    if whole(v) and 10 ** 15 <= abs(v) < P53 and not OPT['mut_no_window']:
        raise Fault('a whole float this size prints two ways')
    return '%.15g' % v


def fin(x):
    if math.isnan(x):
        raise Fault('not a number')
    if math.isinf(x):
        raise Fault('float overflow')
    return x


def exact53(x):
    """a whole number of magnitude 2^53 or more that a double holds exactly"""
    x = int(x)
    return abs(x) >= P53 and int(float(x)) == x


def fits(i):
    return -I63 <= i <= I63 - 1


def cpow(a, b):
    try:
        r = libm.pow(float(a), float(b))
    except OverflowError:
        raise Fault('float overflow')
    return fin(r)


def tofloat(o):
    return float(o.v)


def arith(op, a, b):
    a = num(a)
    b = num(b)
    if OPT['mut_no_soft']:
        for o in (a, b):
            if o.kind == 'soft':
                o.kind = 'num'
    softcase = (a.kind == 'soft' or b.kind == 'soft')
    if op == '%':
        x = a.v if isinstance(a.v, int) else int(a.v)
        y = b.v if isinstance(b.v, int) else int(b.v)
        if not fits(x) or not fits(y):
            raise Fault('modulus of a number outside the integers')
        if y == 0:
            raise Fault('modulus by zero')
        return x % y
    if op == '/' and b.v == 0:
        raise Fault('division by zero')
    if softcase:
        other = b if a.kind == 'soft' else a
        if a.kind == 'soft' and b.kind == 'soft':
            other = b
        if other.kind == 'soft' or other.integral:
            x, y = int(a.v), int(b.v)
            if abs(x) >= P53 or abs(y) >= P53:
                raise Fault('soft: operand 2^53 or more')
            ans = None
            if op == '+':
                ans = x + y
            elif op == '-':
                ans = x - y
            elif op == '*':
                ans = x * y
            elif op == '**' and y >= 0:
                if abs(x) >= 2 and y > 64:
                    raise Fault('soft: answer 2^53 or more')
                ans = x ** y
            if ans is not None and abs(ans) >= P53:
                raise Fault('soft: answer 2^53 or more')
        fa, fb = tofloat(a), tofloat(b)
        if op == '+':
            return fin(fa + fb)
        if op == '-':
            return fin(fa - fb)
        if op == '*':
            return fin(fa * fb)
        if op == '/':
            return fin(fa / fb)
        return cpow(fa, fb)
    both = a.integral and b.integral
    if op in '+-*' and both:
        if not OPT['mut_no_t92'] and ((exact53(a.v) and not b.trueint) or (exact53(b.v) and not a.trueint)):
            raise Fault('T92')
        x, y = int(a.v), int(b.v)
        if op == '+' or op == '-':
            r = x + y if op == '+' else x - y
            if not fits(r):
                raise Fault('integer overflow')
            return r
        p = x * y
        if fits(p):
            return p
        if (a.isint and b.isint) or I63 <= p <= 2 ** 64 - 1:
            raise Fault('integer overflow')
        return fin(tofloat(a) * tofloat(b))
    if op == '+':
        return fin(tofloat(a) + tofloat(b))
    if op == '-':
        return fin(tofloat(a) - tofloat(b))
    if op == '*':
        return fin(tofloat(a) * tofloat(b))
    if op == '/':
        if a.isint and abs(a.v) > P53 and b.integral and a.v % int(b.v) == 0:
            return a.v // int(b.v)
        return fin(tofloat(a) / tofloat(b))
    if op == '**':
        if both and b.v >= 0:
            x, y = int(a.v), int(b.v)
            ax = abs(x)
            if ax <= 1 or ax & (ax - 1) == 0:
                # a Num, exact
                if ax == 0:
                    return 1.0 if y == 0 else 0.0
                k = ax.bit_length() - 1
                if k * y > 1023:
                    raise Fault('float overflow')
                r = math.ldexp(1.0, k * y)
                return -r if (x < 0 and y % 2) else r
            if y * ax.bit_length() <= 64:
                r = x ** y
                if not fits(r):
                    raise Fault('integer overflow')
                return r
        return cpow(tofloat(a), tofloat(b))
    raise AssertionError(op)


def neg(v):
    if isinstance(v, int):
        if v == -I63:
            raise Fault('integer overflow')
        return -v
    if isinstance(v, float):
        return -v
    o = str2num(v)
    if v[:1] == '+':
        raise Fault('unary minus on a string that starts with +')
    f = float(o.v)
    if whole(f) and abs(f) >= P53:
        raise Fault('unary minus on a string 2^53 or more')
    return -f


def nonchar(c):
    o = ord(c)
    return 0xFDD0 <= o <= 0xFDEF or (o & 0xFFFE) == 0xFFFE


def ev(e):
    k = e[0]
    if k == 'lit':
        return e[1]
    if k == 'paren':
        return ev(e[1])
    if k == 'pos':
        return ev(e[1])
    if k == 'neg':
        return neg(ev(e[1]))
    if k == 'bin':
        op = e[1]
        a = ev(e[2])
        b = ev(e[3])
        if op == '.':
            return tostr(a) + tostr(b)
        if op == 'x':
            s = tostr(a)
            n = integer(b)
            if n < 0:
                raise Fault('negative repeat count')
            if OPT['amend_x'] and (float(num(b).v) < 0 or n > I63 - 1):
                raise Fault('AMENDED: repeat count negative before cutting, or past the Ints')
            if OPT['amend_x'] and n * max(len(s), 1) > BIG:
                raise Big()
            if n * len(s) > 2 ** 31 - 1:
                raise Fault('string too long')
            if n * len(s) > BIG:
                raise Big()
            return s * n if s else ''
        return arith(op, a, b)
    if k == 'call':
        f = e[1]
        args = [ev(x) for x in e[2]]
        if f == 'length':
            return len(tostr(args[0]))
        if f == 'uc' or f == 'lc':
            s = tostr(args[0])
            if any(ord(c) > 0x7F for c in s):
                raise Fault(f + ' of a character past ASCII')
            return s.upper() if f == 'uc' else s.lower()
        if f == 'ord':
            s = tostr(args[0])
            return ord(s[0]) if s else 0
        if f == 'chr':
            n = integer(args[0], 'chr')
            if n < 0 or n > 0x10FFFF or 0xD800 <= n <= 0xDFFF:
                raise Fault('chr of a number that is not a character')
            return chr(n)
        if f == 'substr':
            s = tostr(args[0])
            L = len(s)
            off = integer(args[1], 'pos')
            ln = integer(args[2], 'pos') if len(args) > 2 else None
            p1 = off + L if off < 0 else off
            if ln is None:
                p2 = L
            elif ln >= 0:
                p2 = p1 + ln
            else:
                p2 = L + ln
            if p1 > L:
                raise Fault('substr outside of string')
            if OPT['amend_substr'] and p1 < 0 and p2 < 0:
                raise Fault('AMENDED: substr wholly before the string')
            if p1 < 0:
                p1 = 0
            if p2 > L:
                p2 = L
            if p2 < p1:
                p2 = p1
            return s[p1:p2]
        if f == 'index':
            s = tostr(args[0])
            t = tostr(args[1])
            pos = integer(args[2], 'pos') if len(args) > 2 else 0
            pos = max(0, min(len(s), pos))
            return s.find(t, pos)
    raise AssertionError(e)


def kind(v):
    return 'Int' if isinstance(v, int) else 'Num' if isinstance(v, float) else 'Str'


def run(prog, trace=None):
    """-> (stdout bytes, None) or (stdout bytes so far, (statement index, message)).
    trace, if a list, gets the kind of each statement's value or the fault."""
    out = []
    for idx, (w, e, line) in enumerate(prog['stmts']):
        try:
            v = ev(e)
            s = tostr(v)
            if not prog['open'] and any(ord(c) > 0x7F for c in s):
                raise Fault('print of a character past ASCII without use open')
            if any(nonchar(c) for c in s):
                raise Fault('print of a noncharacter')
        except Fault as f:
            if trace is not None:
                trace.append('fault: ' + str(f))
            return b''.join(out), (idx, str(f))
        except RecursionError:
            raise Refuse('too deep')
        if trace is not None:
            trace.append(kind(v))
        out.append(s.encode('utf-8'))
        if w == 'say':
            out.append(b'\n')
    return b''.join(out), None

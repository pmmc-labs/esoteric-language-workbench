#!/usr/bin/env python3
"""An independent model of the step-4 definition (booleans, undef, comparison,
logic), written from the brief's words only, on top of the step-3 reviewer's
model (model.py, every amend_* switch on).

parse(text) -> Program or raises Refuse; run(Program) -> (stdout bytes, fault or None).

Values: Python int = Int, float = Num, str = Str, TRUE/FALSE = Bool, UNDEF = undef.
"""
import re, math
import model as M
from model import Refuse, Fault, Big, I63, P53, Opnd, whole, fits

BIG = 20000   # the longest string a mass run asks perl for

for k in list(M.OPT):
    if k.startswith('amend_'):
        M.OPT[k] = True

# readings and amendments for this step
OPT4 = {
    # how an argument inside a builtin's brackets is read: 'full' = any
    # expression (levels 1 to 14), '11' = a level-11 expression
    'args': 'full',
    # amendments, so that mass runs show what is left
    'amend_not_cmp': False,     # refuse an unbracketed ! as the left operand of a comparison
    'amend_cmp_pv': False,      # fault: comparison where a string with a point/exponent meets an Int >= 2^53
    # mutations
    'mut_and_bool': False,      # && returns a Bool
    'mut_cmp_float': False,     # comparisons always as doubles
    'mut_not_level': False,     # not takes a level-10 operand
}


class Bool:
    __slots__ = ('t',)

    def __init__(self, t):
        self.t = t

    def __repr__(self):
        return 'true' if self.t else 'false'


TRUE = Bool(True)
FALSE = Bool(False)


class Undef:
    def __repr__(self):
        return 'undef'


UNDEF = Undef()

UNARY = {'length', 'uc', 'lc', 'ord', 'chr', 'defined'}
FUNCS = {'substr', 'index'}
REL = {'<', '>', '<=', '>=', 'lt', 'gt', 'le', 'ge'}
EQ = {'==', '!=', '<=>', 'eq', 'ne', 'cmp'}
WORDOPS = {'lt', 'gt', 'le', 'ge', 'eq', 'ne', 'cmp', 'and', 'or', 'xor', 'not', 'x'}
# perl's operator tokens, for the longest one at a place
PUNCTOPS = sorted(['<=>', '**=', '||=', '&&=', '//=', '...', '<<=', '>>=', '<<', '>>', '**', '==', '!=', '<=', '>=',
                   '&&', '||', '//', '..', '::', '->', '++', '--', '+=', '-=', '*=', '/=', '.=', '%=', '&=', '|=', '^=',
                   '=~', '!~', '=>', '^^', '^^=', '&.', '|.', '^.', '&.=', '|.=', '^.=',
                   '+', '-', '*', '/', '%', '.', '<', '>', '=', '!', '~', '&', '|', '^', '?', ':', ',', ';', '(', ')',
                   '\\', '[', ']', '{', '}', '@', '$'], key=lambda s: -len(s))
BINLEVEL = {}
for _o in ('*', '/', '%', 'x'):
    BINLEVEL[_o] = 4
for _o in ('+', '-', '.'):
    BINLEVEL[_o] = 5
for _o in REL:
    BINLEVEL[_o] = 7
for _o in EQ:
    BINLEVEL[_o] = 8
BINLEVEL['&&'] = 9
BINLEVEL['||'] = 10
BINLEVEL['//'] = 10
BINLEVEL['and'] = 13
BINLEVEL['or'] = 14
BINLEVEL['xor'] = 14


class P4(M.P):
    def tok(self):
        """the operator token at the cursor after blanks: a word, or perl's
        longest punctuation token; '' at the end.  Not consumed."""
        self.skip()
        if self.i >= self.n:
            return ''
        w = self.word()
        if w:
            return w
        for o in PUNCTOPS:
            if self.t.startswith(o, self.i):
                return o
        return self.t[self.i]

    def take(self, tok):
        self.i += len(tok)

    # ---- terms

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
        if w in ('true', 'false'):
            self.i += len(w)
            if self.tok() == '(':
                self.refuse(w + ' followed by a bracket')
            return ('lit', TRUE if w == 'true' else FALSE)
        if w == 'undef':
            self.i += 5
            t = self.tok()
            if t not in (')', ',', ';', '?', ':', '//', '||', '&&', 'and', 'or', 'xor'):
                self.refuse('undef followed by %r' % t)
            return ('lit', UNDEF)
        if w in UNARY:
            self.i += len(w)
            self.skip()
            if self.ch() == '(':
                self.i += 1
                self.skip()
                if self.ch() == ')':
                    self.refuse(w + '()')
                e = self.expr()
                self.expect(')')
                return ('call', w, [e], True)
            if self.ch() in ('-', '+') and (self.t[self.i - 1] not in ' \t' or self.ch(1) in (' ', '\t', '\n')):
                self.refuse('a named unary operator before a sign that is not hard against its operand, or is hard against the word')
            return ('call', w, [self.level5()], False)
        if w in FUNCS:
            self.i += len(w)
            self.expect('(')
            args = [self.arg()]
            self.expect(',')
            args.append(self.arg())
            self.skip()
            if self.ch() == ',':
                self.i += 1
                args.append(self.arg())
            self.expect(')')
            return ('call', w, args, True)
        if w == 'not':
            self.i += 3
            self.skip()
            if self.ch() == '(':
                self.i += 1
                self.skip()
                if self.ch() == ')':
                    self.refuse('not()')
                e = self.expr()
                self.expect(')')
                t = self.tok()
                if t in ('**', '?') or (t in BINLEVEL and BINLEVEL[t] <= 10):
                    self.refuse('not (...) followed by the operator %s' % t)
                return ('not', ('paren', e), 'fun')
            if OPT4['mut_not_level']:
                return ('not', self.binary(10), 'op')
            e = self.ternary()
            if OPT4['args'] != 'full' and self.tok() == ',':
                self.refuse('AMENDED: an unbracketed not before a comma')
            return ('not', e, 'op')
        self.refuse('expected a value at %r' % self.t[self.i:self.i + 10])

    def arg(self):
        if OPT4['args'] == 'full':
            return self.expr()
        return self.ternary()

    def power(self):
        p = self.primary()
        if self.tok() == '**':
            self.take('**')
            return ('bin', '**', p, self.unary())
        return p

    def unary(self):
        self.skip()
        c = self.ch()
        if c == '-' or c == '+':
            t = self.tok()
            if t != c:
                self.refuse('operator %s' % t)
            self.i += 1
            return ('neg' if c == '-' else 'pos', self.unary())
        if c == '!':
            t = self.tok()
            if t != '!':
                self.refuse('operator %s' % t)
            self.i += 1
            return ('bang', self.unary())
        return self.power()

    def binop(self, level):
        """the operator at the cursor if it is of this level, consumed"""
        t = self.tok()
        if BINLEVEL.get(t) != level:
            return None
        if t in ('+', '-', '.', '*', '/', '%') and False:
            pass
        self.take(t)
        if t == 'x' and self.ch() == '=':
            self.refuse('x=')
        return t

    def level5(self):
        return self.binary(5)

    def binary(self, level):
        if level == 3:
            return self.unary()
        if level == 6:
            return self.binary(5)
        if level in (4, 5, 9, 10):
            e = self.binary(level - 1)
            while True:
                op = self.binop(level)
                if op is None:
                    return e
                e = ('bin', op, e, self.binary(level - 1))
        if level in (7, 8):
            e = self.binary(level - 1)
            op = self.binop(level)
            if op is None:
                return e
            l = e
            while l[0] == 'pos':
                l = l[1]
            if OPT4['amend_not_cmp'] and l[0] == 'bang' and op not in ('<=>', 'cmp'):
                self.refuse('AMENDED: ! as the left operand of %s' % op)
            e = ('bin', op, e, self.binary(level - 1))
            t = self.tok()
            if BINLEVEL.get(t) == level:
                self.refuse('%s after %s: no chaining' % (t, op))
            return e
        raise AssertionError(level)

    def ternary(self):
        c = self.binary(10)
        if self.tok() == '?':
            self.take('?')
            a = self.ternary()
            if self.tok() != ':':
                self.refuse('expected : at %r' % self.t[self.i:self.i + 10])
            self.take(':')
            b = self.ternary()
            return ('cond', c, a, b)
        return c

    def level12(self):
        # a leading not is a primary; anything else is a level-11 expression
        return self.ternary()

    def expr(self):
        e = self.level12()
        while True:
            op = self.binop(13)
            if op is None:
                break
            e = ('bin', op, e, self.level12())
        while True:
            op = self.binop(14)
            if op is None:
                return e
            r = self.level12()
            while True:
                op2 = self.binop(13)
                if op2 is None:
                    break
                r = ('bin', op2, r, self.level12())
            e = ('bin', op, e, r)

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
            if oneblank:
                j = self.i + 2
                level = 1
                while j < self.n and t[j] != '\n' and level:
                    level += (t[j] == '(') - (t[j] == ')')
                    j += 1
                while j < self.n and t[j] in ' \t':
                    j += 1
                if level or t[j:j + 1] != ';':
                    self.refuse('%s ( with brackets that do not balance as text on the line' % w)
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
                e = self.level12()
                self.skip()
                if self.ch() != ';':
                    self.refuse('expected ; at %r' % t[self.i:self.i + 10])
                self.i += 1
            listrep(e, self)
            stmts.append((w, e, line0))
        return {'stmts': stmts, 'open': use_open, 'utf8': self.utf8_line is not None}


def listrep(e, p):
    """refuse (...) x N in list position"""
    k = e[0]
    if k in ('paren', 'pos'):
        return listrep(e[1], p)
    if k == 'bin':
        if e[1] == 'x':
            l = e[2]
            while l[0] == 'pos':
                l = l[1]
            if l[0] == 'paren':
                p.refuse('(...) x N in list position')
        elif e[1] in ('||', '&&', '//', 'or', 'and'):
            listrep(e[3], p)
    elif k == 'cond':
        listrep(e[2], p)
        listrep(e[3], p)


def parse(src):
    if isinstance(src, bytes):
        try:
            src = src.decode('utf-8')
        except UnicodeDecodeError:
            raise Refuse('invalid UTF-8')
    try:
        return P4(src).program()
    except RecursionError:
        raise Refuse('too deep')


# ---------------------------------------------------------------- values

def num(v):
    if v is UNDEF:
        raise Fault('undef where a number is wanted')
    if isinstance(v, Bool):
        return Opnd(1 if v.t else 0, 'int')
    return M.num(v)


def tostr(v):
    if v is UNDEF:
        raise Fault('undef where a string is wanted')
    if isinstance(v, Bool):
        return '1' if v.t else ''
    return M.tostr(v)


def plain(v):
    """a Bool as the Int it is where a number is wanted (for the old model's functions)"""
    if v is UNDEF:
        raise Fault('undef where a number is wanted')
    if isinstance(v, Bool):
        return 1 if v.t else 0
    return v


def truth(v):
    if v is UNDEF:
        return False
    if isinstance(v, Bool):
        return v.t
    if isinstance(v, str):
        return v != '' and v != '0'
    return v != 0


def integral(o):
    if o.isint:
        return True
    return whole(o.v) and abs(o.v) < P53


def ncmp(a, b):
    """-1, 0, 1"""
    oa = num(a)
    ob = num(b)
    if OPT4['amend_cmp_pv']:
        for o, p in ((oa, ob), (ob, oa)):
            if o.kind in ('soft', 'B', 'Cnum', 'Cint') and p.isint and abs(p.v) >= P53:
                raise Fault('AMENDED: a string with a point or exponent compared with an Int of 2^53 or more')
    if integral(oa) and integral(ob) and not OPT4['mut_cmp_float']:
        x, y = int(oa.v), int(ob.v)
    else:
        x, y = float(oa.v), float(ob.v)
    return (x > y) - (x < y)


def scmp(a, b):
    x = tostr(a)
    y = tostr(b)
    kx = [ord(c) for c in x]
    ky = [ord(c) for c in y]
    return (kx > ky) - (kx < ky)


def B(t):
    return TRUE if t else FALSE


CMP = {
    '==': lambda c: c == 0, '!=': lambda c: c != 0, '<': lambda c: c < 0, '>': lambda c: c > 0,
    '<=': lambda c: c <= 0, '>=': lambda c: c >= 0,
    'eq': lambda c: c == 0, 'ne': lambda c: c != 0, 'lt': lambda c: c < 0, 'gt': lambda c: c > 0,
    'le': lambda c: c <= 0, 'ge': lambda c: c >= 0,
}


def ev(e):
    k = e[0]
    if k == 'lit':
        return e[1]
    if k == 'paren' or k == 'pos':
        v = ev(e[1])
        if k == 'pos':
            return v
        return v
    if k == 'neg':
        v = ev(e[1])
        return M.neg(plain(v))
    if k == 'bang':
        return B(not truth(ev(e[1])))
    if k == 'not':
        return B(not truth(ev(e[1])))
    if k == 'cond':
        return ev(e[2]) if truth(ev(e[1])) else ev(e[3])
    if k == 'bin':
        op = e[1]
        if op in ('&&', 'and'):
            a = ev(e[2])
            if not truth(a):
                return a
            b = ev(e[3])
            return B(truth(b)) if OPT4['mut_and_bool'] else b
        if op in ('||', 'or'):
            a = ev(e[2])
            if truth(a):
                return a
            return ev(e[3])
        if op == '//':
            a = ev(e[2])
            if a is not UNDEF:
                return a
            return ev(e[3])
        a = ev(e[2])
        b = ev(e[3])
        if op == 'xor':
            return B(truth(a) != truth(b))
        if op in ('==', '!=', '<', '>', '<=', '>='):
            return B(CMP[op](ncmp(a, b)))
        if op == '<=>':
            return ncmp(a, b)
        if op in ('eq', 'ne', 'lt', 'gt', 'le', 'ge'):
            return B(CMP[op](scmp(a, b)))
        if op == 'cmp':
            return scmp(a, b)
        if op == '.':
            return tostr(a) + tostr(b)
        if op == 'x':
            s = tostr(a)
            b = plain(b)
            n = M.integer(b)
            if n < 0:
                raise Fault('negative repeat count')
            if float(M.num(b).v) < 0 or n > I63 - 1:
                raise Fault('repeat count negative before cutting, or past the Ints')
            if n * max(len(s), 1) > BIG:
                raise Big()
            return s * n if s else ''
        return M.arith(op, plain(a), plain(b))
    if k == 'call':
        f = e[1]
        args = [ev(x) for x in e[2]]
        if f == 'defined':
            return B(args[0] is not UNDEF)
        if f == 'length':
            if args[0] is UNDEF:
                return UNDEF
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
            n = M.integer(plain(args[0]), 'chr')
            if n < 0 or n > 0x10FFFF or 0xD800 <= n <= 0xDFFF:
                raise Fault('chr of a number that is not a character')
            return chr(n)
        if f == 'substr':
            s = tostr(args[0])
            L = len(s)
            off = M.integer(plain(args[1]), 'pos')
            ln = M.integer(plain(args[2]), 'pos') if len(args) > 2 else None
            p1 = off + L if off < 0 else off
            if ln is None:
                p2 = L
            elif ln >= 0:
                p2 = p1 + ln
            else:
                p2 = L + ln
            if p1 > L:
                raise Fault('substr outside of string')
            if p1 < 0 and p2 < 0:
                raise Fault('substr wholly before the string')
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
            pos = M.integer(plain(args[2]), 'pos') if len(args) > 2 else 0
            pos = max(0, min(len(s), pos))
            return s.find(t, pos)
    raise AssertionError(e)


def safe(prog):
    """not part of the definition: no x in the program, dead branches too,
    builds a string over BIG characters (perl folds constants it never runs)"""
    def walk(e):
        if not isinstance(e, tuple):
            return
        if e[0] == 'bin' and e[1] == 'x':
            try:
                ev(e)
            except Fault:
                try:
                    c = ev(e[3])
                    if isinstance(c, (int, float)) and not isinstance(c, Bool) and abs(c) > BIG:
                        raise Big()
                except Fault:
                    pass
        for x in e[1:]:
            if isinstance(x, tuple):
                walk(x)
            elif isinstance(x, list):
                for y in x:
                    walk(y)
    for w, e, line in prog['stmts']:
        walk(e)


def kind(v):
    if v is UNDEF:
        return 'Undef'
    if isinstance(v, Bool):
        return 'Bool'
    return 'Int' if isinstance(v, int) else 'Num' if isinstance(v, float) else 'Str'


def run(prog, trace=None):
    out = []
    for idx, (w, e, line) in enumerate(prog['stmts']):
        try:
            v = ev(e)
            if v is UNDEF:
                raise Fault('print of undef')
            s = tostr(v)
            if not prog['open'] and any(ord(c) > 0x7F for c in s):
                raise Fault('print of a character past ASCII without use open')
            if any(M.nonchar(c) for c in s):
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


if __name__ == '__main__':
    import sys
    for s in sys.argv[1:]:
        try:
            pr = parse('use v5.42;\n' + s + '\n')
            print(s, '=>', pr['stmts'], run(pr))
        except Refuse as r:
            print(s, '=> REFUSED', r)

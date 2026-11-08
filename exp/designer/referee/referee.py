#!/usr/bin/env python3
"""Ditto referee: an independent interpreter built only from docs/LANGUAGE.md,
docs/DESIGN.md and docs/DECISIONS.md.  Usage: python3 referee.py FILE.ditto

Behaves as a compiled Ditto program: the program's output on stdout; a compile
error (exit 2) or a fault (exit 1) as one line on stderr.  Where the documents
are silent, the choice taken is listed in SILENCES.md (marked S<n> below)."""

import os
import re
import sys
import threading

MIN, MAX = -2 ** 63, 2 ** 63 - 1
KEYWORDS = {'and', 'break', 'continue', 'else', 'false', 'fn', 'for', 'if', 'in',
            'let', 'nil', 'not', 'or', 'return', 'true', 'while'}
# name -> arity (None: any number)
BUILTINS = {'print': None, 'str': 1, 'len': 1, 'int': 1, 'keys': 1, 'remove': 2,
            'sort': 1, 'slice': 3, 'words': 1, 'split': 2, 'join': 2, 'lower': 1,
            'upper': 1, 'read': 0, 'fail': 1}
OPS = ['..=', '..', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '+', '-',
       '*', '/', '%', '<', '>', '=', '(', ')', '[', ']', '{', '}', ',', ':', ';', '.']
COMPOUND = ('+=', '-=', '*=', '/=', '%=')
CMP_OPS = ('==', '!=', '<', '<=', '>', '>=', 'in')
MAX_DEPTH = 1000


class CompileError(Exception):
    def __init__(self, pos, msg):
        self.pos, self.msg = pos, msg


class Fault(Exception):
    def __init__(self, msg, pos):
        self.msg, self.pos = msg, pos


class Miss(Fault):
    """A lookup that found nothing; `else` catches it if the lookup node is
    written in its left operand."""
    def __init__(self, msg, pos, node):
        Fault.__init__(self, msg, pos)
        self.node = node


def lat(b):
    return b.decode('latin-1')


# ---------------------------------------------------------------- lexer

class Tok:
    __slots__ = ('kind', 'text', 'pos', 'val')

    def __init__(self, kind, text, pos, val=None):
        self.kind, self.text, self.pos, self.val = kind, text, pos, val


def found(t):
    if t.kind == 'eof':
        return 'end of file'
    if t.kind == 'nl':
        return 'newline'
    if t.kind == 'str':
        return 'string'
    return "'" + t.text + "'"


class RunOff(Exception):
    """A string reached the end of its line."""
    def __init__(self, start):
        self.start = start


def is_digit(c):
    return 48 <= c <= 57


def is_alpha(c):
    return 65 <= c <= 90 or 97 <= c <= 122 or c == 95


ESCAPES = {ord('n'): 10, ord('t'): 9, ord('r'): 13, ord('\\'): 92, ord('"'): 34,
           ord('{'): 123, ord('}'): 125}


class Lexer:
    def __init__(self, src):
        self.src, self.n = src, len(src)
        self.line, self.ls = 1, 0

    def pos(self, i):
        return (self.line, i - self.ls + 1)

    def err(self, i, msg):
        raise CompileError(self.pos(i), msg)

    def token(self, i):
        """One name, keyword, int or operator token at i."""
        src, n, c = self.src, self.n, self.src[i]
        if is_digit(c):
            j = i
            while j < n and (is_alpha(src[j]) or is_digit(src[j])):
                j += 1
            text = lat(src[i:j])
            if not re.fullmatch(r'[0-9]+(_[0-9]+)*', text):
                self.err(i, 'malformed number')
            v = int(text.replace('_', ''))
            if v > MAX:
                self.err(i, 'integer literal too large')
            return Tok('int', text, self.pos(i), v), j
        if is_alpha(c):
            j = i
            while j < n and (is_alpha(src[j]) or is_digit(src[j])):
                j += 1
            text = lat(src[i:j])
            return Tok(text if text in KEYWORDS else 'name', text, self.pos(i)), j
        for op in OPS:
            if src.startswith(op.encode(), i):
                return Tok(op, op, self.pos(i)), i + len(op)
        if 0x21 <= c <= 0x7e:
            self.err(i, "unexpected character '%s'" % chr(c))
        self.err(i, 'unexpected byte 0x%02X' % c)

    def string(self, i):
        """A string literal at i; parts alternate bytes and token lists."""
        src, n, start = self.src, self.n, i
        parts, buf = [], bytearray()
        i += 1
        while True:
            if i >= n or src[i] == 10:
                raise RunOff(start)
            c = src[i]
            if c == 34:
                i += 1
                break
            if c == 92:
                if i + 1 >= n or src[i + 1] == 10:
                    raise RunOff(start)
                e = src[i + 1]
                if e not in ESCAPES:
                    self.err(i, "unknown escape '\\%s'" % chr(e))  # S2
                buf.append(ESCAPES[e])
                i += 2
                continue
            if c == 123:
                parts.append(bytes(buf))
                buf = bytearray()
                toks, i = self.interp(i)
                parts.append(toks)
                continue
            buf.append(c)
            i += 1
        parts.append(bytes(buf))
        return Tok('str', '', self.pos(start), parts), i

    def interp(self, i):
        src, n, brace = self.src, self.n, i
        j = i + 1
        while j < n and src[j] in (32, 9, 13):
            j += 1
        if j < n and src[j] == 125:
            self.err(brace, 'empty interpolation')
        toks, depth = [], 0
        while True:
            if j >= n or src[j] == 10:
                self.err(brace, 'unterminated interpolation')
            c = src[j]
            if c in (32, 9, 13):
                j += 1
                continue
            if c == 47 and j + 1 < n and src[j + 1] == 47:  # S3: comment eats the line
                self.err(brace, 'unterminated interpolation')
            if c == 34:
                try:
                    t, j = self.string(j)
                except RunOff:
                    self.err(brace, 'unterminated interpolation')
                toks.append(t)
                continue
            t, j2 = self.token(j)
            if t.kind == '{':
                depth += 1
            elif t.kind == '}':
                if depth == 0:
                    toks.append(t)
                    toks.append(Tok('eof', '', self.pos(j2)))
                    return toks, j2
                depth -= 1
            toks.append(t)
            j = j2

    def lex(self):
        src, n = self.src, self.n
        toks, stack, i = [], [], 0
        while i < n:
            c = src[i]
            if c in (32, 9, 13):
                i += 1
                continue
            if c == 10:
                if not (stack and stack[-1] in ('(', '[')):
                    if toks and toks[-1].kind != 'nl':
                        toks.append(Tok('nl', '', self.pos(i)))
                i += 1
                self.line += 1
                self.ls = i
                continue
            if c == 47 and i + 1 < n and src[i + 1] == 47:
                while i < n and src[i] != 10:
                    i += 1
                continue
            if c == 34:
                try:
                    t, i = self.string(i)
                except RunOff as r:
                    self.err(r.start, 'unterminated string')
                toks.append(t)
                continue
            t, i = self.token(i)
            if t.kind in ('(', '[', '{'):
                stack.append(t.kind)
            elif t.kind in (')', ']', '}') and stack:
                stack.pop()
            toks.append(t)
        toks.append(Tok('eof', '', self.pos(n)))
        return toks


# ---------------------------------------------------------------- parser

class Node:
    def __init__(self, kind, pos, **kw):
        self.kind, self.pos, self.start = kind, pos, pos
        self.__dict__.update(kw)


def copy_node(n):
    m = Node.__new__(Node)
    m.__dict__.update(n.__dict__)
    return m


class Parser:
    def __init__(self, toks):
        self.toks, self.i, self.mapd = toks, 0, 0

    def at(self, k):
        i = self.i
        while True:
            t = self.toks[i]
            if t.kind == 'eof':
                return i
            if t.kind == 'nl' and self.mapd:
                i += 1
                continue
            if k == 0:
                return i
            k -= 1
            i += 1

    def peek(self, k=0):
        return self.toks[self.at(k)]

    def adv(self):
        j = self.at(0)
        t = self.toks[j]
        if t.kind != 'eof':
            self.i = j + 1
        return t

    def skipnl(self):
        while self.toks[self.i].kind == 'nl':
            self.i += 1

    def fail(self, what, t):
        raise CompileError(t.pos, 'expected %s, found %s' % (what, found(t)))

    def expect(self, kind, what):
        t = self.peek()
        if t.kind != kind:
            self.fail(what, t)
        return self.adv()

    # statements

    def program(self):
        items = []
        while True:
            t = self.peek()
            if t.kind == 'nl':
                self.adv()
                continue
            if t.kind == 'eof':
                return items
            items.append(self.statement(True))
            self.end_statement()

    def end_statement(self):
        t = self.peek()
        if t.kind in ('nl', ';'):
            self.adv()
        elif t.kind not in ('}', 'eof'):
            self.fail('newline', t)

    def block(self):
        self.expect('{', "'{'")
        body = []
        while True:
            t = self.peek()
            if t.kind == 'nl':
                self.adv()
                continue
            if t.kind == '}':
                self.adv()
                return body
            if t.kind == 'eof':
                self.fail("'}'", t)
            body.append(self.statement(False))
            self.end_statement()

    def statement(self, top):
        t = self.peek()
        k = t.kind
        if k == 'let':
            self.adv()
            name = self.expect('name', 'a name')
            self.expect('=', "'='")
            self.skipnl()
            return Node('let', t.pos, name=name.text, npos=name.pos, e=self.expr())
        if k == 'if':
            return self.if_statement()
        if k == 'while':
            self.adv()
            cond = self.expr()
            return Node('while', t.pos, cond=cond, body=self.block())
        if k == 'for':
            self.adv()
            name = self.expect('name', 'a name')
            self.expect('in', "'in'")
            e = self.expr()
            if self.peek().kind in ('..', '..='):
                incl = self.adv().kind == '..='
                self.skipnl()  # S5
                hi = self.expr()
                return Node('forrange', t.pos, name=name.text, npos=name.pos, lo=e, hi=hi,
                            incl=incl, body=self.block())
            return Node('foreach', t.pos, name=name.text, npos=name.pos, e=e,
                        body=self.block())
        if k in ('break', 'continue'):
            self.adv()
            return Node(k, t.pos)
        if k == 'return':
            self.adv()
            e = None
            if self.peek().kind not in ('nl', ';', '}', 'eof'):
                e = self.expr()
            return Node('return', t.pos, e=e)
        if k == 'fn':
            if not top:
                raise CompileError(t.pos, 'functions are defined at the top level')
            return self.function()
        if k in ('name', 'int', 'str', 'true', 'false', 'nil', '(', '[', '-', 'not'):
            e = self.expr()
            op = self.peek()
            if op.kind == '=' or op.kind in COMPOUND:
                steps = []
                base = e
                while base.kind in ('index', 'field'):
                    steps.append(base)
                    base = base.obj
                if base.kind != 'name':
                    raise CompileError(t.pos, 'cannot assign to this')
                steps.reverse()
                self.adv()
                self.skipnl()
                rhs = self.expr()
                return Node('assign', op.pos, name=base.name, npos=base.pos, steps=steps,
                            op=op.kind, rhs=rhs)
            if e.kind != 'call':  # S6: before the terminator check
                raise CompileError(t.pos, 'expression statement must be a call')
            return Node('exprstmt', t.pos, e=e)
        self.fail('a statement', t)

    def if_statement(self):
        t = self.adv()
        cond = self.expr()
        body = self.block()
        els = None
        nxt = self.peek()
        if nxt.kind == 'nl' and self.peek(1).kind == 'else':
            self.adv()
            nxt = self.peek()
        if nxt.kind == 'else':
            self.adv()
            self.skipnl()  # S7
            if self.peek().kind == 'if':
                els = [self.if_statement()]
            else:
                els = self.block()
        return Node('if', t.pos, cond=cond, body=body, els=els)

    def function(self):
        t = self.adv()
        name = self.expect('name', 'a name')
        self.expect('(', "'('")
        params = []
        while True:
            if self.peek().kind == ')':
                self.adv()
                break
            p = self.expect('name', 'a name')
            params.append((p.text, p.pos))
            if self.peek().kind == ',':
                self.adv()
            elif self.peek().kind == ')':
                self.adv()
                break
            else:
                self.fail("')'", self.peek())
        body = self.block()
        return Node('fn', t.pos, name=name.text, npos=name.pos, params=params, body=body)

    # expressions, loosest first

    def expr(self):
        left = self.and_expr()
        while self.peek().kind == 'or':
            op = self.adv()
            self.skipnl()
            left = self.binary('or', op, left, self.and_expr())
        return left

    def binary(self, op, tok, left, right):
        n = Node('bin', tok.pos, op=op, l=left, r=right)
        n.start = left.start
        return n

    def and_expr(self):
        left = self.not_expr()
        while self.peek().kind == 'and':
            op = self.adv()
            self.skipnl()
            left = self.binary('and', op, left, self.not_expr())
        return left

    def not_expr(self):
        if self.peek().kind == 'not':
            t = self.adv()
            return Node('not', t.pos, e=self.not_expr())
        return self.cmp_expr()

    def cmp_op(self):
        t = self.peek()
        if t.kind in CMP_OPS:
            return t.kind
        if t.kind == 'not' and self.peek(1).kind == 'in':
            return 'not in'
        return None

    def cmp_expr(self):
        left = self.add_expr()
        op = self.cmp_op()
        if op is None:
            return left
        tok = self.adv()
        if op == 'not in':
            self.adv()
        self.skipnl()
        n = self.binary(op, tok, left, self.add_expr())
        if self.cmp_op() is not None:
            raise CompileError(self.peek().pos, 'comparisons do not chain')
        return n

    def add_expr(self):
        left = self.mul_expr()
        while self.peek().kind in ('+', '-'):
            op = self.adv()
            self.skipnl()
            left = self.binary(op.kind, op, left, self.mul_expr())
        return left

    def mul_expr(self):
        left = self.else_expr()
        while self.peek().kind in ('*', '/', '%'):
            op = self.adv()
            self.skipnl()
            left = self.binary(op.kind, op, left, self.else_expr())
        return left

    def else_expr(self):
        left = self.neg_expr()
        while self.peek().kind == 'else':
            op = self.adv()
            self.skipnl()
            n = Node('else', op.pos, l=left, r=self.neg_expr())
            n.start = left.start
            left = n
        return left

    def neg_expr(self):
        if self.peek().kind == '-':
            t = self.adv()
            return Node('neg', t.pos, e=self.neg_expr())
        return self.postfix()

    def postfix(self):
        e = self.primary()
        while True:
            t = self.peek()
            if t.kind == '[':
                self.adv()
                idx = self.expr()
                self.expect(']', "']'")
                n = Node('index', t.pos, obj=e, idx=idx)
            elif t.kind == '.':
                self.adv()
                name = self.expect('name', 'a name')
                n = Node('field', t.pos, obj=e, fname=name.text)
            else:
                return e
            n.start = e.start
            e = n

    def primary(self):
        t = self.peek()
        k = t.kind
        if k == 'int':
            self.adv()
            return Node('int', t.pos, val=t.val)
        if k == 'str':
            self.adv()
            return self.string(t)
        if k in ('true', 'false'):
            self.adv()
            return Node('bool', t.pos, val=(k == 'true'))
        if k == 'nil':
            self.adv()
            return Node('nil', t.pos)
        if k == 'name':
            self.adv()
            if self.peek().kind == '(':
                self.adv()
                args = []
                while True:
                    if self.peek().kind == ')':
                        self.adv()
                        break
                    args.append(self.expr())
                    if self.peek().kind == ',':
                        self.adv()
                    elif self.peek().kind == ')':
                        self.adv()
                        break
                    else:
                        self.fail("')'", self.peek())
                return Node('call', t.pos, name=t.text, args=args)
            return Node('name', t.pos, name=t.text)
        if k == '(':
            self.adv()
            e = self.expr()
            self.expect(')', "')'")
            e = copy_node(e)
            e.start = t.pos
            return e
        if k == '[':
            self.adv()
            items = []
            while True:
                if self.peek().kind == ']':
                    self.adv()
                    break
                items.append(self.expr())
                if self.peek().kind == ',':
                    self.adv()
                elif self.peek().kind == ']':
                    self.adv()
                    break
                else:
                    self.fail("']'", self.peek())
            return Node('list', t.pos, items=items)
        if k == '{':
            return self.map_literal()
        self.fail('an expression', t)

    def string(self, t):
        parts = []
        for p in t.val:
            if isinstance(p, bytes):
                if p:
                    parts.append(p)
            else:
                saved = (self.toks, self.i, self.mapd)
                self.toks, self.i, self.mapd = p, 0, 0
                e = self.expr()
                if self.peek().kind != '}':
                    self.fail("'}'", self.peek())
                self.toks, self.i, self.mapd = saved
                parts.append(e)
        return Node('str', t.pos, parts=parts, simple=len(t.val) == 1, val=t.val[0])

    def map_literal(self):
        t = self.adv()
        self.mapd += 1
        keys, values = [], []
        while True:
            kt = self.peek()
            if kt.kind == '}':
                self.adv()
                break
            if kt.kind == 'name':
                key = kt.text.encode()
                self.adv()
            elif kt.kind == 'str' and len(kt.val) == 1:
                key = kt.val[0]
                self.adv()
            elif kt.kind == 'int':
                key = kt.val
                self.adv()
            elif kt.kind == '-' and self.peek(1).kind == 'int':
                self.adv()
                key = -self.adv().val
            else:
                raise CompileError(kt.pos, 'map key must be a name, a string or an int')
            self.expect(':', "':'")
            keys.append((key, kt.pos))
            values.append(self.expr())
            nt = self.peek()
            if nt.kind == ',':
                self.adv()
            elif nt.kind == '}':
                self.adv()
                break
            else:
                self.fail("'}'", nt)
        self.mapd -= 1
        return Node('map', t.pos, keys=keys, values=values)


# ---------------------------------------------------------------- resolver

def children(n):
    k = n.kind
    if k == 'bin' or k == 'else':
        return [n.l, n.r]
    if k in ('neg', 'not'):
        return [n.e]
    if k == 'index':
        return [n.obj, n.idx]
    if k == 'field':
        return [n.obj]
    if k == 'call':
        return n.args
    if k == 'list':
        return n.items
    if k == 'map':
        return n.values
    if k == 'str':
        return [p for p in n.parts if isinstance(p, Node)]
    return []


def lookups(n, acc):
    if n.kind in ('index', 'field') or (n.kind == 'call' and n.name == 'int'):
        acc.add(n)
    for c in children(n):
        lookups(c, acc)
    return acc


class Resolver:
    def __init__(self, items):
        self.items = items
        self.fns = {}
        for it in items:
            if it.kind == 'fn' and it.name not in self.fns:
                self.fns[it.name] = it
        self.top_names = set()
        for it in items:
            if it.kind != 'fn':
                self.collect(it)

    def collect(self, s):
        if s.kind in ('let', 'forrange', 'foreach'):
            self.top_names.add(s.name)
        for attr in ('body', 'els'):
            for b in getattr(s, attr, None) or []:
                self.collect(b)

    def err(self, pos, msg):
        raise CompileError(pos, msg)

    def run(self):
        top_scopes = [set()]
        seen = set()
        for it in self.items:
            if it.kind == 'fn':
                if it.name in BUILTINS:
                    self.err(it.npos, '%s is a builtin' % it.name)
                if it.name in seen:
                    self.err(it.npos, 'duplicate function %s' % it.name)
                seen.add(it.name)
                self.scopes, self.in_fn, self.loops = [set()], True, 0
                for p, ppos in it.params:
                    if p in self.scopes[0]:
                        self.err(ppos, '%s is already declared' % p)
                    self.scopes[0].add(p)
                self.block(it.body)
            else:
                self.scopes, self.in_fn, self.loops = top_scopes, False, 0
                self.stmt(it)

    def declared(self, name):
        return any(name in s for s in self.scopes)

    def declare(self, name, pos):
        if self.declared(name):
            self.err(pos, '%s is already declared' % name)

    def var(self, name, pos):
        if self.declared(name):
            return
        if name in self.fns or name in BUILTINS:  # S8
            self.err(pos, 'functions are not values')
        if self.in_fn and name in self.top_names:
            self.err(pos, '%s is a top-level variable; functions see only their '
                          'parameters and their own variables' % name)
        self.err(pos, 'unknown variable %s' % name)

    def block(self, stmts, loop_var=None):
        self.scopes.append(set())
        for s in stmts:
            self.stmt(s)
        self.scopes.pop()

    def stmt(self, s):
        k = s.kind
        if k == 'let':
            self.declare(s.name, s.npos)
            self.expr(s.e)
            self.scopes[-1].add(s.name)
        elif k == 'assign':
            self.var(s.name, s.npos)  # S9: same check as a read
            for st in s.steps:
                if st.kind == 'index':
                    self.expr(st.idx)
            self.expr(s.rhs)
        elif k == 'exprstmt':
            self.expr(s.e)
        elif k == 'if':
            self.expr(s.cond)
            self.block(s.body)
            if s.els is not None:
                self.block(s.els)
        elif k == 'while':
            self.expr(s.cond)
            self.loops += 1
            self.block(s.body)
            self.loops -= 1
        elif k in ('forrange', 'foreach'):
            self.declare(s.name, s.npos)  # S10: the name before the header's expressions
            if k == 'forrange':
                self.expr(s.lo)
                self.expr(s.hi)
            else:
                self.expr(s.e)
            self.scopes.append({s.name})
            self.loops += 1
            for b in s.body:
                self.stmt(b)
            self.loops -= 1
            self.scopes.pop()
        elif k in ('break', 'continue'):
            if self.loops == 0:
                self.err(s.pos, '%s outside a loop' % k)
        elif k == 'return':
            if not self.in_fn:
                self.err(s.pos, 'return outside a function')
            if s.e is not None:
                self.expr(s.e)
        elif k == 'fn':  # unreachable: the parser rejects nested fn
            self.err(s.pos, 'functions are defined at the top level')

    def expr(self, n):
        k = n.kind
        if k == 'name':
            self.var(n.name, n.pos)
        elif k == 'call':
            if n.name in self.fns:
                want = len(self.fns[n.name].params)
            elif n.name in BUILTINS:
                want = BUILTINS[n.name]
            else:
                self.err(n.pos, 'unknown function %s' % n.name)
            if want is not None and want != len(n.args):
                self.err(n.pos, '%s takes %d argument%s, got %d'
                         % (n.name, want, '' if want == 1 else 's', len(n.args)))
            for a in n.args:
                self.expr(a)
        elif k == 'else':
            self.expr(n.l)
            n.catch = lookups(n.l, set())
            if not n.catch:
                self.err(n.pos, 'else needs a lookup on its left: an index, a field or int()')
            self.expr(n.r)
        elif k == 'map':
            seen = set()
            for (key, kpos), v in zip(n.keys, n.values):
                if key in seen:
                    self.err(kpos, 'duplicate key %s' % lat(show(key, False)))
                seen.add(key)
                self.expr(v)
        else:
            for c in children(n):
                self.expr(c)


# ---------------------------------------------------------------- values

class DMap:
    """An immutable map; d is never changed after construction."""
    __slots__ = ('d',)

    def __init__(self, d):
        self.d = d


def tname(v):
    if v is None:
        return 'nil'
    t = type(v)
    if t is bool:
        return 'bool'
    if t is int:
        return 'int'
    if t is bytes:
        return 'string'
    if t is tuple:
        return 'list'
    return 'map'


def is_key(v):
    return type(v) is int or type(v) is bytes


def quote(s):
    return (b'"' + s.replace(b'\\', b'\\\\').replace(b'"', b'\\"').replace(b'\n', b'\\n')
            .replace(b'\t', b'\\t').replace(b'\r', b'\\r') + b'"')


def show(v, top=True):
    t = type(v)
    if t is bytes:
        return v if top else quote(v)
    if v is None:
        return b'nil'
    if t is bool:
        return b'true' if v else b'false'
    if t is int:
        return str(v).encode()
    if t is tuple:
        return b'[' + b', '.join(show(x, False) for x in v) + b']'
    return b'{' + b', '.join(show(k, False) + b': ' + show(x, False)
                            for k, x in v.d.items()) + b'}'


def deq(a, b):
    t = type(a)
    if t is not type(b):
        return False
    if t is tuple:
        return len(a) == len(b) and all(deq(x, y) for x, y in zip(a, b))
    if t is DMap:
        if len(a.d) != len(b.d):
            return False
        for k, x in a.d.items():
            if k not in b.d or not deq(x, b.d[k]):
                return False
        return True
    return a == b


def cmp3(a, b, op, pos):
    """-1, 0 or 1; faults on a pair < can't order, naming the pair met."""
    ta, tb = type(a), type(b)
    if (ta is int and tb is int) or (ta is bytes and tb is bytes):
        return (a > b) - (a < b)
    if ta is tuple and tb is tuple:
        for x, y in zip(a, b):
            c = cmp3(x, y, op, pos)
            if c:
                return c
        return (len(a) > len(b)) - (len(a) < len(b))
    raise Fault('cannot use %s on %s and %s' % (op, tname(a), tname(b)), pos)


def check_int(v, pos):
    if v < MIN or v > MAX:
        raise Fault('integer overflow', pos)
    return v


def arith(op, a, b, pos):
    ta, tb = type(a), type(b)
    if op == '+':
        if ta is int and tb is int:
            return check_int(a + b, pos)
        if (ta is bytes and tb is bytes) or (ta is tuple and tb is tuple):
            return a + b
        raise Fault('cannot use + on %s and %s' % (tname(a), tname(b)), pos)
    if not (ta is int and tb is int):
        raise Fault('cannot use %s on %s and %s' % (op, tname(a), tname(b)), pos)
    if op == '-':
        return check_int(a - b, pos)
    if op == '*':
        return check_int(a * b, pos)
    if b == 0:
        raise Fault('division by zero', pos)
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    if op == '/':
        return check_int(q, pos)
    return a - b * q


def do_index(c, k, node):
    tc = type(c)
    if tc is tuple or tc is bytes:
        if type(k) is not int:
            raise Fault('%s index must be an int, got %s'
                        % ('list' if tc is tuple else 'string', tname(k)), node.pos)
        if 0 <= k < len(c):
            return c[k] if tc is tuple else c[k:k + 1]
        raise Miss('index %d out of range (length %d)' % (k, len(c)), node.pos, node)
    if tc is DMap:
        if not is_key(k):
            raise Fault('map key must be an int or a string, got %s' % tname(k), node.pos)
        if k in c.d:
            return c.d[k]
        raise Miss('missing key %s' % lat(show(k, False)), node.pos, node)
    raise Fault('cannot index %s' % tname(c), node.pos)


def do_field(c, node):
    if type(c) is DMap:
        k = node.fname.encode()
        if k in c.d:
            return c.d[k]
        raise Miss('missing key %s' % lat(show(k, False)), node.pos, node)
    raise Fault('cannot use .%s on %s' % (node.fname, tname(c)), node.pos)


def set_step(c, k, node, v):
    tc = type(c)
    if node.kind == 'field':
        if tc is DMap:
            d = dict(c.d)
            d[k] = v
            return DMap(d)
        if tc is tuple:
            raise Fault('cannot use .%s on list' % node.fname, node.pos)
        raise Fault('cannot assign into %s' % tname(c), node.pos)
    if tc is tuple:
        if type(k) is not int:
            raise Fault('list index must be an int, got %s' % tname(k), node.pos)
        if not 0 <= k < len(c):
            raise Fault('index %d out of range (length %d)' % (k, len(c)), node.pos)
        return c[:k] + (v,) + c[k + 1:]
    if tc is DMap:
        if not is_key(k):
            raise Fault('map key must be an int or a string, got %s' % tname(k), node.pos)
        d = dict(c.d)
        d[k] = v
        return DMap(d)
    raise Fault('cannot assign into %s' % tname(c), node.pos)


def merge_sort(xs, pos):
    # S12: top-down, left half the first len//2; the later item goes first
    # only when strictly less, so the pair compared is (later, earlier).
    if len(xs) < 2:
        return list(xs)
    mid = len(xs) // 2
    left, right = merge_sort(xs[:mid], pos), merge_sort(xs[mid:], pos)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if cmp3(right[j], left[i], '<', pos) < 0:
            out.append(right[j])
            j += 1
        else:
            out.append(left[i])
            i += 1
    return out + left[i:] + right[j:]


WORD_SEP = re.compile(rb'[ \t\n\r]+')


# ---------------------------------------------------------------- interpreter

class Ret:
    __slots__ = ('val',)

    def __init__(self, val):
        self.val = val


BREAK, CONTINUE = object(), object()


class Interp:
    def __init__(self, items, out):
        self.fns = {}
        for it in items:
            if it.kind == 'fn' and it.name not in self.fns:
                self.fns[it.name] = it
        self.top = [it for it in items if it.kind != 'fn']
        self.out = out
        self.depth = 0
        self.stdin_done = False
        self.E = {k: getattr(self, 'e_' + k) for k in
                  ('int', 'str', 'bool', 'nil', 'name', 'call', 'list', 'map', 'index',
                   'field', 'neg', 'not', 'bin', 'else')}
        self.X = {k: getattr(self, 'x_' + k) for k in
                  ('let', 'assign', 'exprstmt', 'if', 'while', 'forrange', 'foreach',
                   'break', 'continue', 'return')}

    def run(self):
        self.block(self.top, {})

    def ev(self, n, env):
        return self.E[n.kind](n, env)

    # expressions

    def e_int(self, n, env):
        return n.val

    def e_bool(self, n, env):
        return n.val

    def e_nil(self, n, env):
        return None

    def e_str(self, n, env):
        if n.simple:
            return n.val
        return b''.join(p if isinstance(p, bytes) else show(self.ev(p, env))
                        for p in n.parts)

    def e_name(self, n, env):
        return env[n.name]

    def e_list(self, n, env):
        return tuple(self.ev(x, env) for x in n.items)

    def e_map(self, n, env):
        d = {}
        for (k, _), v in zip(n.keys, n.values):
            d[k] = self.ev(v, env)
        return DMap(d)

    def e_index(self, n, env):
        c = self.ev(n.obj, env)
        k = self.ev(n.idx, env)
        return do_index(c, k, n)

    def e_field(self, n, env):
        return do_field(self.ev(n.obj, env), n)

    def e_neg(self, n, env):
        v = self.ev(n.e, env)
        if type(v) is not int:
            raise Fault('cannot use - on %s' % tname(v), n.pos)
        return check_int(-v, n.pos)

    def e_not(self, n, env):
        v = self.ev(n.e, env)
        if type(v) is not bool:
            raise Fault('cannot use not on %s' % tname(v), n.pos)
        return not v

    def e_bin(self, n, env):
        op = n.op
        if op == 'and' or op == 'or':
            a = self.ev(n.l, env)
            if type(a) is not bool:
                raise Fault('cannot use %s on %s' % (op, tname(a)), n.pos)
            if a == (op == 'or'):
                return a
            b = self.ev(n.r, env)
            if type(b) is not bool:
                raise Fault('cannot use %s on %s' % (op, tname(b)), n.pos)
            return b
        a = self.ev(n.l, env)
        b = self.ev(n.r, env)
        if op == '==':
            return deq(a, b)
        if op == '!=':
            return not deq(a, b)
        if op == '<':
            return cmp3(a, b, op, n.pos) < 0
        if op == '<=':
            return cmp3(a, b, op, n.pos) <= 0
        if op == '>':
            return cmp3(a, b, op, n.pos) > 0
        if op == '>=':
            return cmp3(a, b, op, n.pos) >= 0
        if op == 'in':
            return self.contains(a, b, n.pos)
        if op == 'not in':
            return not self.contains(a, b, n.pos)
        return arith(op, a, b, n.pos)

    def contains(self, x, c, pos):
        tc = type(c)
        if tc is DMap:
            return is_key(x) and x in c.d
        if tc is tuple:
            return any(deq(x, e) for e in c)
        if tc is bytes and type(x) is bytes:
            return x in c
        raise Fault('cannot use in on %s and %s' % (tname(x), tname(c)), pos)

    def e_else(self, n, env):
        try:
            return self.ev(n.l, env)
        except Miss as m:
            if m.node in n.catch:
                return self.ev(n.r, env)
            raise

    def e_call(self, n, env):
        args = [self.ev(a, env) for a in n.args]
        fn = self.fns.get(n.name)
        if fn is None:
            return self.builtin(n, args)
        if self.depth >= MAX_DEPTH:
            raise Fault('stack overflow (more than %d nested calls)' % MAX_DEPTH, n.pos)
        self.depth += 1
        try:
            r = self.block(fn.body, {p: a for (p, _), a in zip(fn.params, args)})
        except Miss as m:
            raise Fault(m.msg, m.pos) from None  # a miss never crosses a call
        finally:
            self.depth -= 1
        return r.val if isinstance(r, Ret) else None

    def builtin(self, n, args):
        name, pos = n.name, n.pos

        def want(v, ok, what):
            if not ok:
                raise Fault('%s: expected %s, got %s' % (name, what, tname(v)), pos)

        if name == 'print':
            self.out.append(b' '.join(show(a) for a in args) + b'\n')
            return None
        if name == 'str':
            return show(args[0])
        if name == 'len':
            v = args[0]
            want(v, type(v) in (bytes, tuple, DMap), 'a string, list or map')
            return len(v.d) if type(v) is DMap else len(v)
        if name == 'int':
            s = args[0]
            want(s, type(s) is bytes, 'a string')
            if re.fullmatch(rb'-?[0-9]+', s):
                v = int(s)
                if MIN <= v <= MAX:
                    return v
            raise Miss('not a number: %s' % lat(quote(s)), pos, n)
        if name == 'keys':
            want(args[0], type(args[0]) is DMap, 'a map')
            return tuple(args[0].d.keys())
        if name == 'remove':
            m, k = args
            want(m, type(m) is DMap, 'a map')
            if is_key(k) and k in m.d:
                d = dict(m.d)
                del d[k]
                return DMap(d)
            return m
        if name == 'sort':
            want(args[0], type(args[0]) is tuple, 'a list')
            return tuple(merge_sort(list(args[0]), pos))
        if name == 'slice':
            x, a, b = args
            want(x, type(x) in (tuple, bytes), 'a list or string')
            want(a, type(a) is int, 'an int')
            want(b, type(b) is int, 'an int')
            if not 0 <= a <= b <= len(x):
                raise Fault('slice %d..%d out of range (length %d)' % (a, b, len(x)), pos)
            return x[a:b]
        if name == 'words':
            want(args[0], type(args[0]) is bytes, 'a string')
            return tuple(w for w in WORD_SEP.split(args[0]) if w)
        if name == 'split':
            s, sep = args
            want(s, type(s) is bytes, 'a string')
            want(sep, type(sep) is bytes, 'a string')
            if sep == b'':
                raise Fault('split: empty separator', pos)
            return tuple(s.split(sep))
        if name == 'join':
            xs, sep = args
            want(xs, type(xs) is tuple, 'a list of strings')
            for x in xs:
                want(x, type(x) is bytes, 'a list of strings')
            want(sep, type(sep) is bytes, 'a string')
            return sep.join(xs)
        if name in ('lower', 'upper'):
            want(args[0], type(args[0]) is bytes, 'a string')
            return args[0].lower() if name == 'lower' else args[0].upper()
        if name == 'read':
            if self.stdin_done:
                return b''
            self.stdin_done = True
            return sys.stdin.buffer.read()
        if name == 'fail':
            v = args[0]
            raise Fault(lat(v) if type(v) is bytes else lat(show(v)), pos)
        raise AssertionError(name)

    # statements

    def block(self, stmts, env):
        X = self.X
        for s in stmts:
            r = X[s.kind](s, env)
            if r is not None:
                return r
        return None

    def x_let(self, s, env):
        env[s.name] = self.ev(s.e, env)

    def x_exprstmt(self, s, env):
        self.ev(s.e, env)

    def lookup(self, c, k, st):
        return do_index(c, k, st) if st.kind == 'index' else do_field(c, st)

    def x_assign(self, s, env):
        keys = [self.ev(st.idx, env) if st.kind == 'index' else st.fname.encode()
                for st in s.steps]
        if s.op == '=':
            val = self.ev(s.rhs, env)
        else:
            cur = env[s.name]
            for st, k in zip(s.steps, keys):
                cur = self.lookup(cur, k, st)
            rhs = self.ev(s.rhs, env)
            val = arith(s.op[0], cur, rhs, s.pos)  # S11: message names + not +=
        if not s.steps:
            env[s.name] = val
            return None
        conts = [env[s.name]]
        for st, k in zip(s.steps[:-1], keys):
            conts.append(self.lookup(conts[-1], k, st))
        new = val
        for i in range(len(s.steps) - 1, -1, -1):
            new = set_step(conts[i], keys[i], s.steps[i], new)
        env[s.name] = new
        return None

    def cond(self, e, env):
        v = self.ev(e, env)
        if type(v) is not bool:
            raise Fault('condition must be a bool, got %s' % tname(v), e.start)
        return v

    def x_if(self, s, env):
        if self.cond(s.cond, env):
            return self.block(s.body, env)
        if s.els is not None:
            return self.block(s.els, env)
        return None

    def loop_body(self, s, env):
        r = self.block(s.body, env)
        if r is CONTINUE:
            return None
        return r

    def x_while(self, s, env):
        while self.cond(s.cond, env):
            r = self.loop_body(s, env)
            if r is BREAK:
                break
            if r is not None:
                return r
        return None

    def x_forrange(self, s, env):
        lo = self.ev(s.lo, env)
        hi = self.ev(s.hi, env)
        for b, e in ((lo, s.lo), (hi, s.hi)):
            if type(b) is not int:
                raise Fault('range bounds must be ints, got %s' % tname(b), e.start)
        k = lo
        end = hi + 1 if s.incl else hi
        while k < end:
            env[s.name] = k
            r = self.loop_body(s, env)
            if r is BREAK:
                break
            if r is not None:
                return r
            k += 1
        return None

    def x_foreach(self, s, env):
        v = self.ev(s.e, env)
        t = type(v)
        if t is tuple:
            items = v
        elif t is DMap:
            items = list(v.d.keys())
        elif t is bytes:
            items = [v[i:i + 1] for i in range(len(v))]
        else:
            raise Fault('cannot iterate over %s' % tname(v), s.e.start)
        for x in items:
            env[s.name] = x
            r = self.loop_body(s, env)
            if r is BREAK:
                break
            if r is not None:
                return r
        return None

    def x_break(self, s, env):
        return BREAK

    def x_continue(self, s, env):
        return CONTINUE

    def x_return(self, s, env):
        return Ret(None if s.e is None else self.ev(s.e, env))


# ---------------------------------------------------------------- main

def report(path, pos, kind, msg):
    sys.stderr.buffer.write(os.fsencode(path) + b':%d:%d: ' % pos + kind.encode() +
                            b': ' + msg.encode('latin-1') + b'\n')
    sys.stderr.buffer.flush()


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('usage: referee.py FILE.ditto\n')
        return 2
    path = sys.argv[1]
    try:
        with open(path, 'rb') as f:
            src = f.read()
    except OSError as e:
        sys.stderr.write('%s: %s\n' % (path, e.strerror))  # S14
        return 2
    try:
        items = Parser(Lexer(src).lex()).program()
        Resolver(items).run()
    except CompileError as e:
        report(path, e.pos, 'error', e.msg)
        return 2
    out = []
    status = [0]

    def go():
        try:
            Interp(items, out).run()
        except Fault as f:
            sys.stdout.buffer.write(b''.join(out))
            sys.stdout.buffer.flush()
            out.clear()
            report(path, f.pos, 'fault', f.msg)
            status[0] = 1
        except BaseException:  # a referee bug, never a Ditto outcome
            import traceback
            traceback.print_exc()
            status[0] = 70

    sys.setrecursionlimit(1_000_000)
    threading.stack_size(1 << 29)
    t = threading.Thread(target=go)
    t.start()
    t.join()
    sys.stdout.buffer.write(b''.join(out))
    sys.stdout.buffer.flush()
    return status[0]


if __name__ == '__main__':
    sys.exit(main())

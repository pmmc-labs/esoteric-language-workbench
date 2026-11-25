#!/usr/bin/env python3
"""A second printer: the fewest brackets perlop's table allows, so that perl has
to parse assignment, ++/--, ?: and the rest by precedence and associativity
alone. The model runs the tree; perl runs the text; a difference is a place
where perl's grammar is not the table (or this printer is wrong)."""
import model

LEVEL = {'**': 19, '*': 16, '/': 16, '%': 16, 'x': 16, '+': 15, '-': 15, '.': 15,
         '<': 12, '>': 12, '<=': 12, '>=': 12, 'lt': 12, 'gt': 12, 'le': 12, 'ge': 12,
         '==': 11, '!=': 11, '<=>': 11, 'eq': 11, 'ne': 11, 'cmp': 11,
         '&&': 8, '||': 7, '//': 7, 'and': 1, 'or': 0, 'xor': 0}


BARE = False      # `say E;` and not `say(E);`: the compiler has to refuse what perl reads another way


def level(e):
    k = e[0]
    if k in ('lit', 'var', 'paren', 'fn', 'fn1', 'my'): return 21
    if k in ('pre', 'post'): return 20
    if k in ('neg', 'not', 'uplus'): return 18
    if k in ('bin', 'log'): return LEVEL[e[1]]
    if k == 'tern': return 5
    if k == 'asg': return 4
    if k == 'lnot': return 2
    raise KeyError(k)


def at(e, need):
    """e, in brackets unless it binds at least as tightly as `need`."""
    s = show(e)
    return s if level(e) >= need else '(' + s + ')'


def glue(sign, s):
    """A unary sign before text: never let two signs make `++` or `--`."""
    return sign + (' ' if s[:1] == sign else '') + s


def show(e):
    k = e[0]
    if k == 'lit': return e[1]
    if k == 'var': return '$' + e[1]
    if k == 'my': return 'my $' + e[1]
    if k == 'paren': return '(' + show(e[1]) + ')'
    if k == 'pre': return e[1] + '$' + e[2]
    if k == 'post': return '$' + e[2] + e[1]
    if k == 'neg': return glue('-', at(e[1], 18))
    if k == 'uplus': return glue('+', at(e[1], 18))
    if k == 'not': return '!' + at(e[1], 18)
    if k == 'lnot': return 'not ' + at(e[1], 2)
    if k == 'fn1': return e[1] + '(' + show(e[2]) + ')'
    if k == 'fn': return e[1] + '(' + ', '.join(at(a, 4) for a in e[2]) + ')'
    if k == 'tern': return at(e[1], 7) + ' ? ' + at(e[2], 4) + ' : ' + at(e[3], 5)
    if k == 'asg': return show(e[2]) + ' ' + e[1] + ' ' + at(e[3], 4)
    op = e[1]
    lv = LEVEL[op]
    if op == '**': return at(e[2], 20) + ' ** ' + at(e[3], 18)          # right associative; a sign may start its right side
    if lv in (11, 12):                                                   # no chains; and `!A == B` is refused by the built compiler
        left = at(e[2], lv + 1)
        if e[2][0] == 'not': left = '(' + left + ')'
        return left + ' ' + op + ' ' + at(e[3], lv + 1)
    return at(e[2], lv) + ' ' + op + ' ' + at(e[3], lv + 1)              # left associative


def stmt(s, ind=''):
    k = s[0]
    if k == 'my': return ind + 'my $' + s[1] + (';' if s[2] is None else ' = ' + at(s[2], 4) + ';')
    if k == 'expr': return ind + show(s[1]) + ';'
    if k in ('say', 'print'): return ind + k + (' ' + show(s[1]) + ';' if BARE else '(' + show(s[1]) + ');')
    if k == 'block': return ind + '{\n' + block(s[1], ind + '    ') + ind + '}'
    if k == 'if':
        out = ''
        for n, (c, body) in enumerate(s[1]):
            out += (ind + 'if' if n == 0 else ' elsif') + ' (' + show(c) + ') {\n' + block(body, ind + '    ') + ind + '}'
        if s[2] is not None: out += ' else {\n' + block(s[2], ind + '    ') + ind + '}'
        return out
    if k == 'unless': return ind + 'unless (' + show(s[1]) + ') {\n' + block(s[2], ind + '    ') + ind + '}'
    if k == 'mod': return ind + stmt(s[1])[:-1] + ' ' + s[2] + ' ' + show(s[3]) + ';'
    raise KeyError(k)


def block(stmts, ind):
    return ''.join(stmt(s, ind) + '\n' for s in stmts)


def source(prog):
    return 'use v5.42;\n' + block(prog, '')


def bracketed_left_of_x(e):
    """Would `show` put brackets round the left operand of this `x`?"""
    return e[2][0] == 'paren' or level(e[2]) < 16


def list_refused(e):
    """T104 for this printer: `(...) x N` where say's list context reaches."""
    while e[0] in ('paren', 'uplus'): e = e[1]
    if e[0] == 'tern': return list_refused(e[2]) or list_refused(e[3])
    if e[0] == 'log': return list_refused(e[3])
    if e[0] == 'bin' and e[1] == 'x':
        left = e[2]
        while left[0] == 'uplus': left = left[1]
        return left[0] == 'paren' or level(e[2]) < 16
    return False

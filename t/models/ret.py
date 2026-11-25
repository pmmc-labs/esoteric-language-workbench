#!/usr/bin/env python3
"""t/1000 to t/1049: a sub gives back a list, slurpy parameters, join and
reverse (step 10a; D18, D79, D84, D87).

The definition, which is all this file knows of the language beyond
t/models/each.py (arrays, lists, foreach).

  return LIST;            every value, to a call where a list is wanted
  sub f($x, @rest) { }    a last parameter that takes every argument left
  join(SEP, LIST)         the values as strings, SEP between them
  reverse(LIST)           the values, last first

**A call where a list is wanted is every value its sub returned**: none,
one or many. A sub that ends in an expression gives that expression's
values the same way.

**D18's fault**: a `return`, or a last statement, that is *list-shaped*,
reached by a call that wants one value, faults before anything of it is
worked out: `f returned a list where one value is wanted`. List-shaped is
by how it is written: an array, a list of two or more or of one that is,
a range, a slice, `(LIST) x N`, `splice`, `reverse`, and `? :` or `|| &&
//` with such an arm, whichever arm would be taken. `return ();` is
`return;`. `return f();` hands on what its own call wanted. A call for
nothing faults for nothing; what a list-shaped `return` holds is worked
out there as a list.

**A slurpy parameter**, `@rest` or `@` alone, is last, and is filled when
its turn comes, after every default before it, with a copy of each
argument that is left (T191). A call may then have any number of
arguments from the number that are required.

**`join`**: SEP is one value, read when the list has been worked out
(T186; the compiler refuses a list that could change it, D87) and made a
string whether it is used or not (T190); then each value is made a
string, as `.` makes one, so an undef faults.

**`reverse`** is a list where a list is wanted. (Where one value is
wanted the compiler refuses it: D84.)

This model works a program out; it does not refuse one.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

1000 is lists returned, every shape to every place. 1001 is slurpy
parameters. 1002 is join and reverse. 1010 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/ret.py --program 1000 > t/1000-returned.pl
    python3 t/models/ret.py 1000 > t/1000-returned.expected
    python3 t/models/ret.py --program 1001 > t/1001-slurpy.pl
    python3 t/models/ret.py 1001 > t/1001-slurpy.expected
    python3 t/models/ret.py --program 1002 > t/1002-join-reverse.pl
    python3 t/models/ret.py 1002 > t/1002-join-reverse.expected
    python3 t/models/ret.py --program 1010 > t/1010-fault-list-returned-array.pl
    python3 t/models/ret.py 1010 > t/1010-fault-list-returned-array.expected
    python3 t/models/ret.py --program 1011 > t/1011-fault-list-returned-list.pl
    python3 t/models/ret.py 1011 > t/1011-fault-list-returned-list.expected
    python3 t/models/ret.py --program 1012 > t/1012-fault-list-returned-list-of-one-array.pl
    python3 t/models/ret.py 1012 > t/1012-fault-list-returned-list-of-one-array.expected
    python3 t/models/ret.py --program 1013 > t/1013-fault-list-returned-range.pl
    python3 t/models/ret.py 1013 > t/1013-fault-list-returned-range.expected
    python3 t/models/ret.py --program 1014 > t/1014-fault-list-returned-slice.pl
    python3 t/models/ret.py 1014 > t/1014-fault-list-returned-slice.expected
    python3 t/models/ret.py --program 1015 > t/1015-fault-list-returned-slice-of-a-list.pl
    python3 t/models/ret.py 1015 > t/1015-fault-list-returned-slice-of-a-list.expected
    python3 t/models/ret.py --program 1016 > t/1016-fault-list-returned-repeated.pl
    python3 t/models/ret.py 1016 > t/1016-fault-list-returned-repeated.expected
    python3 t/models/ret.py --program 1017 > t/1017-fault-list-returned-splice.pl
    python3 t/models/ret.py 1017 > t/1017-fault-list-returned-splice.expected
    python3 t/models/ret.py --program 1018 > t/1018-fault-list-returned-reverse.pl
    python3 t/models/ret.py 1018 > t/1018-fault-list-returned-reverse.expected
    python3 t/models/ret.py --program 1019 > t/1019-fault-list-returned-arm-taken.pl
    python3 t/models/ret.py 1019 > t/1019-fault-list-returned-arm-taken.expected
    python3 t/models/ret.py --program 1020 > t/1020-fault-list-returned-arm-not-taken.pl
    python3 t/models/ret.py 1020 > t/1020-fault-list-returned-arm-not-taken.expected
    python3 t/models/ret.py --program 1021 > t/1021-fault-list-returned-right-of-or.pl
    python3 t/models/ret.py 1021 > t/1021-fault-list-returned-right-of-or.expected
    python3 t/models/ret.py --program 1022 > t/1022-fault-list-returned-right-of-and.pl
    python3 t/models/ret.py 1022 > t/1022-fault-list-returned-right-of-and.expected
    python3 t/models/ret.py --program 1023 > t/1023-fault-list-returned-right-of-defined-or.pl
    python3 t/models/ret.py 1023 > t/1023-fault-list-returned-right-of-defined-or.expected
    python3 t/models/ret.py --program 1024 > t/1024-fault-list-returned-behind-a-plus.pl
    python3 t/models/ret.py 1024 > t/1024-fault-list-returned-behind-a-plus.expected
    python3 t/models/ret.py --program 1025 > t/1025-fault-list-as-last-statement-array.pl
    python3 t/models/ret.py 1025 > t/1025-fault-list-as-last-statement-array.expected
    python3 t/models/ret.py --program 1026 > t/1026-fault-list-as-last-statement-list.pl
    python3 t/models/ret.py 1026 > t/1026-fault-list-as-last-statement-list.expected
    python3 t/models/ret.py --program 1027 > t/1027-fault-list-as-last-statement-reverse.pl
    python3 t/models/ret.py 1027 > t/1027-fault-list-as-last-statement-reverse.expected
    python3 t/models/ret.py --program 1028 > t/1028-fault-list-as-last-statement-arm-not-taken.pl
    python3 t/models/ret.py 1028 > t/1028-fault-list-as-last-statement-arm-not-taken.expected
    python3 t/models/ret.py --program 1029 > t/1029-fault-one-value-wanted-operand.pl
    python3 t/models/ret.py 1029 > t/1029-fault-one-value-wanted-operand.expected
    python3 t/models/ret.py --program 1030 > t/1030-fault-one-value-wanted-test.pl
    python3 t/models/ret.py 1030 > t/1030-fault-one-value-wanted-test.expected
    python3 t/models/ret.py --program 1031 > t/1031-fault-one-value-wanted-index.pl
    python3 t/models/ret.py 1031 > t/1031-fault-one-value-wanted-index.expected
    python3 t/models/ret.py --program 1032 > t/1032-fault-one-value-wanted-builtin.pl
    python3 t/models/ret.py 1032 > t/1032-fault-one-value-wanted-builtin.expected
    python3 t/models/ret.py --program 1033 > t/1033-fault-one-value-wanted-separator.pl
    python3 t/models/ret.py 1033 > t/1033-fault-one-value-wanted-separator.expected
    python3 t/models/ret.py --program 1034 > t/1034-fault-one-value-wanted-left-of-or.pl
    python3 t/models/ret.py 1034 > t/1034-fault-one-value-wanted-left-of-or.expected
    python3 t/models/ret.py --program 1035 > t/1035-fault-one-value-wanted-assigned.pl
    python3 t/models/ret.py 1035 > t/1035-fault-one-value-wanted-assigned.expected
    python3 t/models/ret.py --program 1036 > t/1036-fault-one-value-wanted-element.pl
    python3 t/models/ret.py 1036 > t/1036-fault-one-value-wanted-element.expected
    python3 t/models/ret.py --program 1037 > t/1037-fault-one-value-wanted-range-end.pl
    python3 t/models/ret.py 1037 > t/1037-fault-one-value-wanted-range-end.expected
    python3 t/models/ret.py --program 1038 > t/1038-fault-one-value-wanted-repeat-count.pl
    python3 t/models/ret.py 1038 > t/1038-fault-one-value-wanted-repeat-count.expected
    python3 t/models/ret.py --program 1039 > t/1039-fault-context-handed-on.pl
    python3 t/models/ret.py 1039 > t/1039-fault-context-handed-on.expected
    python3 t/models/ret.py --program 1040 > t/1040-fault-context-handed-on-through-a-test.pl
    python3 t/models/ret.py 1040 > t/1040-fault-context-handed-on-through-a-test.expected
    python3 t/models/ret.py --program 1041 > t/1041-fault-before-the-list-is-worked-out.pl
    python3 t/models/ret.py 1041 > t/1041-fault-before-the-list-is-worked-out.expected
    python3 t/models/ret.py --program 1042 > t/1042-fault-too-few-before-a-slurpy.pl
    python3 t/models/ret.py 1042 > t/1042-fault-too-few-before-a-slurpy.expected
    python3 t/models/ret.py --program 1043 > t/1043-fault-too-few-through-an-empty-array.pl
    python3 t/models/ret.py 1043 > t/1043-fault-too-few-through-an-empty-array.expected
    python3 t/models/ret.py --program 1044 > t/1044-fault-join-of-an-undef.pl
    python3 t/models/ret.py 1044 > t/1044-fault-join-of-an-undef.expected
    python3 t/models/ret.py --program 1045 > t/1045-fault-join-by-an-undef.pl
    python3 t/models/ret.py 1045 > t/1045-fault-join-by-an-undef.expected
    python3 t/models/ret.py --program 1046 > t/1046-fault-join-by-an-undef-not-used.pl
    python3 t/models/ret.py 1046 > t/1046-fault-join-by-an-undef-not-used.expected
    python3 t/models/ret.py --program 1047 > t/1047-fault-join-of-a-number-with-two-spellings.pl
    python3 t/models/ret.py 1047 > t/1047-fault-join-of-a-number-with-two-spellings.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
import sub as subs
import list as lists
import each
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import ABSENT, LIST, SCALAR, VOID, Return, NO_VALUE, arity, ucall, sub, req, opt, ret, say_, named
from list import A, el, lst, mya, seta, sayl, setel, dump, Cases, Arr, items, element
from each import each as over

LISTED = 'returned a list where one value is wanted'
SLURPY = '@'

lists.LISTY = lists.LISTY + ('reverse',)

class Many(list):
    """What a call gives where a list is wanted."""

def shaped(e):
    """Whether an expression is list-shaped (D18), by how it is written."""
    if not isinstance(e, tuple):
        return False
    kind = e[0]
    if kind == 'list':
        return len(e[1]) > 1 or (len(e[1]) == 1 and shaped(e[1][0]))
    if kind in ('@', '..', 'slice', 'xl', 'splice', 'reverse'):
        return True
    if kind == 'lslice':
        return len(e[2]) != 1 or shaped(e[2][0])
    if kind == '?:':
        return shaped(e[2]) or shaped(e[3])
    if len(e) == 3 and (kind in var.LAZY or kind == '//'):
        return shaped(e[2])
    if kind == '+' and len(e) == 2:
        return shaped(e[1])
    return False

def slurp(name=None):
    return (name, SLURPY, None)

def jn(sep, *es):
    return ('join', sep, list(es))

def rev(*es):
    return ('reverse', list(es))

class Run(each.Run):
    def evl(self, e):
        if isinstance(e, tuple) and e[0] == 'reverse':
            return [v for item in e[1] for v in self.evl(item)][::-1]
        flat = []
        for v in super().evl(e):
            flat += list(v) if isinstance(v, Many) else [v]
        return flat

    def ev(self, e):
        if not isinstance(e, tuple) or e[0] not in ('ucall', 'join'):
            return super().ev(e)
        want, self.ctx = self.ctx, SCALAR
        if e[0] == 'join':
            sep = self.ev(e[1])
            values = [v for item in e[2] for v in self.evl(item)]
            s = logic.value(('.', get(sep), ''))
            out = ''
            for n, v in enumerate(values):
                piece = logic.value(('.', v, ''))
                out = piece if n == 0 else out + s + piece
            return out
        results = []
        for a in e[2]:
            if isinstance(a, tuple) and a[0] in lists.LISTY:
                results += self.evl(a)
                continue
            self.ctx = LIST
            r = self.ev(a)              # a variable is a place, read at its parameter's turn
            if isinstance(r, Many):
                results += r
            elif r is not ABSENT:
                results.append(r)
        value = self.call(e[1], results, want)
        self.ctx = SCALAR
        return value

    def call(self, name, args, want):
        self.names.append(name)
        try:
            return self.called(name, args, want)
        finally:
            self.names.pop()

    def called(self, name, args, want):
        _, _, params, body = sub_ = self.subs[name]
        slurpy = bool(params) and params[-1][1] == SLURPY
        least = sum(1 for _, op, _ in params if op is None)
        fault = arity(name, len(args), least, float('inf') if slurpy else len(params))
        if fault:
            raise Fault(fault)
        saved = self.scopes, self.frames, self.at
        self.scopes, self.frames = [self.scopes[0], {}], []
        self.wants.append(want)
        try:
            for k, (pname, op, default) in enumerate(params):
                if op == SLURPY:
                    rest = [get(a) for a in args[k:]]       # read now, at its turn
                    if pname is not None:
                        self.scopes[-1]['@' + pname] = Arr(rest)
                    break
                given = k < len(args)
                v = get(args[k]) if given else UNDEF
                if not given or (op == '//=' and v is UNDEF) or (op == '||=' and not logic.truth(v)):
                    self.at = id(sub_)
                    v = get(self.ev(default))
                if pname is not None:
                    self.scopes[-1][pname] = var.Place()
                    self.scopes[-1][pname].value = v
            try:
                value = self.body(name, body, want)
            except Return as r:
                value = r.value
        finally:
            self.wants.pop()
        self.scopes, self.frames, self.at = saved
        return value

    def given(self, name, e, want):
        """What a `return`'s expression, or a last statement's, is worth
        to a call that wanted `want`."""
        if isinstance(e, tuple) and e[0] == 'list' and not e[1]:
            return ABSENT if want == LIST else UNDEF
        if shaped(e):
            if want == SCALAR:
                raise Fault(f'{name} {LISTED}')
            return Many(self.evl(e))
        if want == LIST:
            return Many(self.evl(e))
        # (`return (7);`: brackets round one value.)
        while isinstance(e, tuple) and e[0] == 'list':
            e = e[1][0]
        self.ctx = want
        return get(self.ev(e))

    def body(self, name, body, want):
        if body and body[-1][0] == 'do':
            for s in body[:-1]:
                self.run(s)
            self.at = id(body[-1])
            return self.given(name, body[-1][1], want)
        return super().body(name, body, want)

    def run(self, s):
        kind = s[0]
        if kind == 'return' and s[1] is not None:
            self.at = id(s)
            raise Return(self.given(self.name(), s[1], self.wants[-1]))
        if kind == 'say':
            self.at = id(s)
            values = self.evl(s[1])
            self.out += ''.join(logic.printed(v) for v in values) + '\n'
            return
        super().run(s)

# ---- as source

def parameter(p):
    name, op, default = p
    if op == SLURPY:
        return '@' if name is None else '@' + name
    head = '$' if name is None else '$' + name
    return head if op is None else f'{head} {op} {text(default)}'

subs.parameter = parameter
var.MORE.update({
    'join': lambda e, top: f'join({", ".join(element(x) for x in [e[1]] + e[2])})',
    'reverse': lambda e, top: f'reverse({items(e[1])})',
})

source = each.source

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

# ---- the cases

shown = var.shown
P, Q, X, Y = (('$', n) for n in 'pqxy')

def returned_cases():
    c = Cases(0)
    # Every shape of list, after `return` and as a last statement, to an
    # array; and what a call of each is among other values.
    def shapes(f, g, G):
        a, e, r = g('a'), g('e'), g('r')
        s = [mya(a, 4, 5, 6), ('mya', e, None), ('mya', r, None),
             sub(f('one'), [], ret(7)), sub(f('none'), [], ret())]
        made = [A(a), lst(1, 2, 3), lst(), lst(A(a), 9), ('..', 2, 5), ('slice', a, [2, 0]), ('lslice', [A(a), 8], [3, 0]), ('xl', ['x', 'y'], 2),
                rev(A(a)), rev(1, A(a), 2), lst(A(e), A(e)), ('?:', 1, A(a), 0), ('?:', 0, A(a), 0), ('||', 0, A(a)), ('||', 3, A(a)), ('//', UNDEF, lst(1, 2)),
                ('&&', 1, lst(8, 9)), ('+', A(a)), el(a, 1), UNDEF, lst(UNDEF, UNDEF), ucall(f('one')), ucall(f('none')), lst(ucall(f('none')), ucall(f('one')), ucall(f('none'))),
                ('+', el(a, 0), 1), lst(lst(1, lst(2)), 3), A(e), ('splice', a, [1, 1]), jn('-', A(a))]
        for n, e_ in enumerate(made):
            by_return, by_last = f(f'r{n}_'), f(f'l{n}_')
            s += [sub(by_return, [], ret(e_)), sub(by_last, [], do(e_)),
                  seta(a, 4, 5, 6), seta(r, ucall(by_return)), dump(r), seta(a, 4, 5, 6), seta(r, 0, ucall(by_last), 0), dump(r)]
        return s
    c.case(shapes)
    # Every place a list is wanted.
    def places(f, g, G):
        a, r = g('a'), g('r')
        three = sub(f('three'), [], ret(lst(1, 2, 3)))
        pair = sub(f('pair'), [req('p')], ret(lst(P, ('*', P, 2))))
        none = sub(f('none'), [], ret(lst()))
        count = sub(f('count'), [opt('p', '-'), opt('q', '-'), opt('r', '-'), opt('s', '-')],
                    ret(join(logic.shown(P), logic.shown(Q), logic.shown(('$', 'r')), logic.shown(('$', 's')))))
        T, PR, NO = ucall(f('three')), ucall(f('pair'), 5), ucall(f('none'))
        return [three, pair, none, count, mya(a, 0), ('mya', r, None),
                sayl(T), sayl('[', T, '|', PR, '|', NO, ']'), say_(T), say_(NO),
                ('lassign', True, [('$', g('x')), ('$', g('y'))], [T]), say_(join(G('x'), G('y'))),
                ('lassign', False, [('$', g('y')), None, ('$', g('x')), A(r)], [PR, T, NO, PR]), say_(join(G('x'), G('y'))), dump(r),
                ('lassign', False, [G('x'), G('y')], [NO]), shown(G('x')), shown(G('y')),
                do(('push', a, [T, PR])), dump(a), do(('unshift', a, [NO])), dump(a), do(('splice', a, [1, 2, PR])), dump(a),
                over('v', [T, NO, PR], sayl('v', ('$', 'v'))),
                over('v', [NO], say_('never')),
                say_(ucall(f('count'), T)), say_(ucall(f('count'), PR, PR)), say_(ucall(f('count'), NO)), say_(ucall(f('count'), 0, NO, T)),
                say_(('lslice', [T], [1])), sayl(('lslice', [T, PR], [4, 0])), sayl(('xl', [PR], 2)), sayl(rev(T, PR)),
                seta(r, ('slice', a, [PR])), dump(r), seta(r, ('..', 1, ('lslice', [PR], [0]))), dump(r),
                seta(r, ('?:', 1, T, PR)), dump(r), seta(r, ('||', 0, PR)), dump(r),
                # For nothing: no fault, whatever it returns.
                do(T), do(NO), do(PR)]
    c.case(places)
    # Through calls: `return f();` hands the context on, a list of calls,
    # and a sub that calls itself to build a list.
    def through(f, g, G):
        r = g('r')
        return [('mya', r, None),
                sub(f('two'), [], ret(lst('a', 'b'))),
                sub(f('pass'), [], ret(ucall(f('two')))),
                sub(f('last'), [], do(ucall(f('two')))),
                sub(f('both'), [], ret(lst(ucall(f('pass')), ucall(f('last'))))),
                sub(f('pick'), [req('p')], ret(('?:', P, ucall(f('two')), 'z'))),
                sub(f('upto'), [req('p')], ('mod', ret(lst()), 'if', ('==', P, 0)), ret(lst(ucall(f('upto'), ('-', P, 1)), P))),
                sub(f('walk'), [req('p')], mya('mine', ucall(f('upto'), P)), do(('push', 'mine', [0])), ret(A('mine'))),
                sub(f('early'), [req('p')], over('v', [ucall(f('upto'), 5)], ('mod', ret(lst(('$', 'v'), ('$', 'v'))), 'if', ('==', ('$', 'v'), P))), ret(lst())),
                seta(r, ucall(f('pass'))), dump(r), seta(r, ucall(f('last'))), dump(r), seta(r, ucall(f('both'))), dump(r),
                seta(r, ucall(f('pick'), 1)), dump(r), seta(r, ucall(f('pick'), 0)), dump(r),
                # Where one value is wanted, a sub that hands the context
                # on to one that returns one value.
                say_(join('<', ucall(f('pick'), 0), '>')),
                seta(r, ucall(f('upto'), 6)), dump(r), seta(r, ucall(f('upto'), 0)), dump(r), seta(r, ucall(f('walk'), 3), ucall(f('walk'), 1)), dump(r),
                seta(r, ucall(f('early'), 3)), dump(r), seta(r, ucall(f('early'), 9)), dump(r),
                seta(r, rev(ucall(f('upto'), 4))), dump(r)]
    c.case(through)
    # A returned array is a copy: the caller's and the sub's are two.
    def copies(f, g, G):
        a, r = g('a'), g('r')
        return [mya(a, 1, 2, 3), ('mya', r, None),
                sub(f('all'), [], ret(A(a))),
                sub(f('grown'), [], do(('push', a, [9])), ret(A(a))),
                seta(r, ucall(f('all'))), do(setel(r, 0, 'r')), do(setel(a, 1, 'a')), dump(r), dump(a),
                seta(a, ucall(f('grown')), ucall(f('grown'))), dump(a),
                seta(a, rev(ucall(f('all')))), dump(a),
                over('v', [ucall(f('all'))], do(('push', a, [('$', 'v')]))), dump(a)]
    c.case(copies)
    # One value, where one is wanted, from what is not list-shaped.
    def ones(f, g, G):
        a = g('a')
        return [mya(a, 4, 5, 6),
                sub(f('seven'), [], ret(lst(7))),
                sub(f('empty'), [], ret(lst())),
                sub(f('elem'), [], ret(el(a, 1))),
                sub(f('of'), [], ret(('lslice', [A(a)], [2]))),
                sub(f('count'), [], ret(('scalar', a))),
                sub(f('or'), [req('p')], ret(('||', A(a), P))),
                sub(f('joined'), [], ret(jn(',', A(a)))),
                sub(f('pushed'), [], do(('push', a, [1]))),
                ('my', g('x'), ucall(f('seven'))), say_(G('x')), shown(ucall(f('empty'))), say_(('+', ucall(f('elem')), ucall(f('of')))),
                say_(join(ucall(f('count')), ucall(f('or'), 0), ucall(f('joined')))),
                ('if', [(ucall(f('empty')), [say_('never')]), (ucall(f('seven')), [say_('seven')])], None),
                say_(el(a, ('-', ucall(f('count')), 1))), say_(ucall(f('pushed')))]
    c.case(ones)
    return c.out

def slurpy_cases():
    c = Cases(100)
    def forms(f, g, G):
        a, e = g('a'), g('e')
        shape = lambda *ps: ret(jn('|', *ps, ('scalar', 'rest'), jn(',', A('rest'))))
        return [mya(a, 5, 6), ('mya', e, None),
                sub(f('all'), [slurp('rest')], shape()),
                sub(f('one'), [req('p'), slurp('rest')], shape(P)),
                sub(f('def'), [req('p'), opt('q', 'dq'), slurp('rest')], shape(P, Q)),
                sub(f('dor'), [opt('p', 'dp', '//='), slurp('rest')], shape(P)),
                sub(f('bare'), [req('p'), slurp()], ret(P)),
                sub(f('skip'), [(None, None, None), slurp('rest')], shape()),
                sub(f('only'), [slurp()], ret('only')),
                say_(ucall(f('all'))), say_(ucall(f('all'), 1)), say_(ucall(f('all'), 1, 2, 3)), say_(ucall(f('all'), A(a), A(a))), say_(ucall(f('all'), A(e))),
                say_(ucall(f('all'), lst(), 0, FALSE, '')), say_(ucall(f('all'), ('..', 1, 5))), say_(ucall(f('all'), rev(A(a)))),
                say_(ucall(f('one'), 1)), say_(ucall(f('one'), 1, 2)), say_(ucall(f('one'), A(a))), say_(ucall(f('one'), A(a), A(a))),
                say_(ucall(f('def'), 1)), say_(ucall(f('def'), 1, 2)), say_(ucall(f('def'), 1, 2, 3, 4)), say_(ucall(f('def'), A(a), A(a))),
                say_(ucall(f('dor'))), say_(ucall(f('dor'), UNDEF, 8, 9)), say_(ucall(f('dor'), 0, 8)),
                say_(ucall(f('bare'), 1)), say_(ucall(f('bare'), 1, 2, 3)), say_(ucall(f('skip'), 1)), say_(ucall(f('skip'), 1, 2)),
                say_(ucall(f('only'))), say_(ucall(f('only'), A(a), 1))]
    c.case(forms)
    # Copies: the sub's array is its own, new at each call, and changing
    # it changes nothing of the caller's. Handed on, and back.
    def copies(f, g, G):
        a, r = g('a'), g('r')
        return [mya(a, 1, 2, 3), ('mya', r, None),
                sub(f('change'), [slurp('v')], do(setel('v', 0, 'changed')), do(('push', 'v', ['more'])), ret(A('v'))),
                sub(f('same'), [slurp('v')], ret(A('v'))),
                sub(f('on'), [req('p'), slurp('v')], ret(ucall(f('same'), A('v'), P))),
                sub(f('twice'), [slurp('v')], ret(lst(A('v'), A('v')))),
                sub(f('sum'), [slurp('v')], ('my', 't', 0), over('n', [A('v')], do(set_('t', ('$', 'n'), '+='))), ret(('$', 't'))),
                sub(f('deep'), [req('p'), slurp('v')], ('mod', ret(A('v')), 'if', ('==', P, 0)), ret(ucall(f('deep'), ('-', P, 1), A('v'), P))),
                seta(r, ucall(f('change'), A(a))), dump(r), dump(a),
                seta(r, ucall(f('on'), A(a))), dump(r), seta(r, ucall(f('twice'), ucall(f('twice'), 7))), dump(r),
                say_(ucall(f('sum'), A(a), 10, ucall(f('twice'), 100))), say_(ucall(f('sum'))),
                seta(r, ucall(f('deep'), 4, 'x')), dump(r)]
    c.case(copies)
    # Filled at its turn (T191): after a default has run, and a variable
    # among the arguments read then.
    def late(f, g, G):
        v = g('v')
        return [('my', v, 5),
                sub(f('bump'), [], do(set_(v, 9)), ret(5)),
                sub(f('rest'), [req('p'), slurp('rest')], ret(jn('|', P, A('rest')))),
                sub(f('dflt'), [req('p'), opt('q', ucall(f('bump')), '//='), slurp('rest')], ret(jn('|', P, Q, A('rest')))),
                say_(ucall(f('rest'), 1, G('v'), ucall(f('bump')))), do(set_(v, 5)),
                say_(ucall(f('dflt'), 1, UNDEF, G('v'))), do(set_(v, 5)),
                say_(ucall(f('dflt'), 1, 2, G('v')))]
    c.case(late)
    return c.out

def join_cases():
    c = Cases(200)
    def joins(f, g, G):
        a, e, r = g('a'), g('e'), g('r')
        s = [mya(a, 'x', 'y', 'z'), ('mya', e, None), ('mya', r, None), sub(f('two'), [], ret(lst(1, 2))), sub(f('none'), [], ret())]
        for sep in (',', '', ' - ', 0, 1.5, TRUE, FALSE, A(a), el(a, 0), ('lslice', [ucall(f('two'))], [1])):
            for its in ([A(a)], [1, 2, 3], [A(e)], ['only'], [A(a), A(a)], [0.5, TRUE, FALSE, '', -7, 3.0], [ucall(f('two')), ucall(f('none')), ucall(f('two'))]):
                s.append(say_(join('<', jn(sep, *its), '>')))
        s += [say_(jn(',')), say_(jn(',', lst())), say_(jn(jn('+', 1, 2), 'a', 'b')), say_(jn(',', jn('-', A(a)), jn('', A(a)))),
              say_(('call', 'length', [jn(',', A(a))])), say_(('x', jn('', A(a)), 2)), say_(('.', jn(',', ('..', 1, 5)), '!')),
              say_(jn(',', ('slice', a, [2, 0]), ('xl', ['r'], 3))), say_(jn('/', ('last', a), ('scalar', a), el(a, 1)))]
        return s
    c.case(joins)
    def reverses(f, g, G):
        a, e, r = g('a'), g('e'), g('r')
        return [mya(a, 1, 2, 3), ('mya', e, None), ('mya', r, None), sub(f('two'), [], ret(lst('a', 'b'))),
                seta(r, rev(A(a))), dump(r), seta(r, rev(A(e))), dump(r), seta(r, rev(7)), dump(r), seta(r, rev(A(a), 0, A(a))), dump(r),
                seta(r, rev(rev(A(a)))), dump(r), seta(r, rev(('..', 1, 5))), dump(r), seta(r, rev(UNDEF, 1, UNDEF)), dump(r),
                seta(r, rev(ucall(f('two')), ucall(f('two')))), dump(r), seta(r, 0, rev(A(a)), 0), dump(r),
                sayl(rev(A(a))), sayl(rev('ab', 'cd')), say_(jn(',', rev(A(a)))),
                over('v', [rev(A(a))], sayl('v', ('$', 'v'))),
                over('v', [rev(('..', 1, 3))], do(('push', a, [('$', 'v')]))), dump(a),
                ('lassign', True, [('$', g('x')), ('$', g('y'))], [rev(1, 2, 3)]), say_(join(G('x'), G('y'))),
                seta(a, rev(A(a))), dump(a), do(('push', r, [rev(A(a))])), dump(r),
                sayl(('lslice', [rev(A(a))], [0, -1])), sayl(('xl', [rev(1, 2)], 2))]
    c.case(reverses)
    return c.out

SAME = {'1000': ('returned', returned_cases), '1001': ('slurpy', slurpy_cases), '1002': ('join-reverse', join_cases)}

def faults():
    out = {}
    n = [1010]
    def fault(name, subs_, near, far):
        out[str(n[0])] = ('fault-' + name, subs_, near, far)
        n[0] += 1
    a3 = mya('a', 4, 5, 6)
    # Each list shape, after `return`, to a call that wants one value:
    # the same call for a list first, which is fine.
    shapes = [('array', A('a')), ('list', lst(1, 2)), ('list-of-one-array', lst(A('a'))), ('range', ('..', 1, 2)), ('slice', ('slice', 'a', [0, 1])),
              ('slice-of-a-list', ('lslice', [A('a')], [0, 1])), ('repeated', ('xl', [1], 2)), ('splice', ('splice', 'a', [0, 1])), ('reverse', rev(A('a'))),
              ('arm-taken', ('?:', 1, A('a'), 0)), ('arm-not-taken', ('?:', 0, A('a'), 0)), ('right-of-or', ('||', 1, A('a'))), ('right-of-and', ('&&', 0, lst(1, 2))),
              ('right-of-defined-or', ('//', 1, A('a'))), ('behind-a-plus', ('+', A('a')))]
    for name, e in shapes:
        fault('list-returned-' + name, [a3, sub('f', [], ret(e))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    # As a last statement, a few; and for one value in each kind of place.
    for name, e in (('array', A('a')), ('list', lst(1, 2)), ('reverse', rev(1, 2)), ('arm-not-taken', ('?:', 0, lst(1, 2), 0))):
        fault('list-as-last-statement-' + name, [a3, sub('f', [], do(e))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    two = [a3, sub('f', [], ret(lst(1, 2)))]
    for name, far in (('operand', say_(('+', ucall('f'), 1))), ('test', ('if', [(ucall('f'), [say_('never')])], None)), ('index', say_(el('a', ucall('f')))),
                      ('builtin', say_(('call', 'length', [ucall('f')]))), ('separator', say_(jn(ucall('f'), 1, 2))), ('left-of-or', sayl(('||', ucall('f'), 1))),
                      ('assigned', block(('my', 'x', 0), do(set_('x', ucall('f'))))), ('element', do(setel('a', 0, ucall('f')))),
                      ('range-end', sayl(('..', 1, ucall('f')))), ('repeat-count', sayl(('xl', [1], ucall('f'))))):
        fault('one-value-wanted-' + name, two, sayl(ucall('f')), far)
    # Handed on: the call that wanted one value is two calls up.
    fault('context-handed-on', two + [sub('g', [], ret(ucall('f'))), sub('h', [], do(ucall('g')))], sayl(ucall('h')), ('my', 'x', ucall('h')))
    fault('context-handed-on-through-a-test', two + [sub('g', [req('p')], ret(('?:', ('$', 'p'), ucall('f'), 0)))], block(sayl(ucall('g', 1)), ('my', 'y', ucall('g', 0))), ('my', 'x', ucall('g', 1)))
    # Nothing of the list is worked out before the fault.
    fault('before-the-list-is-worked-out', [sub('loud', [], say_('worked out'), ret(1)), sub('f', [], ret(lst(ucall('loud'), 2)))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    # A slurpy parameter does not make up for one that is required.
    fault('too-few-before-a-slurpy', [sub('f', [req('p'), req('q'), slurp('rest')], ret(1))], say_(ucall('f', 1, 2)), say_(ucall('f', 1)))
    fault('too-few-through-an-empty-array', [('mya', 'e', None), sub('f', [req('p'), slurp('rest')], ret(1))], say_(ucall('f', A('e'), 1)), say_(ucall('f', A('e'))))
    # join: an undef among the values, an undef for the separator, used
    # or not (T190).
    u = ('my', 'u', None)
    fault('join-of-an-undef', [], block(u, say_(jn(',', 1, '', 2))), block(u, say_(jn(',', 1, ('$', 'u'), 2))))
    fault('join-by-an-undef', [], block(u, say_(jn('', 1, 2))), block(u, say_(jn(('$', 'u'), 1, 2))))
    fault('join-by-an-undef-not-used', [], block(u, say_(jn('', 1))), block(u, say_(jn(('$', 'u'), 1))))
    fault('join-of-a-number-with-two-spellings', [], say_(jn(',', 1e14, 1)), say_(jn(',', 1e15, 1)))
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/ret.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/ret.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    sys.setrecursionlimit(20000)
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/ret.py']
    if number in SAME:
        cases = SAME[number][1]()
        for c in cases:
            assert output(c)[1] is None, (number, output(c)[1], output(c)[0][-200:])
        statements = [s for c in cases for s in c]
        out.write((program(statements, model) if want_program else output(statements)[0]).encode())
        return
    name, the_subs, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    statements = the_subs + [('say', 1), near, far, ('say', 2)]
    if want_program:
        out.write(program(statements, header).encode())
        return
    printed, fault, at = output(statements)
    assert fault is not None and output(the_subs + [('say', 1), near])[1] is None, (number, printed, fault)
    found = {}
    each.lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

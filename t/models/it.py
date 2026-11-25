#!/usr/bin/env python3
"""t/1100 to t/1149: `$_`, and what binds it (step 10b; D17, D84, D85, D87).

The definition, which is all this file knows of the language beyond
t/models/ret.py (lists returned, join, reverse).

  for (LIST) { ... }          the block once for each value, `$_` that value
  STATEMENT for LIST;         the same, for one statement
  map { ...; EXPR } LIST      the values of EXPR, for each value of LIST
  grep { ...; EXPR } LIST     the values of LIST for which EXPR is true

Each is t/models/each.py's `foreach` under another spelling. LIST is
worked out once, where the binder stands (so a `$_` in it is the one
outside), and copied; `$_` is a value, new each time round, read-only;
and **every array named in LIST is frozen while the binder runs**, a
store to it or a change of its size a fault, from the block or from a sub
the block calls. An element or a slice past either end of its array, in
LIST, is a fault (T177: perl would make it), as in a `foreach`.

A block is statements and then an expression. `map`'s is worked out where
a list is wanted, and gives any number of values; `grep`'s is one value,
and tested for truth. A `my` in a block is new each time round.

**Where one value is wanted, `map` and `grep` are how many values they
give** (D84). After `return`, each is list-shaped (D18).

A fault in a block names the line its statement stands on.

This model works a program out; it does not refuse one: that `$_` is
read-only, that a block has no `return`, D76 and D77 are the compiler's.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

1100 is the two `for`s. 1101 is map. 1102 is grep. 1110 on each fault
once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/it.py --program 1100 > t/1100-for-it.pl
    python3 t/models/it.py 1100 > t/1100-for-it.expected
    python3 t/models/it.py --program 1101 > t/1101-map.pl
    python3 t/models/it.py 1101 > t/1101-map.expected
    python3 t/models/it.py --program 1102 > t/1102-grep.pl
    python3 t/models/it.py 1102 > t/1102-grep.expected
    python3 t/models/it.py --program 1110 > t/1110-fault-frozen-for-store.pl
    python3 t/models/it.py 1110 > t/1110-fault-frozen-for-store.expected
    python3 t/models/it.py --program 1111 > t/1111-fault-frozen-for-push.pl
    python3 t/models/it.py 1111 > t/1111-fault-frozen-for-push.expected
    python3 t/models/it.py --program 1112 > t/1112-fault-frozen-for-shift.pl
    python3 t/models/it.py 1112 > t/1112-fault-frozen-for-shift.expected
    python3 t/models/it.py --program 1113 > t/1113-fault-frozen-for-assign.pl
    python3 t/models/it.py 1113 > t/1113-fault-frozen-for-assign.expected
    python3 t/models/it.py --program 1114 > t/1114-fault-frozen-for-splice.pl
    python3 t/models/it.py 1114 > t/1114-fault-frozen-for-splice.expected
    python3 t/models/it.py --program 1115 > t/1115-fault-frozen-for-from-a-sub.pl
    python3 t/models/it.py 1115 > t/1115-fault-frozen-for-from-a-sub.expected
    python3 t/models/it.py --program 1116 > t/1116-fault-frozen-for-modifier-store.pl
    python3 t/models/it.py 1116 > t/1116-fault-frozen-for-modifier-store.expected
    python3 t/models/it.py --program 1117 > t/1117-fault-frozen-for-modifier-shift.pl
    python3 t/models/it.py 1117 > t/1117-fault-frozen-for-modifier-shift.expected
    python3 t/models/it.py --program 1118 > t/1118-fault-frozen-for-modifier-splice.pl
    python3 t/models/it.py 1118 > t/1118-fault-frozen-for-modifier-splice.expected
    python3 t/models/it.py --program 1119 > t/1119-fault-frozen-map-store.pl
    python3 t/models/it.py 1119 > t/1119-fault-frozen-map-store.expected
    python3 t/models/it.py --program 1120 > t/1120-fault-frozen-map-push.pl
    python3 t/models/it.py 1120 > t/1120-fault-frozen-map-push.expected
    python3 t/models/it.py --program 1121 > t/1121-fault-frozen-map-shift.pl
    python3 t/models/it.py 1121 > t/1121-fault-frozen-map-shift.expected
    python3 t/models/it.py --program 1122 > t/1122-fault-frozen-map-assign.pl
    python3 t/models/it.py 1122 > t/1122-fault-frozen-map-assign.expected
    python3 t/models/it.py --program 1123 > t/1123-fault-frozen-map-splice.pl
    python3 t/models/it.py 1123 > t/1123-fault-frozen-map-splice.expected
    python3 t/models/it.py --program 1124 > t/1124-fault-frozen-map-from-a-sub.pl
    python3 t/models/it.py 1124 > t/1124-fault-frozen-map-from-a-sub.expected
    python3 t/models/it.py --program 1125 > t/1125-fault-frozen-grep-store.pl
    python3 t/models/it.py 1125 > t/1125-fault-frozen-grep-store.expected
    python3 t/models/it.py --program 1126 > t/1126-fault-frozen-grep-push.pl
    python3 t/models/it.py 1126 > t/1126-fault-frozen-grep-push.expected
    python3 t/models/it.py --program 1127 > t/1127-fault-frozen-grep-splice.pl
    python3 t/models/it.py 1127 > t/1127-fault-frozen-grep-splice.expected
    python3 t/models/it.py --program 1128 > t/1128-fault-frozen-grep-from-a-sub.pl
    python3 t/models/it.py 1128 > t/1128-fault-frozen-grep-from-a-sub.expected
    python3 t/models/it.py --program 1129 > t/1129-fault-frozen-for-modifier-from-a-sub.pl
    python3 t/models/it.py 1129 > t/1129-fault-frozen-for-modifier-from-a-sub.expected
    python3 t/models/it.py --program 1130 > t/1130-fault-given-back-after-a-map.pl
    python3 t/models/it.py 1130 > t/1130-fault-given-back-after-a-map.expected
    python3 t/models/it.py --program 1131 > t/1131-fault-given-back-after-a-grep.pl
    python3 t/models/it.py 1131 > t/1131-fault-given-back-after-a-grep.expected
    python3 t/models/it.py --program 1132 > t/1132-fault-given-back-after-a-for-modifier.pl
    python3 t/models/it.py 1132 > t/1132-fault-given-back-after-a-for-modifier.expected
    python3 t/models/it.py --program 1133 > t/1133-fault-frozen-after-the-inner-map.pl
    python3 t/models/it.py 1133 > t/1133-fault-frozen-after-the-inner-map.expected
    python3 t/models/it.py --program 1134 > t/1134-fault-map-names-by-second-of-two.pl
    python3 t/models/it.py 1134 > t/1134-fault-map-names-by-second-of-two.expected
    python3 t/models/it.py --program 1135 > t/1135-fault-map-names-by-slice.pl
    python3 t/models/it.py 1135 > t/1135-fault-map-names-by-slice.expected
    python3 t/models/it.py --program 1136 > t/1136-fault-map-names-by-element.pl
    python3 t/models/it.py 1136 > t/1136-fault-map-names-by-element.expected
    python3 t/models/it.py --program 1137 > t/1137-fault-map-names-by-reverse.pl
    python3 t/models/it.py 1137 > t/1137-fault-map-names-by-reverse.expected
    python3 t/models/it.py --program 1138 > t/1138-fault-map-names-by-a-grep-of-it.pl
    python3 t/models/it.py 1138 > t/1138-fault-map-names-by-a-grep-of-it.expected
    python3 t/models/it.py --program 1139 > t/1139-fault-map-names-by-a-map-of-it.pl
    python3 t/models/it.py 1139 > t/1139-fault-map-names-by-a-map-of-it.expected
    python3 t/models/it.py --program 1140 > t/1140-fault-map-names-by-last-index.pl
    python3 t/models/it.py 1140 > t/1140-fault-map-names-by-last-index.expected
    python3 t/models/it.py --program 1141 > t/1141-fault-element-past-the-end-in-a-for.pl
    python3 t/models/it.py 1141 > t/1141-fault-element-past-the-end-in-a-for.expected
    python3 t/models/it.py --program 1142 > t/1142-fault-slice-past-the-end-in-a-for.pl
    python3 t/models/it.py 1142 > t/1142-fault-slice-past-the-end-in-a-for.expected
    python3 t/models/it.py --program 1143 > t/1143-fault-element-past-the-end-in-a-for-modifier.pl
    python3 t/models/it.py 1143 > t/1143-fault-element-past-the-end-in-a-for-modifier.expected
    python3 t/models/it.py --program 1144 > t/1144-fault-slice-past-the-end-in-a-for-modifier.pl
    python3 t/models/it.py 1144 > t/1144-fault-slice-past-the-end-in-a-for-modifier.expected
    python3 t/models/it.py --program 1145 > t/1145-fault-element-past-the-end-in-a-map.pl
    python3 t/models/it.py 1145 > t/1145-fault-element-past-the-end-in-a-map.expected
    python3 t/models/it.py --program 1146 > t/1146-fault-slice-past-the-end-in-a-map.pl
    python3 t/models/it.py 1146 > t/1146-fault-slice-past-the-end-in-a-map.expected
    python3 t/models/it.py --program 1147 > t/1147-fault-element-past-the-end-in-a-grep.pl
    python3 t/models/it.py 1147 > t/1147-fault-element-past-the-end-in-a-grep.expected
    python3 t/models/it.py --program 1148 > t/1148-fault-slice-past-the-end-in-a-grep.pl
    python3 t/models/it.py 1148 > t/1148-fault-slice-past-the-end-in-a-grep.expected
    python3 t/models/it.py --program 1149 > t/1149-fault-map-returned-for-one-value.pl
    python3 t/models/it.py 1149 > t/1149-fault-map-returned-for-one-value.expected
    python3 t/models/it.py --program 1150 > t/1150-fault-grep-returned-for-one-value.pl
    python3 t/models/it.py 1150 > t/1150-fault-grep-returned-for-one-value.expected
    python3 t/models/it.py --program 1151 > t/1151-fault-map-as-a-last-statement-for-one-value.pl
    python3 t/models/it.py 1151 > t/1151-fault-map-as-a-last-statement-for-one-value.expected
    python3 t/models/it.py --program 1152 > t/1152-fault-in-a-map-block.pl
    python3 t/models/it.py 1152 > t/1152-fault-in-a-map-block.expected
    python3 t/models/it.py --program 1153 > t/1153-fault-in-a-grep-test.pl
    python3 t/models/it.py 1153 > t/1153-fault-in-a-grep-test.expected
    python3 t/models/it.py --program 1154 > t/1154-fault-under-a-for-modifier.pl
    python3 t/models/it.py 1154 > t/1154-fault-under-a-for-modifier.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
import sub as subs
import list as lists
import each
import ret
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import ABSENT, LIST, SCALAR, VOID, ucall, sub, req, opt, say_, named
from sub import ret as returns
from list import A, el, lst, mya, seta, sayl, setel, dump, Cases, Arr, items, element
from each import each as over
from ret import jn, rev, slurp

IT = ('$', '_')

lists.LISTY = lists.LISTY + ('map', 'grep')
_shaped = ret.shaped
ret.shaped = lambda e: (isinstance(e, tuple) and e[0] in ('map', 'grep')) or _shaped(e)

def forit(its, *body, label=None):
    return ('foreach', label, '_', list(its), list(body))

def formod(statement, *its):
    return ('formod', statement, list(its))

def mp(its, *body):
    """map: the statements of its block, the last an expression."""
    return ('map', list(body[:-1]), body[-1], list(its))

def gr(its, *body):
    return ('grep', list(body[:-1]), body[-1], list(its))

class Run(ret.Run):
    def binder(self, e):
        kind, body, last, its = e
        for item in its:
            self.strict(item)
        values = [v for item in its for v in self.evl(item)]
        # The arrays its list names: not those its block does.
        frozen = [self.arr(n) for n in dict.fromkeys(each.names(('list', its), []))]
        for a in frozen:
            a.frozen += 1
        at, out = self.at, []
        try:
            for v in values:
                self.scopes.append({'_': var.Place()})
                self.scopes[-1]['_'].value = v
                try:
                    for s in body:
                        self.run(s)
                    self.at = at
                    if kind == 'map':
                        out += self.evl(last)
                    elif logic.truth(get(self.ev(last))):
                        out.append(v)
                finally:
                    self.scopes.pop()
        except Fault:
            # The block is on its statement's line.
            self.at = at
            raise
        finally:
            for a in frozen:
                a.frozen -= 1
        return out

    def evl(self, e):
        if isinstance(e, tuple) and e[0] in ('map', 'grep'):
            return self.binder(e)
        return super().evl(e)

    def ev(self, e):
        if isinstance(e, tuple) and e[0] in ('map', 'grep'):
            self.ctx = SCALAR
            return len(self.binder(e))
        return super().ev(e)

    def run(self, s):
        if s[0] == 'formod':
            whole = ('foreach', None, '_', s[2], [s[1]])
            self.alias[id(whole)] = id(s)
            self.kept = getattr(self, 'kept', []) + [whole]
            return super().run(whole)
        if s[0] == 'do' and isinstance(s[1], tuple) and s[1][0] in ('map', 'grep'):
            # As a statement: for what its block does.
            self.at = id(s)
            self.binder(s[1])
            return
        super().run(s)

# ---- as source

def inline(statements):
    return ''.join(line.strip() + ' ' for s in statements for line in source(s))

def binder_text(e, top):
    return f'({e[0]} {{ {inline(e[1])}{text(e[2])} }} ({items(e[3])}))'

var.MORE.update({'map': binder_text, 'grep': binder_text})

_source = each.source

def source(s, depth=0):
    pad = '    ' * depth
    if s[0] == 'foreach' and s[2] == '_':
        label = '' if s[1] is None else s[1] + ': '
        return [f'{pad}{label}for ({items(s[3])}) {{'] + [line for t in s[4] for line in source(t, depth + 1)] + [pad + '}']
    if s[0] == 'formod':
        return [source(s[1], depth)[0][:-1] + f' for ({items(s[2])});']
    return _source(s, depth)

each.source = source

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

def lines_(statements, line, found):
    """each.py's `lines_`, with a statement under a `for`."""
    for s in statements:
        found[id(s)] = line
        kind = s[0]
        if kind in ('block', 'unless', 'while', 'until', 'for', 'sub', 'foreach'):
            line = lines_(s[-1], line + 1, found) + 1
        elif kind == 'if':
            for n, (test, body) in enumerate(s[1]):
                found[(id(s), n)] = line
                line = lines_(body, line + 1, found)
            if s[2] is not None:
                line = lines_(s[2], line + 1, found)
            line += 1
        else:
            if kind in ('mod', 'formod'):
                found[id(s[1])] = line
            line += 1
    return line

# ---- the cases

shown = var.shown
P, Q, X = (('$', n) for n in 'pqx')
VALUES = [0, 1, -7, 0.5, 3.0, '', '0', 'ab', '00', ' 3 ', TRUE, FALSE, UNDEF]
show_it = ('?:', ('call', 'defined', [IT]), join('<', IT, '>'), 'undef')

def for_cases():
    c = Cases(0)
    # The block form, over every kind of list.
    def kinds(f, g, G):
        a, e, line = g('a'), g('e'), g('line')
        L = G('line')
        s = [mya(a, 1, 2, 3), ('mya', e, None), ('my', line, ''), sub(f('two'), [], returns(lst('p', 'q'))), sub(f('none'), [], returns())]
        for its in ([A(a)], [1, 2, 3], [A(e)], [lst()], [A(a), 9, A(e)], [('slice', a, [2, 0])], [('..', 2, 5)], [0, ('..', 1, 2)], [('xl', [A(a)], 2)],
                    [el(a, 0), el(a, 2)], [ucall(f('two')), ucall(f('none'))], [rev(A(a))], [UNDEF, 0, '', TRUE, FALSE, 1.5], [('scalar', a)], [('?:', 1, A(a), A(e))], [lst(1, lst(2, lst(3)))]):
            s += [do(set_(line, '')), forit(its, do(set_(line, show_it, '.='))), say_(L)]
        return s
    c.case(kinds)
    # One inside another: the inner `$_` hides the outer, which is itself
    # again after; a list sees the `$_` outside it; labels, last and next.
    def nested(f, g, G):
        a, b, line = g('a'), g('b'), g('line')
        L = G('line')
        add = lambda *vs: do(set_(line, join(*vs, ' '), '.='))
        return [mya(a, 1, 2, 3), mya(b, 10, 20), ('my', line, ''),
                forit([A(a)], add('o', IT), forit([A(b)], add('i', IT)), add('o', IT)), say_(L), do(set_(line, '')),
                forit([A(a)], forit([('..', 1, IT)], add(IT))), say_(L), do(set_(line, '')),
                forit([A(a)], forit([IT, ('*', IT, 10)], add(IT))), say_(L), do(set_(line, '')),
                forit([A(a)], over('x', [A(b)], add(IT, X))), say_(L), do(set_(line, '')),
                over('x', [A(a)], forit([A(b)], add(X, IT))), say_(L), do(set_(line, '')),
                forit([A(a)], ('mod', ('next', None), 'if', ('==', IT, 2)), add(IT)), say_(L), do(set_(line, '')),
                forit([A(a)], ('mod', ('last', None), 'if', ('==', IT, 2)), add(IT)), say_(L), do(set_(line, '')),
                forit([A(a)], forit([A(b)], ('mod', ('next', 'OUT'), 'if', ('==', IT, 20)), add(IT)), label='OUT'), say_(L), do(set_(line, '')),
                forit([A(a)], ('my', 'k', 0), ('while', None, ('<', ('$', 'k'), IT), [add(IT, ('$', 'k')), do(step('k'))])), say_(L), do(set_(line, '')),
                # A copy: the array is as it was.
                forit([A(a)], ('my', 'c', IT), do(set_('c', 10, '*=')), add(('$', 'c'))), say_(L), dump(a), do(set_(line, '')),
                # Another array changed, and the array read.
                forit([A(a)], do(('push', b, [('*', IT, el(a, 0))])), add(('scalar', a), el(a, -1))), say_(L), dump(b)]
    c.case(nested)
    # The modifier: each kind of statement under it.
    def modifier(f, g, G):
        a, b, n, t = g('a'), g('b'), g('n'), g('t')
        return [mya(a, 1, 2, 3), ('mya', b, None), ('my', n, 0), ('my', t, ''),
                sub(f('note'), [req('p')], do(set_(t, join(P, ';'), '.=')), returns(0)),
                formod(say_(IT), A(a)), formod(say_(join('v', IT)), 7, A(a)), formod(sayl(IT, IT), ('..', 1, 2)),
                formod(do(set_(n, IT, '+=')), A(a), 10), say_(G('n')),
                formod(do(step(n)), A(a)), say_(G('n')),
                formod(do(('push', b, [('*', IT, 2), IT])), A(a)), dump(b),
                formod(do(ucall(f('note'), IT)), rev(A(a))), say_(G('t')),
                formod(do(setel(b, IT, 0)), ('..', 0, 1)), dump(b),
                formod(do(set_(t, IT, '.=')), lst()), say_(G('t')),
                formod(say_('never'), A(g('b2'))) if False else say_('-'),
                # In a loop, and in a block form's block.
                forit([A(a)], formod(do(set_(n, IT, '+=')), ('..', 1, IT)), say_(join(IT, ':', G('n')))),
                over('x', [1, 2], formod(say_(join(X, IT)), A(a)))]
    c.case(modifier)
    # In subs: the file's array, the sub's own, `$_` handed on as an
    # argument, and a sub that runs a `for` of its own, called from one.
    def in_subs(f, g, G):
        a = g('a')
        return [mya(a, 4, 8, 15),
                sub(f('total'), [], ('my', 't', 0), forit([A(a)], do(set_('t', IT, '+='))), returns(('$', 't'))),
                sub(f('find'), [req('p')], forit([A(a)], ('mod', returns(IT), 'if', ('>', IT, P))), returns(-1)),
                sub(f('twice'), [req('p')], returns(('*', P, 2))),
                sub(f('inner'), [req('p')], ('my', 't', 0), formod(do(set_('t', IT, '+=')), ('..', 1, P)), returns(('$', 't'))),
                sub(f('all'), [slurp('v')], ('my', 't', ''), formod(do(set_('t', IT, '.=')), A('v')), returns(('$', 't'))),
                say_(ucall(f('total'))), say_(ucall(f('find'), 5)), say_(ucall(f('find'), 99)),
                forit([A(a)], say_(ucall(f('twice'), IT))),
                forit([1, 2, 3], say_(join(IT, ':', ucall(f('inner'), IT), ':', IT))),
                say_(ucall(f('all'), A(a), 16)), say_(ucall(f('all')))]
    c.case(in_subs)
    return c.out

def map_cases():
    c = Cases(100)
    def kinds(f, g, G):
        a, e, r = g('a'), g('e'), g('r')
        s = [mya(a, 1, 2, 3), ('mya', e, None), ('mya', r, None), sub(f('two'), [], returns(lst('p', 'q'))), sub(f('twice'), [req('p')], returns(('*', P, 2)))]
        # What a block gives: a value, two, none, some by a test, a list
        # of calls, an array; over each kind of list.
        blocks = [[('*', IT, 2)], [lst(IT, ('+', IT, 10))], [lst()], [('?:', ('>', IT, 1), lst(IT), lst())], [ucall(f('twice'), IT)], [lst(ucall(f('two')), IT)],
                  [A(a)], [('xl', [IT], 2)], [('..', 1, IT)], [rev(IT, 0)], [UNDEF], [join('<', IT, '>')], [('?:', ('==', IT, 2), 'two', IT)],
                  [('my', 't', ('*', IT, IT)), ('+', ('$', 't'), 1)], [('my', 't', IT), do(set_('t', 3, '*=')), ('mod', do(set_('t', 0)), 'if', ('==', IT, 2)), ('$', 't')],
                  [('mya', 'm', None), do(('push', 'm', [IT, IT])), A('m')], [('scalar', a)], [el(a, ('-', IT, 1))], [jn('-', IT, IT)]]
        for b in blocks:
            s += [seta(r, mp([A(a)], *b)), dump(r)]
        for its in ([1, 2, 3], [A(e)], [lst()], [A(a), 9, A(e)], [('slice', a, [2, 0])], [('..', 2, 4)], [('xl', [A(a)], 2)], [el(a, 0), el(a, 2)], [ucall(f('two'))], [rev(A(a))],
                    [('?:', 0, A(a), A(e))], [UNDEF, 0, ''], [mp([A(a)], ('*', IT, 3))], [gr([A(a)], ('>', IT, 1))]):
            s += [seta(r, mp(its, show_it)), dump(r)]
        return s
    c.case(kinds)
    # Every place a list is wanted, and where one value is: the count.
    def places(f, g, G):
        a, r = g('a'), g('r')
        M = lambda: mp([A(a)], ('*', IT, 2))
        pair = lambda: mp([A(a)], lst(IT, IT))
        return [mya(a, 1, 2, 3), ('mya', r, None),
                sub(f('cnt'), [slurp('v')], returns(jn(',', ('scalar', 'v'), A('v')))),
                sub(f('mapped'), [slurp('v')], returns(mp([A('v')], ('+', IT, 100)))),
                sub(f('last'), [slurp('v')], do(mp([A('v')], ('-', IT)))),
                sayl(M()), sayl('[', M(), '|', pair(), ']'), say_(jn(',', M())), say_(ucall(f('cnt'), M())), say_(ucall(f('cnt'), 0, pair(), 0)),
                ('lassign', True, [('$', g('x')), ('$', g('y'))], [M()]), say_(join(G('x'), G('y'))),
                do(('push', r, [M()])), dump(r), over('v', [M()], sayl('v', ('$', 'v'))), forit([pair()], sayl('i', IT)),
                sayl(('lslice', [M()], [2, 0])), sayl(rev(M())), sayl(('xl', [M()], 2)), formod(say_(IT), M()),
                seta(r, ucall(f('mapped'), A(a))), dump(r), seta(r, ucall(f('last'), 5, 6)), dump(r),
                seta(a, mp([A(a)], ('*', IT, 10))), dump(a),
                seta(a, mp([A(a)], lst(IT, IT))), dump(a),
                # The count.
                ('my', g('n'), pair()), say_(G('n')), say_(('+', M(), 1)), say_(join('n', M())), say_(('scalar', a)),
                ('if', [(mp([A(a)], lst()), [say_('never')]), (M(), [say_('some')])], None),
                say_(('?:', mp([lst()], IT), 'yes', 'no')), say_(el(a, mp([1, 2], IT))),
                # As a statement, for what its block does.
                do(mp([A(a)], do(('push', r, [IT])), 0)), say_(('scalar', r))]
    c.case(places)
    # One inside another, a map in a for and a for in a map's block, and a
    # block that calls a sub which maps.
    def nested(f, g, G):
        a, r = g('a'), g('r')
        return [mya(a, 1, 2, 3), ('mya', r, None),
                sub(f('row'), [req('p')], returns(jn('', mp([('..', 1, P)], ('*', IT, P))))),
                seta(r, mp([A(a)], ('my', 'o', IT), mp([('..', 1, ('$', 'o'))], join(('$', 'o'), IT)))), dump(r),
                seta(r, mp([A(a)], mp([IT, ('+', IT, 10)], ('*', IT, 2)))), dump(r),
                seta(r, mp([mp([A(a)], lst(IT, IT))], ('+', IT, 1))), dump(r),
                seta(r, mp([A(a)], ucall(f('row'), IT))), dump(r),
                seta(r, mp([A(a)], ('my', 't', 0), formod(do(set_('t', IT, '+=')), ('..', 1, IT)), join(IT, ':', ('$', 't')))), dump(r),
                seta(r, mp([A(a)], ('my', 't', ''), forit([A(a)], do(set_('t', IT, '.='))), join(IT, ('$', 't')))), dump(r),
                forit([A(a)], sayl(IT, ':', mp([('..', 1, IT)], ('*', IT, IT)), ':', IT)),
                seta(r, mp([A(a)], jn('+', mp([A(a)], IT)))), dump(r),
                # The array read from the block while it is frozen.
                seta(r, mp([A(a)], ('+', IT, el(a, 0)), )), dump(r), seta(r, mp([A(a)], ('scalar', a))), dump(r)]
    c.case(nested)
    return c.out

def grep_cases():
    c = Cases(200)
    def truths(f, g, G):
        a, v, r = g('a'), g('v'), g('r')
        s = [mya(a, 1, 2, 3, 4, 5, 6), ('mya', v, None), ('mya', r, None), sub(f('odd'), [req('p')], returns(('%', P, 2)))]
        s += [do(('push', v, [x])) for x in VALUES]
        tests = [[IT], [('!', IT)], [('call', 'defined', [IT])], [('//', IT, 1)], [1], [0], [''], ['0'], ['00'], [UNDEF], [('&&', ('call', 'defined', [IT]), ('ne', IT, ''))]]
        for t in tests:
            s += [seta(r, gr([A(v)], *t)), dump(r)]
        for t in ([('>', IT, 2)], [('%', IT, 2)], [ucall(f('odd'), IT)], [('==', IT, el(a, 2))], [('my', 'h', ('*', IT, 2)), ('>', ('$', 'h'), 7)], [('&&', ('>', IT, 1), ('<', IT, 5))],
                  [('scalar', a)], [('?:', ('==', IT, 3), 0, 1)], [gr([A(a)], ('>', IT, 5))], [mp([lst()], IT)]):
            s += [seta(r, gr([A(a)], *t)), dump(r)]
        return s
    c.case(truths)
    def places(f, g, G):
        a, e, r = g('a'), g('e'), g('r')
        big = lambda: gr([A(a)], ('>', IT, 2))
        return [mya(a, 1, 2, 3, 4), ('mya', e, None), ('mya', r, None),
                sub(f('cnt'), [slurp('v')], returns(jn(',', ('scalar', 'v'), A('v')))),
                sub(f('has'), [req('p')], returns(('?:', gr([A(a)], ('==', IT, P)), 'yes', 'no'))),
                sub(f('kept'), [slurp('v')], returns(gr([A('v')], ('<', IT, 3)))),
                sayl(big()), say_(jn(',', big())), say_(ucall(f('cnt'), big(), 9)), over('x', [big()], sayl('x', X)), formod(say_(IT), big()),
                ('lassign', True, [('$', g('x')), ('$', g('y'))], [big()]), say_(join(G('x'), G('y'))),
                seta(r, rev(big())), dump(r), seta(r, mp([big()], ('*', IT, 2))), dump(r), seta(r, gr([mp([A(a)], ('*', IT, 2))], ('>', IT, 4))), dump(r),
                seta(r, gr([A(e)], 1)), dump(r), seta(r, gr([lst()], 1)), dump(r), seta(r, gr([A(a), 9, A(a)], ('>', IT, 3))), dump(r),
                seta(r, gr([('..', 1, 10)], ('==', ('%', IT, 3), 0))), dump(r), seta(r, gr([('slice', a, [3, 0])], 1)), dump(r),
                seta(r, ucall(f('kept'), A(a), 0)), dump(r),
                # The count, and the test.
                ('my', g('n'), big()), say_(G('n')), say_(('+', big(), 0)), say_(join('n', gr([A(a)], 0))),
                ('if', [(gr([A(a)], ('==', IT, 9)), [say_('never')]), (gr([A(a)], ('==', IT, 2)), [say_('has 2')])], None),
                say_(ucall(f('has'), 3)), say_(ucall(f('has'), 7)),
                ('while', None, ('>', gr([A(a)], ('>', IT, 2)), 0), [do(('pop', a))]), dump(a),
                # A copy: the array is as it was, and what was kept is the
                # caller's own.
                seta(a, 5, 6, 7), seta(r, gr([A(a)], 1)), do(setel(r, 0, 'r')), dump(a), dump(r),
                seta(a, gr([A(a)], ('>', IT, 5))), dump(a),
                do(gr([A(a)], do(('push', r, [IT])), 1)), dump(r)]
    c.case(places)
    return c.out

SAME = {'1100': ('for-it', for_cases), '1101': ('map', map_cases), '1102': ('grep', grep_cases)}

def faults():
    out = {}
    n = [1110]
    def fault(name, subs_, near, far):
        out[str(n[0])] = ('fault-' + name, subs_, near, far)
        n[0] += 1
    a3 = lambda: mya('a', 1, 2, 3)
    quiet = ('+', IT, 0)
    # Each binder, and each way its array is changed while it runs: in a
    # run that only reads, and then one that changes. T131, twice over:
    # perl carries on where this faults, so a `for` that pushes onto its
    # array never ends (the block form's change is followed by a `last`,
    # and the modifier has no push), and perl 5.42 itself crashes on a
    # grep whose block shifts or assigns its array (T194): no test of
    # those two.
    ways = [('store', do(setel('a', 0, 9))), ('push', do(('push', 'a', [4]))), ('shift', do(('shift', 'a'))), ('assign', seta('a', 7)), ('splice', do(('splice', 'a', [0, 0])))]
    poke = sub('poke', [], do(setel('a', 2, 30)), returns(0))
    binders = [
        ('for', lambda *b: forit([A('a')], *b, *([('last', None)] if b else [say_(IT)]))),
        ('for-modifier', None),
        ('map', lambda *b: ('mya', 'r', [mp([A('a')], *b, quiet)])),
        ('grep', lambda *b: ('mya', 'r', [gr([A('a')], *b, quiet)])),
    ]
    for bname, make in binders:
        for wname, change in ways:
            if make is None:
                if change[0] != 'do' or wname == 'push':
                    continue
                fault(f'frozen-{bname}-{wname}', [], block(a3(), formod(say_(IT), A('a'))), block(a3(), formod(change, A('a'))))
            elif not (bname == 'grep' and wname in ('shift', 'assign')):
                fault(f'frozen-{bname}-{wname}', [], block(a3(), make()), block(a3(), make(change)))
        if make is not None:
            fault(f'frozen-{bname}-from-a-sub', [mya('a', 1, 2, 3), poke], block(make()), block(make(do(ucall('poke')))))
    fault('frozen-for-modifier-from-a-sub', [mya('a', 1, 2, 3), poke], formod(say_(IT), A('a')), formod(do(ucall('poke')), A('a')))
    # Given back when the binder ends: a change after it, and then one in
    # it.
    store = do(setel('a', 0, 9))
    fault('given-back-after-a-map', [], block(a3(), ('mya', 'r', [mp([A('a')], quiet)]), store, dump('a')), block(a3(), ('mya', 'r', [mp([A('a')], store, quiet)])))
    fault('given-back-after-a-grep', [], block(a3(), ('mya', 'r', [gr([A('a')], quiet)]), store, dump('a')), block(a3(), ('mya', 'r', [gr([A('a')], store, quiet)])))
    fault('given-back-after-a-for-modifier', [], block(a3(), formod(say_(IT), A('a')), store, dump('a')), block(a3(), formod(store, A('a'))))
    # One binder in another's block, over one array: the inner one ending
    # leaves it frozen.
    fault('frozen-after-the-inner-map', [], block(a3(), ('mya', 'r', [mp([A('a')], mp([A('a')], quiet))])), block(a3(), ('mya', 'r', [mp([A('a')], ('mya', 'q', [mp([A('a')], quiet)]), store, quiet)])))
    # Each shape that names the array, for a map.
    for name, its in (('second-of-two', [A('b'), A('a')]), ('slice', [('slice', 'a', [0, 1])]), ('element', [el('a', 1)]), ('reverse', [rev(A('a'))]),
                      ('a-grep-of-it', [gr([A('a')], 1)]), ('a-map-of-it', [mp([A('a')], IT)]), ('last-index', [('..', 0, ('last', 'a'))])):
        fault('map-names-by-' + name, [], block(a3(), mya('b', 7), ('mya', 'r', [mp(its, quiet)])), block(a3(), mya('b', 7), ('mya', 'r', [mp(its, store, quiet)])))
    # Past the end, in each binder's list (T177).
    for bname, make in (('for', lambda its: forit(its, say_(IT))), ('for-modifier', lambda its: formod(say_(IT), *its)),
                        ('map', lambda its: ('mya', 'r', [mp(its, quiet)])), ('grep', lambda its: ('mya', 'r', [gr(its, quiet)]))):
        fault(f'element-past-the-end-in-a-{bname}', [], block(a3(), make([el('a', 2)])), block(a3(), make([el('a', 3)])))
        fault(f'slice-past-the-end-in-a-{bname}', [], block(a3(), make([('slice', 'a', [0, 2])])), block(a3(), make([('slice', 'a', [0, 3])])))
    # D18: a map and a grep after return, for one value.
    fault('map-returned-for-one-value', [mya('a', 1, 2, 3), sub('f', [], returns(mp([A('a')], IT)))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    fault('grep-returned-for-one-value', [mya('a', 1, 2, 3), sub('f', [], returns(gr([A('a')], IT)))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    fault('map-as-a-last-statement-for-one-value', [mya('a', 1, 2, 3), sub('f', [], do(mp([A('a')], IT)))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    # A fault in a block; in a block's value; in a list.
    fault('in-a-map-block', [], block(a3(), ('mya', 'r', [mp([A('a')], ('my', 't', ('/', 6, IT)), ('$', 't'))])), block(a3(), ('mya', 'r', [mp([A('a')], ('my', 't', ('/', 6, ('-', IT, 2))), ('$', 't'))])))
    fault('in-a-grep-test', [], block(a3(), ('mya', 'r', [gr([A('a')], ('>', IT, 1))])), block(a3(), ('mya', 'r', [gr([A('a'), UNDEF], ('>', IT, 1))])))
    fault('under-a-for-modifier', [], block(a3(), ('my', 't', 0), formod(do(set_('t', ('/', 6, IT), '+=')), A('a'))), block(a3(), ('my', 't', 0), formod(do(set_('t', ('/', 6, ('-', IT, 3)), '+=')), A('a'))))
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/it.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/it.py {n} > t/{n}-{name}.expected\n'
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
    model = ['model: t/models/it.py']
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
    lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

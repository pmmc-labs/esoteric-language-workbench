#!/usr/bin/env python3
"""t/1300 to t/1342: a variable in a double-quoted string (step 11a; D91 to D95).

The definition, which is all this file knows of the language beyond
t/models/sort.py.

  "text $x text"      the text, and the scalar made a string
  "${x}text"          the same: the braces end the name
  "@a" "@{a}"         the array's values, one space between each two
  "$a[I]"             the element
  "@a[I, J .. K]"     the slice, one space between each two
  "$#a" "$#{a}"       the last index

**An interpolated string is one value, a Str, made where it stands**: its
pieces from left to right, each made a string as `.` makes one (a number
as it prints, a boolean `1` or the empty string, the fault for a whole Num
from 10^15), an array's or a slice's values as `join(" ", ...)` joins
them. **An undef is a fault wherever it stands**: a scalar, an element
past either end, a value of an array or of a slice.

An index in a string is a whole number or a scalar variable (D91), so
nothing in a string changes anything, and the order its pieces are read in
does not show. A string names nothing: in a loop's list it freezes no
array, and an element in it past the end is the string's fault, an undef,
and not the list's (T209).

This model works a program out; it does not refuse one. Which `$` and `@`
begin a variable, where a name ends and what may follow it (D92) are the
lexer's, and its refusals are tests written by hand.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

1300 is scalars, 1301 arrays, elements, slices and `$#a`, 1302 strings
where the language has blocks, loops and subs. 1310 on each fault once.

A case's statements are tried one at a time, and one that faults is left
out of a `same` test (a string that is no number, where a number is
wanted): the faults have tests of their own.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/interp.py --program 1300 > t/1300-interpolate-scalars.pl
    python3 t/models/interp.py 1300 > t/1300-interpolate-scalars.expected
    python3 t/models/interp.py --program 1301 > t/1301-interpolate-arrays.pl
    python3 t/models/interp.py 1301 > t/1301-interpolate-arrays.expected
    python3 t/models/interp.py --program 1302 > t/1302-interpolate-in-blocks-loops-subs.pl
    python3 t/models/interp.py 1302 > t/1302-interpolate-in-blocks-loops-subs.expected
    python3 t/models/interp.py --program 1310 > t/1310-fault-interpolate-undef.pl
    python3 t/models/interp.py 1310 > t/1310-fault-interpolate-undef.expected
    python3 t/models/interp.py --program 1311 > t/1311-fault-interpolate-undef-in-braces.pl
    python3 t/models/interp.py 1311 > t/1311-fault-interpolate-undef-in-braces.expected
    python3 t/models/interp.py --program 1312 > t/1312-fault-interpolate-undef-after-text.pl
    python3 t/models/interp.py 1312 > t/1312-fault-interpolate-undef-after-text.expected
    python3 t/models/interp.py --program 1313 > t/1313-fault-interpolate-undef-in-an-array.pl
    python3 t/models/interp.py 1313 > t/1313-fault-interpolate-undef-in-an-array.expected
    python3 t/models/interp.py --program 1314 > t/1314-fault-interpolate-undef-in-a-braced-array.pl
    python3 t/models/interp.py 1314 > t/1314-fault-interpolate-undef-in-a-braced-array.expected
    python3 t/models/interp.py --program 1315 > t/1315-fault-interpolate-undef-element.pl
    python3 t/models/interp.py 1315 > t/1315-fault-interpolate-undef-element.expected
    python3 t/models/interp.py --program 1316 > t/1316-fault-interpolate-undef-in-a-slice.pl
    python3 t/models/interp.py 1316 > t/1316-fault-interpolate-undef-in-a-slice.expected
    python3 t/models/interp.py --program 1317 > t/1317-fault-interpolate-element-past-the-end.pl
    python3 t/models/interp.py 1317 > t/1317-fault-interpolate-element-past-the-end.expected
    python3 t/models/interp.py --program 1318 > t/1318-fault-interpolate-element-before-the-start.pl
    python3 t/models/interp.py 1318 > t/1318-fault-interpolate-element-before-the-start.expected
    python3 t/models/interp.py --program 1319 > t/1319-fault-interpolate-element-of-an-empty-array.pl
    python3 t/models/interp.py 1319 > t/1319-fault-interpolate-element-of-an-empty-array.expected
    python3 t/models/interp.py --program 1320 > t/1320-fault-interpolate-last-element-of-an-empty-array.pl
    python3 t/models/interp.py 1320 > t/1320-fault-interpolate-last-element-of-an-empty-array.expected
    python3 t/models/interp.py --program 1321 > t/1321-fault-interpolate-element-by-a-scalar-past-the-end.pl
    python3 t/models/interp.py 1321 > t/1321-fault-interpolate-element-by-a-scalar-past-the-end.expected
    python3 t/models/interp.py --program 1322 > t/1322-fault-interpolate-slice-past-the-end.pl
    python3 t/models/interp.py 1322 > t/1322-fault-interpolate-slice-past-the-end.expected
    python3 t/models/interp.py --program 1323 > t/1323-fault-interpolate-slice-range-past-the-end.pl
    python3 t/models/interp.py 1323 > t/1323-fault-interpolate-slice-range-past-the-end.expected
    python3 t/models/interp.py --program 1324 > t/1324-fault-interpolate-slice-range-before-the-start.pl
    python3 t/models/interp.py 1324 > t/1324-fault-interpolate-slice-range-before-the-start.expected
    python3 t/models/interp.py --program 1325 > t/1325-fault-interpolate-whole-num.pl
    python3 t/models/interp.py 1325 > t/1325-fault-interpolate-whole-num.expected
    python3 t/models/interp.py --program 1326 > t/1326-fault-interpolate-whole-num-after-text.pl
    python3 t/models/interp.py 1326 > t/1326-fault-interpolate-whole-num-after-text.expected
    python3 t/models/interp.py --program 1327 > t/1327-fault-interpolate-whole-num-in-an-array.pl
    python3 t/models/interp.py 1327 > t/1327-fault-interpolate-whole-num-in-an-array.expected
    python3 t/models/interp.py --program 1328 > t/1328-fault-interpolate-whole-num-element.pl
    python3 t/models/interp.py 1328 > t/1328-fault-interpolate-whole-num-element.expected
    python3 t/models/interp.py --program 1329 > t/1329-fault-interpolate-whole-num-in-a-slice.pl
    python3 t/models/interp.py 1329 > t/1329-fault-interpolate-whole-num-in-a-slice.expected
    python3 t/models/interp.py --program 1330 > t/1330-fault-interpolate-index-undef.pl
    python3 t/models/interp.py 1330 > t/1330-fault-interpolate-index-undef.expected
    python3 t/models/interp.py --program 1331 > t/1331-fault-interpolate-index-not-a-number.pl
    python3 t/models/interp.py 1331 > t/1331-fault-interpolate-index-not-a-number.expected
    python3 t/models/interp.py --program 1332 > t/1332-fault-interpolate-index-too-large.pl
    python3 t/models/interp.py 1332 > t/1332-fault-interpolate-index-too-large.expected
    python3 t/models/interp.py --program 1333 > t/1333-fault-interpolate-slice-index-not-a-number.pl
    python3 t/models/interp.py 1333 > t/1333-fault-interpolate-slice-index-not-a-number.expected
    python3 t/models/interp.py --program 1334 > t/1334-fault-interpolate-slice-range-end-a-string.pl
    python3 t/models/interp.py 1334 > t/1334-fault-interpolate-slice-range-end-a-string.expected
    python3 t/models/interp.py --program 1335 > t/1335-fault-interpolate-not-a-numeric-string.pl
    python3 t/models/interp.py 1335 > t/1335-fault-interpolate-not-a-numeric-string.expected
    python3 t/models/interp.py --program 1336 > t/1336-fault-interpolate-false-is-the-empty-string.pl
    python3 t/models/interp.py 1336 > t/1336-fault-interpolate-false-is-the-empty-string.expected
    python3 t/models/interp.py --program 1337 > t/1337-fault-interpolate-element-past-the-end-in-a-loop-list.pl
    python3 t/models/interp.py 1337 > t/1337-fault-interpolate-element-past-the-end-in-a-loop-list.expected
    python3 t/models/interp.py --program 1338 > t/1338-fault-interpolate-undef-it-in-a-map-block.pl
    python3 t/models/interp.py 1338 > t/1338-fault-interpolate-undef-it-in-a-map-block.expected
    python3 t/models/interp.py --program 1339 > t/1339-fault-interpolate-undef-in-a-sort-block.pl
    python3 t/models/interp.py 1339 > t/1339-fault-interpolate-undef-in-a-sort-block.expected
    python3 t/models/interp.py --program 1340 > t/1340-fault-interpolate-undef-under-a-for-modifier.pl
    python3 t/models/interp.py 1340 > t/1340-fault-interpolate-undef-under-a-for-modifier.expected
    python3 t/models/interp.py --program 1341 > t/1341-fault-interpolate-undef-argument.pl
    python3 t/models/interp.py 1341 > t/1341-fault-interpolate-undef-argument.expected
    python3 t/models/interp.py --program 1342 > t/1342-fault-interpolate-undef-returned.pl
    python3 t/models/interp.py 1342 > t/1342-fault-interpolate-undef-returned.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import list as lists
import each
import ret
import it
import sort
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import SCALAR, ucall, sub, req, say_, named
from sub import ret as returns
from list import A, el, mya, seta, sayl, setel, dump, Cases, items
from each import each as over
from ret import jn, rev
from it import IT, forit, formod, mp, gr
from sort import VA, VB, srt

# A string: ('qq', [pieces]). A piece is text, a Python str, or one of
#   ('$', name)  ('${', name)       a scalar, bare and in braces
#   ('@', name)  ('@{', name)       an array
#   ('elem', name, index)           an element
#   ('slice', name, [indexes])      a slice
#   ('last', name)  ('last{', name) the last index
# An index is a whole number or ('$', name); in a slice, ('..', i, j) too.

def qq(*pieces):
    return ('qq', list(pieces))

BRACED = {'${': '$', '@{': '@', 'last{': 'last'}

def plain(piece):
    """A piece as the expression it is outside a string."""
    return (BRACED[piece[0]],) + piece[1:] if piece[0] in BRACED else piece

class Run(sort.Run):
    def ev(self, e):
        if not isinstance(e, tuple) or e[0] != 'qq':
            return super().ev(e)
        out = ''
        for piece in e[1]:
            if isinstance(piece, str):
                out += piece
                continue
            p = plain(piece)
            if p[0] in ('@', 'slice'):
                out += ' '.join(logic.value(('.', v, '')) for v in self.evl(p))
            else:
                out += logic.value(('.', get(self.ev(p)), ''))
        self.ctx = SCALAR
        return out

# A string names nothing: not for the arrays a loop freezes (T209).
_names = each.names

def names(e, into):
    return into if isinstance(e, tuple) and e[0] == 'qq' else _names(e, into)

each.names = names

# ---- as source

WORD = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

def chars(s):
    out = ''
    for c in s:
        if c == '\n': out += '\\n'
        elif c == '\t': out += '\\t'
        elif c in '"\\$@': out += '\\' + c
        else:
            assert ' ' <= c <= '~', s
            out += c
    return out

def index_text(i):
    if isinstance(i, tuple) and i[0] == '..':
        return f'{index_text(i[1])} .. {index_text(i[2])}'
    if isinstance(i, tuple):
        assert i[0] == '$', i
        return '$' + i[1]
    assert isinstance(i, int) and not isinstance(i, bool), i
    return str(i)

def piece_text(p):
    kind = p[0]
    if kind == '$': return '$' + p[1]
    if kind == '${': return '${' + p[1] + '}'
    if kind == '@': return '@' + p[1]
    if kind == '@{': return '@{' + p[1] + '}'
    if kind == 'last': return '$#' + p[1]
    if kind == 'last{': return '$#{' + p[1] + '}'
    if kind == 'elem': return f'${p[1]}[{index_text(p[2])}]'
    assert kind == 'slice' and (len(p[2]) > 1 or p[2][0][0] == '..'), p
    return f'@{p[1]}[{", ".join(index_text(i) for i in p[2])}]'

def qq_text(e, top):
    out = ''
    before = None
    # Two pieces of text side by side are one, to the lexer.
    pieces = []
    for piece in e[1]:
        if isinstance(piece, str) and pieces and isinstance(pieces[-1], str):
            pieces[-1] += piece
        else:
            pieces.append(piece)
    for piece in pieces:
        if isinstance(piece, str):
            # What the lexer would take into the variable before it, or
            # refuse after it (D92): the case is written wrong.
            if before is not None and before[0] not in BRACED:
                assert piece[0] not in '[{', (before, piece)
                assert not piece.startswith('::') and not (piece.startswith('->') and piece[2:3] in ('[', '{', '@', '$')), (before, piece)
                assert not (before[0] in ('$', '@', 'last') and piece[0] in WORD), (before, piece)
            out += chars(piece)
        else:
            out += piece_text(piece)
        before = None if isinstance(piece, str) else piece
    return f'"{out}"'

var.MORE['qq'] = qq_text
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

def quiet(setup, candidates):
    """The candidates that do not fault after the setup, in order."""
    return [c for c in candidates if output(setup + [c])[1] is None]

# ---- the cases

shown = var.shown
D, B = (lambda n: ('$', n)), (lambda n: ('${', n))
# Every kind of value that a string takes in silence.
VALUES = [0, 1, -7, 41, 2**53, -2**63, 0.5, 3.0, -0.0, 1.5e300, 1e21, 0.1, 1 / 3, 999999999999999.0, '', '0', 'ab', ' 3 ', '00', '3.0', '1e3', '12abc', 'a b',
          "it's", 'x[1]', 'p::q', '5', '-5', '+5', TRUE, FALSE]

def scalar_cases():
    c = Cases(0)
    # Each kind of value, in each shape, with text of every kind round it.
    def shapes(f, g, G):
        out = []
        w = g('w')
        setup = [('my', w, 'W')]
        for n, v in enumerate(VALUES):
            x = f'{g("x")}_{n}'
            mine = [('my', x, v)]
            tries = [qq(D(x)), qq(B(x)), qq('<', D(x), '>'), qq(B(x), 'x'), qq(B(x), '_'), qq(D(x), ' ', D(w)), qq(D(x), D(w)), qq(D(x), B(w), D(x)),
                     qq(D(x), "'s"), qq(D(x), ': ', B(w), '9'), qq(D(x), '->y'), qq(D(x), '->'), qq(D(x), '-1'), qq(D(x), '.', D(w)), qq(D(x), ':'), qq(D(x), ']'),
                     qq(D(x), '}'), qq(D(x), ')'), qq(D(x), '('), qq(D(x), '%'), qq(D(x), '\\'), qq('\\', D(x)), qq('$', D(x)), qq(D(x), '$'), qq(D(x), '@'),
                     qq('a\tb "q" $5 me@x ', D(x), '\n-'), qq(B(x), '[1]'), qq(B(x), '{a}'), qq(B(x), '::y'), qq(B(x), '->[0]'), qq(D(x), ' [1]'), qq(D(x), ' {a}'),
                     qq(D(x), '-> [0]'), qq(D(x), '- >[0]'), qq(D(x), '#'), qq('#', D(x)), qq(D(x), '=', D(x)), qq(D(x), '+', D(x), '!')]
            out += mine + [say_(t) for t in tries]
        return setup + out
    c.case(shapes)
    # A string is a Str, whatever it holds: what a later operation sees.
    def later(f, g, G):
        out = []
        for n, v in enumerate(VALUES):
            x, s = f'{g("x")}_{n}', f'{g("s")}_{n}'
            mine = [('my', x, v), ('my', s, qq(D(x)))]
            q = qq(D(x))
            tries = [shown(D(s)), say_(('.', q, 'z')), say_(('x', q, 2)), say_(('call', 'length', [q])), say_(('eq', q, ('.', D(x), ''))),
                     say_(('+', q, 0)), say_(('*', q, 2)), say_(('-', q)), say_(('==', q, 1)), say_(('<', q, 1.5)), say_(('!', q)), say_(('?:', q, 'T', 'F')),
                     say_(('||', q, 'none')), say_(('//', q, 'undef')), say_(('lt', q, 'b')), say_(('call', 'defined', [q])), say_(('+', qq('0', D(x)), 1)),
                     say_(('+', qq(B(x), '0'), 1)), say_(('+', qq(D(x), '.', D(x)), 1)), say_(('call', 'substr', ['abcdefgh', q])),
                     block(('my', 't', q), do(step('t')), shown(D('t'))), block(('my', 't', q), do(step('t', '--')), shown(D('t'))),
                     block(('my', 't', ''), do(set_('t', q, '.=')), do(set_('t', qq(D('t'), '|', D(x)), '.=')), shown(D('t'))),
                     block(('my', 't', q), do(set_('t', qq(D('t'), D('t')))), shown(D('t')))]
            out += mine + quiet(mine, tries)
        return out
    c.case(later)
    return c.out

def array_cases():
    c = Cases(0)
    def arrays(f, g, G):
        a, b, e, one, i, j = g('a'), g('b'), g('e'), g('one'), g('i'), g('j')
        setup = [mya(a, *VALUES), mya(b, 'p', 'q', 'r', 's', 't'), ('mya', e, None), mya(one, 'only'), ('my', i, 1), ('my', j, 3)]
        tries = [qq(('@', a)), qq('[', ('@', a), ']'), qq(('@{', a), 's'), qq(('@', b), ('@', one)), qq(('@', b), ' ', ('@', one)), qq('[', ('@', e), ']'),
                 qq(('@', e), ('@', e)), qq(('@', one)), qq(('@', b), "'s"), qq(('@', b), ':'), qq(('@', b), '->'), qq(('@', b), ' [0]'), qq(('@{', b), '[0]'),
                 qq(('@{', b), '::x'), qq('me@', ('@', b), '.com'), qq(('@', b), '.', ('@', b)),
                 qq(('last', b)), qq(('last{', b), 'x'), qq(('last', b), '/', ('@', b)), qq(('last', e)), qq(('last', b), '->'), qq(('last{', b), '[0]'),
                 qq(('last', b), ':'), qq('n=', ('last', b), ': ', ('@', b), ' (', ('elem', b, 0), '..', ('elem', b, -1), ')')]
        for k in (0, 1, 4, -1, -5, D(i), D(j)):
            tries += [qq(('elem', b, k)), qq('<', ('elem', b, k), '>'), qq(('elem', b, k), ('elem', b, 0)), qq(('elem', b, k), 's'), qq(('elem', b, k), '->'),
                      qq(('elem', b, k), ' [0]'), qq(('elem', b, k), ':'), qq(('elem', b, k), "'"), qq(('elem', b, k), '-1')]
        for n in range(len(VALUES)):
            tries.append(qq(('elem', a, n), '|', ('elem', a, n - len(VALUES))))
        for idx in ([0, 1], [-1, 0], [D(i), D(j)], [('..', 0, 1)], [('..', D(i), D(j))], [0, ('..', 2, 3)], [('..', 2, 0)], [0, 0, 0], [('..', -2, -1)],
                    [('..', 1, 1)], [('..', 0, 4)], [D(j), ('..', D(i), 2), -1], [4, 3, 2, 1, 0]):
            tries += [qq(('slice', b, idx)), qq('[', ('slice', b, idx), ']'), qq(('slice', b, idx), 's'), qq(('slice', b, idx), '->'), qq(('slice', b, idx), ' [0]')]
        # An index held in a scalar, of every kind an index may be.
        out = []
        for n, v in enumerate((0, 4, -1, 1.9, -1.9, 0.5, '2', ' 1 ', '-1', TRUE, FALSE)):
            k = f'{g("k")}_{n}'
            mine = setup + [('my', k, v)]
            out += [('my', k, v)] + quiet(mine, [say_(qq(('elem', b, D(k)))), say_(qq(('slice', b, [D(k), 0]))), say_(qq(('slice', b, [('..', 0, D(k))]), '|'))])
        # As operands, and stored.
        s = g('s')
        after = [('my', s, qq(('@', b))), shown(D(s)), say_(('call', 'length', [qq(('@', b))])), say_(('x', qq(('@', one)), 2)), say_(('.', qq(('@', b)), qq(('@', b)))),
                 say_(('eq', qq(('@', b)), jn(' ', A(b)))), say_(('+', qq(('last', b)), 1)), say_(('+', qq(('elem', a, 3)), 1)),
                 seta(e, qq(('@', b)), qq(('@', b))), dump(e), do(setel(e, 0, qq(('@', e)))), dump(e), do(('push', e, [qq(('@', e))])), dump(e),
                 seta(b, qq(('@', b))), dump(b)]
        return setup + [say_(t) for t in tries] + out + after
    c.case(arrays)
    return c.out

def place_cases():
    c = Cases(0)
    # In a block of each binder, with its variable; in a loop's list, which
    # a string does not freeze; as an argument and a returned value.
    def binders(f, g, G):
        a, r, n = g('a'), g('r'), g('n')
        return [mya(a, 3, 'b', 1.5, TRUE, ''), ('mya', r, None), ('my', n, 0),
                forit([A(a)], say_(qq('<', IT, '>'))), formod(say_(qq(IT, ':')), A(a)), formod(say_(qq(B('_'), '_')), 1, 2),
                over('v', [A(a)], say_(qq(D('v'), '/', ('@', a)))),
                seta(r, mp([A(a)], qq(IT, '-'))), dump(r), seta(r, mp([A(a)], ('list', [qq('a', IT), qq(IT)]))), dump(r),
                seta(r, gr([A(a)], ('ne', qq(IT), ''))), dump(r), seta(r, gr([A(a)], qq(IT))), dump(r),
                seta(r, srt([A(a)], ('cmp', qq(VA), qq(VB)))), dump(r), seta(r, srt([A(a)], ('cmp', qq(B('b'), '!'), qq(B('a'), '!')))), dump(r),
                seta(r, srt(['z', qq(('@', a)), qq(('elem', a, 1)), qq('a', B(n))])), dump(r),
                seta(r, mp([1, 2, 3], qq(IT, '.', D(n), ' of ', ('last', a)))), dump(r),
                seta(r, mp([0, 1], qq(('elem', a, IT), '|', ('slice', a, [IT, ('..', 0, IT)])))), dump(r)]
    c.case(binders)
    def loops(f, g, G):
        a, x = g('a'), g('x')
        return [mya(a, 1, 2), ('my', x, 3),
                over('v', [qq(('@', a))], do(('push', a, [3])), say_(D('v'))), dump(a),
                over('v', [qq(('elem', a, 0)), qq(('slice', a, [0, 1])), qq(('last', a))], do(setel(a, 0, 9)), do(('push', a, [4])), say_(D('v'))), dump(a),
                over('v', [qq(D(x)), qq(D(x), '-')], do(set_(x, 5)), say_(D('v'))), say_(D(x)),
                seta(a, 1, 2), seta(a, mp([qq(('@', a)), qq(('elem', a, 1))], qq(IT, '!'))), dump(a),
                ('my', g('k'), 0),
                ('while', None, ('<', G('k'), 2), [say_(qq('k=', G('k'), ' ', ('elem', a, G('k')))), do(step(g('k')))]),
                ('mod', say_(qq('yes ', D(x))), 'if', ('eq', qq(D(x)), '5')), ('if', [(qq(D(x)), [say_(qq('true: ', D(x)))])], None)]
    c.case(loops)
    def subs(f, g, G):
        a = g('a')
        return [mya(a, 'p', 'q'),
                sub(f('show'), [req('s'), req('t')], returns(qq('[', D('s'), '|', D('t'), ']'))),
                sub(f('all'), [], returns(qq(('@', a)))),
                sub(f('lastly'), [], do(qq(('@', a), '!'))),
                say_(ucall(f('show'), qq(('@', a)), qq(('elem', a, 0), ('last', a)))), ('my', g('v'), ucall(f('all'))), say_(G('v')),
                ('my', g('w'), ucall(f('lastly'))), say_(G('w')), sayl(ucall(f('all')), ucall(f('lastly'))),
                say_(jn(qq('-', ('last', a), '-'), qq(('@', a)), qq(('elem', a, 1)))), sayl(qq(('@', a)), qq(('@', a))),
                sayl(rev(qq('a', ('elem', a, 0)), qq('b', ('elem', a, 1))))]
    c.case(subs)
    return c.out

SAME = {'1300': ('interpolate-scalars', scalar_cases), '1301': ('interpolate-arrays', array_cases), '1302': ('interpolate-in-blocks-loops-subs', place_cases)}

def faults():
    out = {}
    n = [1310]
    def fault(name, near, far, subs_=()):
        out[str(n[0])] = ('fault-interpolate-' + name, list(subs_), near, far)
        n[0] += 1
    a3 = lambda: mya('a', 1, 2, 3)
    both = lambda make, good, bad: (block(*good, say_(make())), block(*bad, say_(make())))
    # An undef, in each shape.
    fault('undef', *both(lambda: qq(D('u')), [('my', 'u', '')], [('my', 'u', None)]))
    fault('undef-in-braces', *both(lambda: qq('a', B('u'), 'b'), [('my', 'u', 0)], [('my', 'u', None)]))
    fault('undef-after-text', *both(lambda: qq('a ', D('u')), [('my', 'u', FALSE)], [('my', 'u', UNDEF)]))
    fault('undef-in-an-array', *both(lambda: qq(('@', 'a')), [mya('a', 1, '')], [mya('a', 1, UNDEF)]))
    fault('undef-in-a-braced-array', *both(lambda: qq(('@{', 'a'), 's'), [mya('a', 1, 2)], [mya('a', UNDEF, 2)]))
    fault('undef-element', *both(lambda: qq(('elem', 'a', 1)), [mya('a', 1, 2)], [mya('a', 1, UNDEF)]))
    fault('undef-in-a-slice', *both(lambda: qq(('slice', 'a', [0, 1])), [mya('a', 1, 2)], [mya('a', 1, UNDEF)]))
    # Past either end: an undef, and nothing is made.
    fault('element-past-the-end', block(a3(), say_(qq(('elem', 'a', 2)))), block(a3(), say_(qq(('elem', 'a', 3)))))
    fault('element-before-the-start', block(a3(), say_(qq(('elem', 'a', -3)))), block(a3(), say_(qq(('elem', 'a', -4)))))
    fault('element-of-an-empty-array', block(mya('a', 1), say_(qq(('elem', 'a', 0)))), block(('mya', 'a', None), say_(qq(('elem', 'a', 0)))))
    fault('last-element-of-an-empty-array', block(mya('a', 1), say_(qq(('elem', 'a', -1)))), block(('mya', 'a', None), say_(qq(('elem', 'a', -1)))))
    fault('element-by-a-scalar-past-the-end', *both(lambda: qq('<', ('elem', 'a', D('i')), '>'), [a3(), ('my', 'i', 2)], [a3(), ('my', 'i', 3)]))
    fault('slice-past-the-end', block(a3(), say_(qq(('slice', 'a', [0, 2])))), block(a3(), say_(qq(('slice', 'a', [0, 3])))))
    fault('slice-range-past-the-end', block(a3(), say_(qq(('slice', 'a', [('..', 1, 2)])))), block(a3(), say_(qq(('slice', 'a', [('..', 1, 3)])))))
    fault('slice-range-before-the-start', block(a3(), say_(qq(('slice', 'a', [('..', -3, -1)])))), block(a3(), say_(qq(('slice', 'a', [('..', -4, -3)])))))
    # D36: a whole Num from 10^15 is no string.
    fault('whole-num', *both(lambda: qq(D('n')), [('my', 'n', 999999999999999.0)], [('my', 'n', 1e15)]))
    fault('whole-num-after-text', *both(lambda: qq('n=', B('n'), '.'), [('my', 'n', 2.0**53)], [('my', 'n', 2.0**53 - 1)]))
    fault('whole-num-in-an-array', *both(lambda: qq(('@', 'a')), [mya('a', 1, 0.5)], [mya('a', 1, 1e15)]))
    fault('whole-num-element', *both(lambda: qq(('elem', 'a', 0)), [mya('a', 1e16)], [mya('a', 1e15)]))
    fault('whole-num-in-a-slice', *both(lambda: qq(('slice', 'a', [0, 1])), [mya('a', 1, 1e21)], [mya('a', 1, 1e15)]))
    # An index held in a scalar: a whole number, or a fault.
    fault('index-undef', *both(lambda: qq(('elem', 'a', D('i'))), [a3(), ('my', 'i', 0)], [a3(), ('my', 'i', None)]))
    fault('index-not-a-number', *both(lambda: qq(('elem', 'a', D('i'))), [a3(), ('my', 'i', '1')], [a3(), ('my', 'i', 'one')]))
    fault('index-too-large', *both(lambda: qq(('elem', 'a', D('i')), '|'), [a3(), ('my', 'i', -1.5)], [a3(), ('my', 'i', 1e30)]))
    fault('slice-index-not-a-number', *both(lambda: qq(('slice', 'a', [0, D('i')])), [a3(), ('my', 'i', ' 2 ')], [a3(), ('my', 'i', '')]))
    fault('slice-range-end-a-string', *both(lambda: qq(('slice', 'a', [('..', 0, D('i'))])), [a3(), ('my', 'i', 2)], [a3(), ('my', 'i', '2')]))
    # The string is a Str: where a number is wanted it has to be one.
    fault('not-a-numeric-string', *both(lambda: ('+', qq(D('p'), D('q')), 1), [('my', 'p', 1), ('my', 'q', 2)], [('my', 'p', 1), ('my', 'q', 'a')]))
    fault('false-is-the-empty-string', *both(lambda: ('+', qq(D('t')), 1), [('my', 't', TRUE)], [('my', 't', FALSE)]))
    # In a loop's list the fault is the string's (T209), and in a block.
    fault('element-past-the-end-in-a-loop-list', block(a3(), over('v', [qq(('elem', 'a', 2))], say_(D('v')))), block(a3(), over('v', [qq(('elem', 'a', 3))], say_(D('v')))))
    fault('undef-it-in-a-map-block', block(mya('a', 1, 2), ('mya', 'r', [mp([A('a')], qq(IT, '-'))])), block(mya('a', 1, UNDEF), ('mya', 'r', [mp([A('a')], qq(IT, '-'))])))
    fault('undef-in-a-sort-block', block(mya('a', 2, 1), ('mya', 'r', [srt([A('a')], ('cmp', qq(VA), qq(VB)))])),
          block(mya('a', 2, UNDEF), ('mya', 'r', [srt([A('a')], ('cmp', qq(VA), qq(VB)))])))
    fault('undef-under-a-for-modifier', block(mya('a', 1, 2), formod(say_(qq('<', IT, '>')), A('a'))), block(mya('a', 1, UNDEF), formod(say_(qq('<', IT, '>')), A('a'))))
    fault('undef-argument', say_(ucall('f', qq(('@', 'a')))), say_(ucall('f', qq(('elem', 'a', 5)))), [mya('a', 1, 2), sub('f', [req('s')], returns(D('s')))])
    fault('undef-returned', say_(ucall('f', 1)), say_(ucall('f', UNDEF)), [sub('f', [req('s')], returns(qq('<', D('s'), '>')))])
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/interp.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/interp.py {n} > t/{n}-{name}.expected\n'
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
    model = ['model: t/models/interp.py']
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
    it.lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

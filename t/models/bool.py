#!/usr/bin/env python3
"""t/300 to t/359: booleans, undef, comparison and logic (step 4; D47 to
D51).

The definition, which is all this file knows of the language beyond
t/models/str.py and num.py (strings and numbers, which it imports). Two
more kinds of value: undef, and the booleans true and false.

  as a number   a boolean is the Int 1 or 0; an undef is a fault, `undef
                where a number is wanted`
  as a string   a boolean is `1` or the empty string; an undef is a
                fault, `undef where a string is wanted`. Printing wants a
                string. `length` of an undef is undef.
  truth         false: undef, false, a number that is zero, the empty
                string, the string `0`. Everything else is true.

  == != < <= > >=   both operands as numbers (str.py's rule for a string);
                    both integral (an Int, or a whole Num below 2^53): the
                    whole numbers compared; otherwise the doubles. A
                    boolean.
  <=>               the same comparison: the Int -1, 0 or 1
  eq ne lt le gt ge both operands as strings, compared character by
                    character. A boolean.
  cmp               the Int -1, 0 or 1
  ! x, not x        the boolean that x's truth isn't
  a && b, a and b   a if a is false, otherwise b; b isn't worked out
                    unless it is wanted
  a || b, a or b    a if a is true, otherwise b
  a // b            a unless a is undef, otherwise b
  a xor b           both worked out; a boolean
  c ? a : b         one branch worked out
  defined x         a boolean: whether x isn't undef

Operands are worked out left before right, and made numbers or strings
in that order.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

In a test every operand that isn't a literal is in brackets, an undef
too, `(undef)`: how the operators group is for the hand tests (t/360 on),
whose answers are perl's.

300 is `<=>` over numbers and strings at the edges of D35 and D40, and
301 the six that give booleans. 302 is `cmp`, and 303 the six. 304 is
truth: each value under `!`, `not`, `? :`, `&&`, `||`, `//`, `defined`.
305 is what the logical operators give, over pairs. 306 is a boolean
wherever a number or a string is wanted, and 307 what is not worked out.
320 on each fault once, the line before the fault being a near thing
that doesn't.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/bool.py --program 300 > t/300-compare.pl
    python3 t/models/bool.py 300 > t/300-compare.expected
    python3 t/models/bool.py --program 301 > t/301-compare-booleans.pl
    python3 t/models/bool.py 301 > t/301-compare-booleans.expected
    python3 t/models/bool.py --program 302 > t/302-compare-strings.pl
    python3 t/models/bool.py 302 > t/302-compare-strings.expected
    python3 t/models/bool.py --program 303 > t/303-compare-strings-booleans.pl
    python3 t/models/bool.py 303 > t/303-compare-strings-booleans.expected
    python3 t/models/bool.py --program 304 > t/304-truth.pl
    python3 t/models/bool.py 304 > t/304-truth.expected
    python3 t/models/bool.py --program 305 > t/305-logic.pl
    python3 t/models/bool.py 305 > t/305-logic.expected
    python3 t/models/bool.py --program 306 > t/306-boolean-as-value.pl
    python3 t/models/bool.py 306 > t/306-boolean-as-value.expected
    python3 t/models/bool.py --program 307 > t/307-not-worked-out.pl
    python3 t/models/bool.py 307 > t/307-not-worked-out.expected
    python3 t/models/bool.py --program 320 > t/320-undef-add-left.pl
    python3 t/models/bool.py 320 > t/320-undef-add-left.expected
    python3 t/models/bool.py --program 321 > t/321-undef-add-right.pl
    python3 t/models/bool.py 321 > t/321-undef-add-right.expected
    python3 t/models/bool.py --program 322 > t/322-undef-mul.pl
    python3 t/models/bool.py 322 > t/322-undef-mul.expected
    python3 t/models/bool.py --program 323 > t/323-undef-pow.pl
    python3 t/models/bool.py 323 > t/323-undef-pow.expected
    python3 t/models/bool.py --program 324 > t/324-undef-mod.pl
    python3 t/models/bool.py 324 > t/324-undef-mod.expected
    python3 t/models/bool.py --program 325 > t/325-undef-neg.pl
    python3 t/models/bool.py 325 > t/325-undef-neg.expected
    python3 t/models/bool.py --program 326 > t/326-undef-compare-left.pl
    python3 t/models/bool.py 326 > t/326-undef-compare-left.expected
    python3 t/models/bool.py --program 327 > t/327-undef-compare-right.pl
    python3 t/models/bool.py 327 > t/327-undef-compare-right.expected
    python3 t/models/bool.py --program 328 > t/328-undef-less.pl
    python3 t/models/bool.py 328 > t/328-undef-less.expected
    python3 t/models/bool.py --program 329 > t/329-undef-repeat-count.pl
    python3 t/models/bool.py 329 > t/329-undef-repeat-count.expected
    python3 t/models/bool.py --program 330 > t/330-undef-chr.pl
    python3 t/models/bool.py 330 > t/330-undef-chr.expected
    python3 t/models/bool.py --program 331 > t/331-undef-substr-position.pl
    python3 t/models/bool.py 331 > t/331-undef-substr-position.expected
    python3 t/models/bool.py --program 332 > t/332-undef-substr-length.pl
    python3 t/models/bool.py 332 > t/332-undef-substr-length.expected
    python3 t/models/bool.py --program 333 > t/333-undef-index-position.pl
    python3 t/models/bool.py 333 > t/333-undef-index-position.expected
    python3 t/models/bool.py --program 334 > t/334-undef-concat-left.pl
    python3 t/models/bool.py 334 > t/334-undef-concat-left.expected
    python3 t/models/bool.py --program 335 > t/335-undef-concat-right.pl
    python3 t/models/bool.py 335 > t/335-undef-concat-right.expected
    python3 t/models/bool.py --program 336 > t/336-undef-repeat.pl
    python3 t/models/bool.py 336 > t/336-undef-repeat.expected
    python3 t/models/bool.py --program 337 > t/337-undef-say.pl
    python3 t/models/bool.py 337 > t/337-undef-say.expected
    python3 t/models/bool.py --program 338 > t/338-undef-uc.pl
    python3 t/models/bool.py 338 > t/338-undef-uc.expected
    python3 t/models/bool.py --program 339 > t/339-undef-ord.pl
    python3 t/models/bool.py 339 > t/339-undef-ord.expected
    python3 t/models/bool.py --program 340 > t/340-undef-substr.pl
    python3 t/models/bool.py 340 > t/340-undef-substr.expected
    python3 t/models/bool.py --program 341 > t/341-undef-index.pl
    python3 t/models/bool.py 341 > t/341-undef-index.expected
    python3 t/models/bool.py --program 342 > t/342-undef-index-piece.pl
    python3 t/models/bool.py 342 > t/342-undef-index-piece.expected
    python3 t/models/bool.py --program 343 > t/343-undef-eq.pl
    python3 t/models/bool.py 343 > t/343-undef-eq.expected
    python3 t/models/bool.py --program 344 > t/344-undef-cmp.pl
    python3 t/models/bool.py 344 > t/344-undef-cmp.expected
    python3 t/models/bool.py --program 345 > t/345-undef-lt.pl
    python3 t/models/bool.py 345 > t/345-undef-lt.expected
    python3 t/models/bool.py --program 346 > t/346-undef-from-and.pl
    python3 t/models/bool.py 346 > t/346-undef-from-and.expected
    python3 t/models/bool.py --program 347 > t/347-undef-from-ternary.pl
    python3 t/models/bool.py 347 > t/347-undef-from-ternary.expected
    python3 t/models/bool.py --program 348 > t/348-undef-length.pl
    python3 t/models/bool.py 348 > t/348-undef-length.expected
    python3 t/models/bool.py --program 349 > t/349-undef-from-or.pl
    python3 t/models/bool.py 349 > t/349-undef-from-or.expected
    python3 t/models/bool.py --program 350 > t/350-compare-not-numeric.pl
    python3 t/models/bool.py 350 > t/350-compare-not-numeric.expected
    python3 t/models/bool.py --program 351 > t/351-compare-not-numeric-right.pl
    python3 t/models/bool.py 351 > t/351-compare-not-numeric-right.expected
    python3 t/models/bool.py --program 352 > t/352-compare-exponent.pl
    python3 t/models/bool.py 352 > t/352-compare-exponent.expected
    python3 t/models/bool.py --program 353 > t/353-compare-string-overflow.pl
    python3 t/models/bool.py 353 > t/353-compare-string-overflow.expected
    python3 t/models/bool.py --program 354 > t/354-compare-whole-float.pl
    python3 t/models/bool.py 354 > t/354-compare-whole-float.expected
    python3 t/models/bool.py --program 355 > t/355-compare-whole-float-right.pl
    python3 t/models/bool.py 355 > t/355-compare-whole-float-right.expected
    python3 t/models/bool.py --program 356 > t/356-compare-fault-order.pl
    python3 t/models/bool.py 356 > t/356-compare-fault-order.expected
    python3 t/models/bool.py --program 357 > t/357-compare-strings-fault-order.pl
    python3 t/models/bool.py 357 > t/357-compare-strings-fault-order.expected
    python3 t/models/bool.py --program 358 > t/358-xor-works-both-out.pl
    python3 t/models/bool.py 358 > t/358-xor-works-both-out.expected
    python3 t/models/bool.py --program 359 > t/359-ternary-test-faults.pl
    python3 t/models/bool.py 359 > t/359-ternary-test-faults.expected
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import num
import str as strings
from num import Fault, MIN, MAX

class Undef:
    pass
UNDEF = Undef()

class Bool:
    def __init__(self, truth):
        self.truth = truth
TRUE, FALSE = Bool(True), Bool(False)

def boolean(truth):
    return TRUE if truth else FALSE

UNDEF_NUMBER = 'undef where a number is wanted'
UNDEF_STRING = 'undef where a string is wanted'

def number_of(v):
    """A value where a number is wanted, as str.py takes one: an Int, a
    Num, or a string it will read."""
    if v is UNDEF:
        raise Fault(UNDEF_NUMBER)
    return int(v.truth) if isinstance(v, Bool) else v

def string_of(v):
    """A value where a string is wanted, as a string."""
    if v is UNDEF:
        raise Fault(UNDEF_STRING)
    return ('1' if v.truth else '') if isinstance(v, Bool) else strings.to_str(v)

def truth(v):
    if v is UNDEF:
        return False
    if isinstance(v, Bool):
        return v.truth
    return v not in ('', '0') if strings.is_str(v) else v != 0

def compare_numbers(a, b):
    p, _ = strings.as_number(number_of(a))      # the left operand first
    q, _ = strings.as_number(number_of(b))
    x, y = num.integral(p), num.integral(q)
    if x is None or y is None:
        x, y = float(p), float(q)
    return (x > y) - (x < y)

def compare_strings(a, b):
    s = string_of(a)
    t = string_of(b)
    return (s > t) - (s < t)

TESTS = {'==': lambda c: c == 0, '!=': lambda c: c != 0, '<': lambda c: c < 0, '<=': lambda c: c <= 0,
         '>': lambda c: c > 0, '>=': lambda c: c >= 0}
WORDS = {'eq': '==', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>='}
ARITHMETIC = ('+', '-', '*', '/', '%', '**')

def arithmetic(op, a, b):
    x = number_of(a)
    strings.as_number(x)        # its own fault, before the right operand's
    return strings.arith(op, x, number_of(b))

def call(name, args):
    if name == 'defined':
        return boolean(args[0] is not UNDEF)
    if name == 'length':
        return UNDEF if args[0] is UNDEF else len(string_of(args[0]))
    if name in ('uc', 'lc', 'ord'):
        return strings.BUILTINS[name](string_of(args[0]))
    if name == 'chr':
        return strings.chr_(number_of(args[0]))
    if name == 'substr':
        s = string_of(args[0])
        rest = []
        for a in args[1:]:
            rest.append(number_of(a))
            strings.whole(rest[-1])
        return strings.substr(s, *rest)
    s = string_of(args[0])
    t = string_of(args[1])
    return strings.index(s, t, *[number_of(a) for a in args[2:]])

# An expression is a value; ('!', e), ('not', e), ('-', e), ('+', e);
# (op, left, right); ('?:', test, then, else); or ('call', name, [args]).
def value(e):
    if not isinstance(e, tuple):
        return e
    if e[0] == 'call':
        return call(e[1], [value(a) for a in e[2]])
    if e[0] == '?:':
        return value(e[2]) if truth(value(e[1])) else value(e[3])
    if len(e) == 2:
        v = value(e[1])
        if e[0] in ('!', 'not'):
            return boolean(not truth(v))
        return v if e[0] == '+' else strings.negate(number_of(v))
    op, left, right = e
    a = value(left)
    if op in ('&&', 'and'):
        return value(right) if truth(a) else a
    if op in ('||', 'or'):
        return a if truth(a) else value(right)
    if op == '//':
        return value(right) if a is UNDEF else a
    b = value(right)
    if op == 'xor':
        return boolean(truth(a) != truth(b))
    if op in TESTS:
        return boolean(TESTS[op](compare_numbers(a, b)))
    if op in WORDS:
        return boolean(TESTS[WORDS[op]](compare_strings(a, b)))
    if op == '<=>':
        return compare_numbers(a, b)
    if op == 'cmp':
        return compare_strings(a, b)
    if op == '.':
        s = string_of(a)
        return s + string_of(b)
    if op == 'x':
        return strings.repeat(string_of(a), number_of(b))
    return arithmetic(op, a, b)

def printed(v):
    """What `say` prints for a value, less the newline, or the fault."""
    return strings.printed(string_of(v), True)

def answers(e):
    """Whether an expression has an answer that prints."""
    try:
        printed(value(e))
        return True
    except Fault:
        return False

def text(e, top=True):
    """The expression as source: whatever isn't a literal in brackets."""
    if e is UNDEF:
        return '(undef)'
    if isinstance(e, Bool):
        return 'true' if e.truth else 'false'
    if not isinstance(e, tuple):
        return strings.text(e, top)
    if e[0] == 'call':
        return f'{e[1]}({", ".join(text(a) for a in e[2])})'
    if e[0] == '?:':
        s = f'{text(e[1], False)} ? {text(e[2], False)} : {text(e[3], False)}'
    elif len(e) == 2:
        s = f'{e[0]}{" " if e[0] == "not" else ""}{text(e[1], False)}'
    else:
        s = f'{text(e[1], False)} {e[0]} {text(e[2], False)}'
    return s if top else f'({s})'

# ---- the values

# Numbers and numeric strings at the edges: zero of each kind; small; on
# each side of 2^53, where a double stops holding every whole number, and
# two that differ and share a double; the ends of the Ints, and floats
# beside them; a string of each class of D40.
NUMBERS = [0, 1, -1, 2, 3, 10, 2**53 - 1, 2**53, 2**53 + 1, 2**53 + 2, 2**62, MAX - 1, MAX, MIN + 1, MIN,
           0.0, -0.0, 0.5, 1.0, 1.5, -2.5, 3.0, 1e15, 2.0**53 - 1, 2.0**53, 2.0**53 + 2, 2.0**63, -(2.0**63), 1e19, 1e300, 5e-324]
STRINGS = ['0', '1', '-1', '3', '10', ' 12 ', '012', '-0', '9007199254740992', '9007199254740993', '9223372036854775807',
           '3.0', '0.0', '-0.0', '1.5', '.5', '9007199254740992.0', '9007199254740993.0', '1e3', '1.5e1', '1e-3', '0e0']
BOOLS = [TRUE, FALSE]
# Values of every kind, for truth and the string comparisons.
TEXTS = ['', '0', '00', '0.0', ' ', '0\n', '0E0', '-0', 'a', 'abc', 'abd', 'ab', 'B', '1', '10', '9', '1.0', '\x00', 'a\x00',
         '\xe9', '\xff', 'Ā', '￿', '\U00010000', 'true', 'false']
VALUES = [0, 1, -1, 10, 9, MAX, 0.0, -0.0, 0.5, 1.0, 1.5, -2.5, 1e21, 5e-324, 1e-5, 0.1 + 0.2, 0.3, 999999999999999.0, 2.0**53]

def bracketed(e):
    return ('.', ('.', '[', e), ']')

def shown(e):
    """An expression whose value may be an undef or a boolean, as a line
    that says which: `[...]`, or `undef`."""
    return ('?:', ('call', 'defined', [e]), bracketed(e), 'undef')

def same(number):
    numeric = NUMBERS + STRINGS + BOOLS
    if number == '300':
        return 'compare', [('<=>', a, b) for a in numeric for b in numeric]
    if number == '301':
        pairs = [(a, b) for a in numeric for b in numeric]
        return 'compare-booleans', [bracketed((op, a, b)) for n, op in enumerate(TESTS) for a, b in pairs[n::7]]
    every = TEXTS + VALUES + BOOLS
    if number == '302':
        return 'compare-strings', [('cmp', a, b) for a in every for b in every]
    if number == '303':
        pairs = [(a, b) for a in every for b in every]
        return 'compare-strings-booleans', [bracketed((op, a, b)) for n, op in enumerate(WORDS) for a, b in pairs[n::5]]
    every = every + NUMBERS[:14] + STRINGS + [UNDEF]
    if number == '304':
        out = []
        for v in every:
            out += [bracketed(('!', v)), bracketed(('not', v)), ('?:', v, 't', 'f'), shown(('&&', v, 't')), shown(('||', v, 'f')),
                    shown(('//', v, 'u')), bracketed(('call', 'defined', [v])), bracketed(('!', ('!', v))), shown(('and', v, 't')),
                    shown(('or', v, 'f')), bracketed(('xor', v, 1)), bracketed(('xor', 0, v))]
        return 'truth', out
    some = ['', '0', 'a', '0.0', 0, 1, 2, 0.0, 0.5, TRUE, FALSE, UNDEF, '3.0', 2**53]
    if number == '305':
        out = [shown((op, a, b)) for op in ('&&', '||', '//', 'and', 'or') for a in some for b in some]
        out += [bracketed(('xor', a, b)) for a in some for b in some]
        out += [shown(('?:', c, a, b)) for c in some for a in some[::3] for b in some[1::4]]
        # What comes back is the operand itself, and behaves as it would.
        out += [('+', ('||', 0, '3.0'), 1), ('.', ('&&', 1, 2.50), ''), ('+', ('//', UNDEF, '12'), 1), bracketed(('x', ('||', '', 'ab'), ('&&', 1, 2))),
                ('call', 'length', [('||', 0, 1000.0)]), ('+', ('?:', 1, '1e3', 0), 1), ('==', ('&&', 1, '1.0'), 1), ('eq', ('&&', 1, '1.0'), 1)]
        return 'logic', out
    if number == '306':
        out = []
        for b in BOOLS:
            for n in [0, 1, 2, -1, 0.5, 1.0, 10**16, 2**53, MAX, 2.0**53, 1e16, '3.0', '12', TRUE, FALSE]:
                out += [(op, b, n) for op in ARITHMETIC] + [(op, n, b) for op in ARITHMETIC]
            out += [bracketed(('.', b, 'x')), bracketed(('.', 'x', b)), bracketed(('.', b, b)), ('-', b), bracketed(('+', b)), bracketed(('x', 'ab', b)),
                    bracketed(('x', b, 3)), ('call', 'length', [b]), bracketed(('call', 'uc', [b])), ('call', 'ord', [b]),
                    ('call', 'ord', [('call', 'chr', [b])]), bracketed(('call', 'substr', ['abc', b])), bracketed(('call', 'substr', ['abc', 0, b])),
                    bracketed(('call', 'substr', [b, 0])), ('call', 'index', ['a1b', b]), ('call', 'index', ['abab', 'b', b]),
                    bracketed(('call', 'lc', [('.', b, 'A')])), bracketed(b), ('==', b, 1), bracketed(('eq', b, '')), bracketed(('eq', b, '0')),
                    ('==', b, 0), bracketed(('==', b, '1.0')), ('<=>', b, 0.5), ('cmp', b, '0')]
        return 'boolean-as-value', out
    if number == '307':
        bad = [('/', 1, 0), ('+', 'abc', 1), ('.', 'a', UNDEF), ('x', 'a', -1), ('call', 'chr', [-1]), ('call', 'substr', ['abc', 9])]
        out = []
        for f in bad:
            out += [('||', 1, f), shown(('&&', 0, f)), ('//', 0, f), ('?:', 1, 'then', f), ('?:', 0, f, 'else'), ('or', 'a', f),
                    shown(('and', '', f)), ('?:', ('||', 1, f), ('&&', 2, 3), f), ('||', ('&&', 0, f), 'x')]
        return 'not-worked-out', out
    raise KeyError(number)

SAME = {'300': 'compare', '301': 'compare-booleans', '302': 'compare-strings', '303': 'compare-strings-booleans', '304': 'truth',
        '305': 'logic', '306': 'boolean-as-value', '307': 'not-worked-out'}

def f(name, args):
    return ('call', name, list(args))

# number: (name, a near expression that prints, the one that faults)
FAULTS = {
    # An undef where a number is wanted: each side of each kind of operator.
    '320': ('undef-add-left', ('+', ('//', UNDEF, 1), 1), ('+', UNDEF, 1)),
    '321': ('undef-add-right', ('+', 1, ('||', UNDEF, 1)), ('+', 1, UNDEF)),
    '322': ('undef-mul', ('*', FALSE, 2), ('*', UNDEF, 2)),
    '323': ('undef-pow', ('**', 2, FALSE), ('**', 2, UNDEF)),
    '324': ('undef-mod', ('%', FALSE, 2), ('%', UNDEF, 2)),
    '325': ('undef-neg', ('-', FALSE), ('-', UNDEF)),
    '326': ('undef-compare-left', bracketed(('==', FALSE, 1)), ('==', UNDEF, 1)),
    '327': ('undef-compare-right', ('<=>', 1, FALSE), ('<=>', 1, UNDEF)),
    '328': ('undef-less', ('<', FALSE, 1), ('<', UNDEF, 1)),
    '329': ('undef-repeat-count', bracketed(('x', 'a', FALSE)), ('x', 'a', UNDEF)),
    '330': ('undef-chr', f('ord', [f('chr', [FALSE])]), f('chr', [UNDEF])),
    '331': ('undef-substr-position', f('substr', ['abc', FALSE]), f('substr', ['abc', UNDEF])),
    '332': ('undef-substr-length', bracketed(f('substr', ['abc', 0, FALSE])), f('substr', ['abc', 0, UNDEF])),
    '333': ('undef-index-position', f('index', ['abc', 'c', FALSE]), f('index', ['abc', 'c', UNDEF])),
    # And where a string is.
    '334': ('undef-concat-left', bracketed(('.', FALSE, 'a')), ('.', UNDEF, 'a')),
    '335': ('undef-concat-right', bracketed(('.', 'a', FALSE)), ('.', 'a', UNDEF)),
    # (In brackets of its own an undef repeated would be a list, to perl: T101.)
    '336': ('undef-repeat', bracketed(('x', FALSE, 2)), bracketed(('x', UNDEF, 2))),
    '337': ('undef-say', bracketed(FALSE), UNDEF),
    '338': ('undef-uc', bracketed(f('uc', [FALSE])), f('uc', [UNDEF])),
    '339': ('undef-ord', f('ord', [FALSE]), f('ord', [UNDEF])),
    '340': ('undef-substr', bracketed(f('substr', [FALSE, 0])), f('substr', [UNDEF, 0])),
    '341': ('undef-index', f('index', [FALSE, '']), f('index', [UNDEF, ''])),
    '342': ('undef-index-piece', f('index', ['abc', FALSE]), f('index', ['abc', UNDEF])),
    '343': ('undef-eq', ('eq', FALSE, ''), ('eq', UNDEF, '')),
    '344': ('undef-cmp', ('cmp', '', FALSE), ('cmp', '', UNDEF)),
    '345': ('undef-lt', ('lt', FALSE, 'a'), ('lt', UNDEF, 'a')),
    # An undef that an operator gave, printed; and the length of one.
    '346': ('undef-from-and', shown(('&&', UNDEF, 1)), ('&&', UNDEF, 1)),
    '347': ('undef-from-ternary', ('?:', 0, UNDEF, 'else'), ('?:', 1, UNDEF, 'else')),
    '348': ('undef-length', shown(f('length', [UNDEF])), f('length', [UNDEF])),
    '349': ('undef-from-or', ('||', FALSE, 'x'), bracketed(('||', FALSE, UNDEF))),
    # A comparison's operands are made numbers, or strings, as anywhere.
    '350': ('compare-not-numeric', bracketed(('==', FALSE, 0)), ('==', '', 0)),
    '351': ('compare-not-numeric-right', ('<', 1, '2'), ('<', 1, 'abc')),
    '352': ('compare-exponent', ('<=>', '1e15', 1), ('<=>', '1e16', 1)),
    '353': ('compare-string-overflow', ('==', '9223372036854775807', 1), ('==', '9223372036854775808', 1)),
    '354': ('compare-whole-float', ('eq', 999999999999999.0, 'x'), ('eq', 1e15, 'x')),
    '355': ('compare-whole-float-right', ('cmp', 'x', 2.0**53), ('cmp', 'x', 2.0**53 - 1)),
    # The left operand's fault is the one that happens.
    '356': ('compare-fault-order', ('==', '1', '1'), ('==', 'abc', UNDEF)),
    '357': ('compare-strings-fault-order', ('eq', 1e14, FALSE), ('eq', 1e15, UNDEF)),
    '358': ('xor-works-both-out', bracketed(('xor', 1, ('/', 1, 1))), ('xor', 1, ('/', 1, 0))),
    '359': ('ternary-test-faults', ('?:', ('==', '0', 0), 'a', 'b'), ('?:', ('==', 'zero', 0), 'a', 'b')),
}

def commands():
    return ''.join(f'    python3 t/models/bool.py --program {n} > t/{n}-{FAULTS[n][0]}.pl\n'
                   f'    python3 t/models/bool.py {n} > t/{n}-{FAULTS[n][0]}.expected\n' for n in sorted(FAULTS))

def program(statements, header):
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(f'say({text(e)});\n' for e in statements)

def main(argv):
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    # The list in the docstring is what t/checks.py reads, so it has to be
    # the whole list.
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/bool.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/bool.py']
    if number in SAME:
        name, lines = same(number)
        assert name == SAME[number]
        lines = [e for e in lines if answers(e)]
        if want_program:
            out.write(program(lines, model).encode())
        else:
            out.write(''.join(f'{printed(value(e))}\n' for e in lines).encode())
        return
    name, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    lines = [1, near, far, 2]
    if want_program:
        out.write(program(lines, header).encode())
        return
    result = ''
    for n, e in enumerate(lines):
        try:
            result += printed(value(e)) + '\n'
        except Fault as fault:
            result += f'fault: {fault} at {path} line {len(header) + 2 + n + 1}.\nexit: 1\n'
            break
    assert 'fault:' in result and result.count('\n') == 4, (number, result)
    out.write(result.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

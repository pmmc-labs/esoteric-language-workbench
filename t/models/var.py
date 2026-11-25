#!/usr/bin/env python3
"""t/500 to t/549: variables, assignment, blocks and `if` (step 5; D52 to
D56).

The definition, which is all this file knows of the language beyond
t/models/bool.py, str.py and num.py (values and operators, which it
imports).

  my $x;  my $x = E;   a variable, undef until given a value, seen from
                       the next statement to the end of its block
  $x = E               E's value is put in $x
  $x OP= E             $x = $x OP E, for + - * / % ** . x; an undef in
                       $x is 0 for += and -=, and the empty string for
                       .=, and a fault for the others
  $x ||= E             $x = E if $x is false; &&= if true; //= if undef.
                       E is worked out only then.
  ++$x, $x++, --$x, $x--   by what $x holds (`step`, below, is D52's
                       table). $x++ is worth what $x was (0 for an
                       undef), and $x-- likewise (an undef for an undef).
  { ... }              a block: a scope
  if (C) {...} elsif (C) {...} else {...};  unless (C) {...}
  S if C;  S unless C;

An operand that is the variable itself is read when its operator runs
(D14, D56): `$x`, `+$x`, an assignment, `++$x`, and whichever operand
`||`, `&&`, `//`, `and`, `or` and `? :` give. So an expression is worked
out to a place or to a value, and a place is read late: `ev` and `get`.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

A test is a row of cases, each a block of its own, so that one case's
variables are not the next one's; a case that faults is left out of a
test of what prints, and the fault tests have one each. 500 is `++` and
`--` in each form over every kind of value; 501 the same after the
variable has been read some way first, which must change nothing; 502
the assigning operators; 503 what is read late and what is not; 504
`if`, `unless`, the modifiers and scopes. 520 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/var.py --program 500 > t/500-step.pl
    python3 t/models/var.py 500 > t/500-step.expected
    python3 t/models/var.py --program 501 > t/501-step-after-use.pl
    python3 t/models/var.py 501 > t/501-step-after-use.expected
    python3 t/models/var.py --program 502 > t/502-assigning.pl
    python3 t/models/var.py 502 > t/502-assigning.expected
    python3 t/models/var.py --program 503 > t/503-late-reads.pl
    python3 t/models/var.py 503 > t/503-late-reads.expected
    python3 t/models/var.py --program 504 > t/504-control.pl
    python3 t/models/var.py 504 > t/504-control.expected
    python3 t/models/var.py --program 520 > t/520-step-overflow.pl
    python3 t/models/var.py 520 > t/520-step-overflow.expected
    python3 t/models/var.py --program 521 > t/521-step-overflow-down.pl
    python3 t/models/var.py 521 > t/521-step-overflow-down.expected
    python3 t/models/var.py --program 522 > t/522-step-float-lost.pl
    python3 t/models/var.py 522 > t/522-step-float-lost.expected
    python3 t/models/var.py --program 523 > t/523-step-float-lost-down.pl
    python3 t/models/var.py 523 > t/523-step-float-lost-down.expected
    python3 t/models/var.py --program 524 > t/524-step-float-two.pl
    python3 t/models/var.py 524 > t/524-step-float-two.expected
    python3 t/models/var.py --program 525 > t/525-step-string.pl
    python3 t/models/var.py 525 > t/525-step-string.expected
    python3 t/models/var.py --program 526 > t/526-step-string-down.pl
    python3 t/models/var.py 526 > t/526-step-string-down.expected
    python3 t/models/var.py --program 527 > t/527-step-string-empty.pl
    python3 t/models/var.py 527 > t/527-step-string-empty.expected
    python3 t/models/var.py --program 528 > t/528-step-string-zero.pl
    python3 t/models/var.py 528 > t/528-step-string-zero.expected
    python3 t/models/var.py --program 529 > t/529-step-string-large.pl
    python3 t/models/var.py 529 > t/529-step-string-large.expected
    python3 t/models/var.py --program 530 > t/530-step-string-large-down.pl
    python3 t/models/var.py 530 > t/530-step-string-large-down.expected
    python3 t/models/var.py --program 531 > t/531-step-float-down-is-a-float.pl
    python3 t/models/var.py 531 > t/531-step-float-down-is-a-float.expected
    python3 t/models/var.py --program 532 > t/532-step-string-is-a-float.pl
    python3 t/models/var.py 532 > t/532-step-string-is-a-float.expected
    python3 t/models/var.py --program 533 > t/533-step-whole-float-printed.pl
    python3 t/models/var.py 533 > t/533-step-whole-float-printed.expected
    python3 t/models/var.py --program 534 > t/534-assign-undef-times.pl
    python3 t/models/var.py 534 > t/534-assign-undef-times.expected
    python3 t/models/var.py --program 535 > t/535-assign-undef-divide.pl
    python3 t/models/var.py 535 > t/535-assign-undef-divide.expected
    python3 t/models/var.py --program 536 > t/536-assign-undef-power.pl
    python3 t/models/var.py 536 > t/536-assign-undef-power.expected
    python3 t/models/var.py --program 537 > t/537-assign-undef-modulus.pl
    python3 t/models/var.py 537 > t/537-assign-undef-modulus.expected
    python3 t/models/var.py --program 538 > t/538-assign-undef-repeat.pl
    python3 t/models/var.py 538 > t/538-assign-undef-repeat.expected
    python3 t/models/var.py --program 539 > t/539-assign-undef-right.pl
    python3 t/models/var.py 539 > t/539-assign-undef-right.expected
    python3 t/models/var.py --program 540 > t/540-assign-fault.pl
    python3 t/models/var.py 540 > t/540-assign-fault.expected
    python3 t/models/var.py --program 541 > t/541-undef-variable.pl
    python3 t/models/var.py 541 > t/541-undef-variable.expected
    python3 t/models/var.py --program 542 > t/542-undef-variable-added.pl
    python3 t/models/var.py 542 > t/542-undef-variable-added.expected
    python3 t/models/var.py --program 543 > t/543-fault-in-branch.pl
    python3 t/models/var.py 543 > t/543-fault-in-branch.expected
    python3 t/models/var.py --program 544 > t/544-fault-under-modifier.pl
    python3 t/models/var.py 544 > t/544-fault-under-modifier.expected
    python3 t/models/var.py --program 545 > t/545-fault-in-condition.pl
    python3 t/models/var.py 545 > t/545-fault-in-condition.expected
    python3 t/models/var.py --program 546 > t/546-late-read-fault.pl
    python3 t/models/var.py 546 > t/546-late-read-fault.expected
    python3 t/models/var.py --program 550 > t/550-step-string-edge.pl
    python3 t/models/var.py 550 > t/550-step-string-edge.expected
    python3 t/models/var.py --program 551 > t/551-step-string-edge-up.pl
    python3 t/models/var.py 551 > t/551-step-string-edge-up.expected
    python3 t/models/var.py --program 552 > t/552-step-float-lost-tie.pl
    python3 t/models/var.py 552 > t/552-step-float-lost-tie.expected
    python3 t/models/var.py --program 553 > t/553-step-float-lost-negative.pl
    python3 t/models/var.py 553 > t/553-step-float-lost-negative.expected
    python3 t/models/var.py --program 554 > t/554-step-float-lost-negative-up.pl
    python3 t/models/var.py 554 > t/554-step-float-lost-negative-up.expected
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import num
import str as strings
import bool as logic
from num import Fault, MIN, MAX
from bool import UNDEF, TRUE, FALSE

STEP_ZERO = '++ on a string of digits that begins with a zero has two answers in perl'
STEP_STRING = '++ or -- on a string that is a whole number this large has two answers in perl'
STEP_FLOAT = '-- on a whole float that reaches 2^53 has two answers in perl'
STEP_LOST = 'a float too large to step by one'

def step(op, v):
    """What `++` or `--` leaves in a variable that holds v (D52)."""
    d = 1 if op == '++' else -1
    if v is UNDEF:
        return d
    if isinstance(v, logic.Bool):
        return int(v.truth) + d
    if strings.is_str(v):
        x = float(strings.as_number(v)[0])
        # Every double of 2^53 and up is whole.
        if abs(x) >= 2**53 or abs(x + d) >= 2**53:
            raise Fault(STEP_STRING)
        if d > 0 and len(v) > 1 and v[0] == '0' and all('0' <= c <= '9' for c in v):
            raise Fault(STEP_ZERO)
        return x + d
    if not num.is_num(v):
        return num.Int(v + d)
    whole = num.integral(v)
    if d > 0 and whole is not None:
        return whole + 1
    # Where perl warns `Lost precision`: by where the float is, whether
    # or not one more or less is another float (T130).
    if (v >= 2**53 or v < -(2**53)) if d > 0 else (v > 2**53 or v <= -(2**53)):
        raise Fault(STEP_LOST)
    if whole is not None and abs(whole - 1) >= 2**53:
        raise Fault(STEP_FLOAT)
    return v + d

class Place:
    """A variable: what an expression is worth when it is the variable
    itself."""
    def __init__(self):
        self.value = UNDEF

def get(r):
    return r.value if isinstance(r, Place) else r

LAZY = {'&&': True, 'and': True, '||': False, 'or': False}

# An expression is one of bool.py's, or ('$', name); ('set', op, name, e)
# for `$name op e` with op one of = += ...; ('step', op, before, name).
class Run:
    def __init__(self):
        self.scopes = [{}]
        self.out = ''

    def place(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise AssertionError(f'${name} is not declared')

    def ev(self, e):
        """A place or a value."""
        if not isinstance(e, tuple):
            return e
        kind = e[0]
        if kind == '$':
            return self.place(e[1])
        if kind == 'set':
            _, op, name, right = e
            p = self.place(name)
            if op in ('||=', '&&=', '//='):
                wanted = p.value is UNDEF if op == '//=' else logic.truth(p.value) == (op == '&&=')
                if wanted:
                    p.value = get(self.ev(right))
                return p
            r = self.ev(right)
            if op == '=':
                p.value = get(r)
                return p
            left = p.value          # read now, after the right side is worked out
            if left is UNDEF and op in ('+=', '-=', '.='):
                left = '' if op == '.=' else 0
            p.value = logic.value((op[:-1], left, get(r)))
            return p
        if kind == 'step':
            _, op, before, name = e
            p = self.place(name)
            old = p.value
            p.value = step(op, old)
            return p if before else 0 if old is UNDEF and op == '++' else old
        if kind == 'call':
            results = [self.ev(a) for a in e[2]]
            return logic.call(e[1], [get(r) for r in results])
        if kind == '?:':
            return self.ev(e[2]) if logic.truth(get(self.ev(e[1]))) else self.ev(e[3])
        if len(e) == 2:
            r = self.ev(e[1])
            return r if kind == '+' else logic.value((kind, get(r)))
        left = self.ev(e[1])
        if kind in LAZY:
            return self.ev(e[2]) if logic.truth(get(left)) == LAZY[kind] else left
        if kind == '//':
            return self.ev(e[2]) if get(left) is UNDEF else left
        right = self.ev(e[2])
        return logic.value((kind, get(left), get(right)))

    def block(self, statements):
        self.scopes.append({})
        for s in statements:
            self.run(s)
        self.scopes.pop()

    def run(self, s):
        self.at = id(s)         # the statement a fault would name (D34)
        kind = s[0]
        if kind == 'my':
            v = UNDEF if s[2] is None else get(self.ev(s[2]))
            self.scopes[-1][s[1]] = Place()
            self.scopes[-1][s[1]].value = v
        elif kind == 'say':
            self.out += logic.printed(get(self.ev(s[1]))) + '\n'
        elif kind == 'do':
            self.ev(s[1])
        elif kind == 'block':
            self.block(s[1])
        elif kind == 'if':
            for n, (test, body) in enumerate(s[1]):
                self.at = (id(s), n)
                if logic.truth(get(self.ev(test))):
                    return self.block(body)
            if s[2] is not None:
                self.block(s[2])
        elif kind == 'unless':
            if not logic.truth(get(self.ev(s[1]))):
                self.block(s[2])
        else:
            _, inner, word, test = s
            if logic.truth(get(self.ev(test))) == (word == 'if'):
                self.run(inner)

def text(e, top=True):
    """The expression as source: whatever isn't a literal or a variable in
    brackets."""
    if not isinstance(e, tuple):
        return logic.text(e, top)
    kind = e[0]
    if kind == '$':
        return '$' + e[1]
    if kind == 'call':
        return f'{e[1]}({", ".join(text(a) for a in e[2])})'
    if kind == 'set':
        s = f'${e[2]} {e[1]} {text(e[3], False)}'
    elif kind == 'step':
        s = f'{e[1]}${e[3]}' if e[2] else f'${e[3]}{e[1]}'
    elif kind == '?:':
        s = f'{text(e[1], False)} ? {text(e[2], False)} : {text(e[3], False)}'
    elif len(e) == 2:
        s = f'{kind}{" " if kind == "not" else ""}{text(e[1], False)}'
    else:
        s = f'{text(e[1], False)} {kind} {text(e[2], False)}'
    return s if top else f'({s})'

def source(s, depth=0):
    """A statement as lines of source."""
    pad = '    ' * depth
    kind = s[0]
    body = lambda statements: [line for t in statements for line in source(t, depth + 1)]
    if kind == 'my':
        return [f'{pad}my ${s[1]};' if s[2] is None else f'{pad}my ${s[1]} = {text(s[2])};']
    if kind == 'say':
        return [f'{pad}say({text(s[1])});']
    if kind == 'do':
        return [f'{pad}{text(s[1])};']
    if kind == 'block':
        return [pad + '{'] + body(s[1]) + [pad + '}']
    if kind == 'if':
        lines = []
        for n, (test, statements) in enumerate(s[1]):
            lines += [f'{pad}{"if" if n == 0 else "} elsif"} ({text(test)}) {{'] + body(statements)
        if s[2] is not None:
            lines += [pad + '} else {'] + body(s[2])
        return lines + [pad + '}']
    if kind == 'unless':
        return [f'{pad}unless ({text(s[1])}) {{'] + body(s[2]) + [pad + '}']
    return [source(s[1], depth)[0][:-1] + f' {s[2]} {text(s[3])};']

def output(statements):
    """What a program prints, and the fault that ended it or None, and
    the statement it was in."""
    r = Run()
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.at
    return r.out, None, None

def lines(statements, line, found):
    """The line each statement starts on, as `source` lays them out, into
    `found`; an `elsif`'s test is on the line that says `elsif`. Returns
    the line after the last."""
    for s in statements:
        found[id(s)] = line
        kind = s[0]
        if kind == 'block' or kind == 'unless':
            line = lines(s[-1], line + 1, found) + 1
        elif kind == 'if':
            for n, (test, body) in enumerate(s[1]):
                found[(id(s), n)] = line
                line = lines(body, line + 1, found)
            if s[2] is not None:
                line = lines(s[2], line + 1, found)
            line += 1
        else:
            if kind == 'mod':
                found[id(s[1])] = line
            line += 1
    return line

# ---- the cases

V = ('$', 'v')
def shown(e):
    return ('say', logic.shown(e))

# Every kind of value, at the edges of D52's table.
VALUES = [UNDEF, TRUE, FALSE, 0, 1, -1, 41, MAX - 1, MAX, MIN + 1, MIN, 2**53 - 1, 2**53, -(2**53),
          0.0, -0.0, 0.5, -0.5, 1.5, 3.0, -1.0, 999999999999998.0, 2.0**53 - 2, 2.0**53 - 1, 2.0**53, -(2.0**53) + 1, -(2.0**53), -(2.0**53) + 2, 1e16, -1e16, 1e300,
          '0', '1', '12', '-12', ' 12 ', '+12', '09', '009', '00', '0.0', '3.0', '1.5', '-0.5', '.5', '1e3', '1e-3', '9007199254740990',
          '9007199254740991', '9007199254740992', '-9007199254740992', '9223372036854775807', '999999999999999', '', 'ab', 'a9', 'zz', '12abc', '0x10']
FORMS = [('step', op, before, 'v') for op in ('++', '--') for before in (True, False)]
# Ways to read a variable that leave what it holds as it was.
USES = [('+', V, 0), ('.', V, ''), ('>', V, 0.5), ('-', V), ('*', V, 1.5), ('%', V, 7), ('call', 'length', [V]), ('==', V, 1), ('eq', V, 'a'), ('!', V),
        ('x', V, 1), ('call', 'defined', [V])]

def step_case(v, form, use=None):
    case = [('my', 'v', v)] + ([('my', 't', use)] if use is not None else []) + [('my', 'r', form), shown(V), shown(('$', 'r'))]
    # And once more: the kind of number the first step left shows in the second.
    return ('block', case + [('do', form), shown(V)])

def assigning_cases():
    lefts = [UNDEF, TRUE, 0, 5, MAX, 0.5, 3.0, 2.0**53, '', '12', '3.0', 'ab']
    rights = [0, 2, -1, 0.5, MAX, '3.0', 'x', UNDEF]
    out = []
    for op in ('+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//='):
        for a in lefts:
            for b in rights:
                out.append(('block', [('my', 'v', a), ('my', 'r', ('set', op, 'v', b)), shown(V), shown(('$', 'r'))]))
    # The four that the pairs above are thin on: every value under each.
    for op in ('+=', '-=', '.=', '//='):
        out += [('block', [('my', 'v', a), ('do', ('set', op, 'v', 1)), shown(V)]) for a in VALUES]
    return out

def late_cases():
    """Each: $v is 3, an expression that reads $v and then changes it."""
    change = [('set', '=', 'v', 5), ('set', '+=', 'v', 10), ('step', '++', True, 'v'), ('step', '--', False, 'v'), ('set', '.=', 'v', '0'), ('set', '||=', 'v', 9)]
    itself = [V, ('+', V), ('||', V, 0), ('&&', 1, V), ('//', V, 0), ('?:', 1, V, 0), ('?:', 0, 0, V), ('set', '=', 'v', 4), ('set', '+=', 'v', 1), ('set', '.=', 'v', '1'),
              ('step', '++', True, 'v'), ('step', '--', True, 'v'), ('or', V, 0), ('and', 1, V), ('||', 0, ('||', V, 1)), ('?:', V, ('&&', 2, V), 0)]
    values = [('step', '++', False, 'v'), ('step', '--', False, 'v'), ('-', V), ('!', V), ('.', V, ''), ('+', V, 0), ('*', V, 1), ('call', 'length', [V]),
              ('==', V, 3), ('x', V, 1), ('||', 0, ('+', V, 0)), ('?:', 1, ('-', V), 0)]
    out = []
    for first in itself + values:
        for c in change:
            # (No dot here: in a concatenation a later piece may not change
            # a variable an earlier piece reads, D57: perl joins a row of
            # dots as one operation, and reads every piece late.)
            for op in ('+', '-', '==', '<=>'):
                out.append(('block', [('my', 'v', 3), ('say', (op, first, c)), shown(V)]))
            # (In brackets of its own as say's argument, a repeated value
            # would be a list to perl: T101.)
            out.append(('block', [('my', 'v', 3), ('say', ('.', '', ('x', first, c))), shown(V)]))
    for c in change:
        out += [('block', [('my', 'v', 3), ('say', ('call', 'substr', ['abcdefghijklmnop', V, c])), shown(V)]),
                ('block', [('my', 'v', 3), ('say', ('call', 'index', ['abc3abc5abc13', V, c])), shown(V)]),
                ('block', [('my', 'v', 3), ('my', 'w', ('+', ('+', V, c), V)), shown(('$', 'w'))]),
                ('block', [('my', 'v', 3), ('do', ('set', '+=', 'v', c)), shown(V)]),
                ('block', [('my', 'v', 3), ('do', ('set', '=', 'v', ('+', ('step', '++', False, 'v'), ('step', '++', False, 'v')))), shown(V)]),
                ('block', [('my', 'v', 3), ('say', ('+', ('+', ('set', '=', 'v', 1), ('set', '=', 'v', 2)), V))]),
                ('block', [('my', 'v', 3), ('my', 'w', 4), ('say', ('+', ('?:', ('+', c, 0), V, ('$', 'w')), ('set', '=', 'w', 100)))])]
    return out

def control_cases():
    tests = [0, 1, '', '0', '0.0', 'a', 0.0, UNDEF, TRUE, FALSE, ('==', V, 1), ('<', V, 2), ('!', V), ('set', '+=', 'v', 1), ('step', '++', False, 'v'),
             ('set', '=', 'v', ('+', V, 0)), ('&&', V, ('set', '=', 'v', ('+', V, 6)))]
    out = []
    for start in (0, 1, 2):
        for t in tests:
            head = [('my', 'v', start)]
            out += [('block', head + [('if', [(t, [('say', 'then')])], None), shown(V)]),
                    ('block', head + [('if', [(t, [('say', 'then')])], [('say', 'else')]), shown(V)]),
                    ('block', head + [('if', [(0, [('say', 'first')]), (t, [('say', 'second')])], [('say', 'else')]), shown(V)]),
                    ('block', head + [('if', [(t, [('say', 'first')]), (1, [('say', 'second')])], None), shown(V)]),
                    ('block', head + [('unless', t, [('say', 'unless')]), shown(V)]),
                    ('block', head + [('mod', ('say', 'said'), 'if', t), shown(V)]),
                    ('block', head + [('mod', ('say', 'said'), 'unless', t), shown(V)]),
                    ('block', head + [('mod', ('do', ('set', '=', 'v', 50)), 'if', t), shown(V)]),
                    ('block', head + [('mod', ('do', ('step', '++', False, 'v')), 'unless', t), shown(V)])]
    # Scopes: an inner `my` hides the outer one until its block ends, and
    # its own right side is worked out before it exists (T58).
    out += [
        ('block', [('my', 'v', 1), ('block', [('my', 'v', 2), shown(V)]), shown(V)]),
        ('block', [('my', 'v', 1), ('block', [('my', 'v', ('+', V, 10)), shown(V), ('do', ('step', '++', False, 'v'))]), shown(V)]),
        ('block', [('my', 'v', 1), ('block', [('do', ('set', '=', 'v', 2)), ('my', 'v', 3), ('do', ('set', '=', 'v', 4)), shown(V)]), shown(V)]),
        ('block', [('my', 'v', 1), ('if', [(V, [('my', 'v', 'inner'), shown(V)])], None), shown(V)]),
        ('block', [('my', 'v', 1), ('if', [(0, []), (1, [('my', 'w', ('+', V, 1)), ('do', ('set', '=', 'v', ('$', 'w')))])], [('my', 'v', 9)]), shown(V)]),
        ('block', [('my', 'v', None), shown(V), ('do', ('set', '=', 'v', 'set')), shown(V)]),
        ('block', [('my', 'v', 1), ('my', 'w', V), ('do', ('step', '++', False, 'w')), shown(V), shown(('$', 'w'))]),
        ('block', [('my', 'v', 1), ('my', 'w', ('set', '=', 'v', 5)), ('do', ('step', '++', False, 'w')), shown(V), shown(('$', 'w'))]),
        ('block', [('my', 'v', 1), ('block', [('block', [('do', ('set', '+=', 'v', 1))])]), shown(V)]),
        ('block', [('my', 'v', 1), ('my', 'w', 2), ('do', ('set', '=', 'v', ('set', '=', 'w', 7))), shown(V), shown(('$', 'w'))]),
        ('block', [('my', 'v', 1), ('my', 'w', 2), ('do', ('set', '+=', 'v', ('set', '*=', 'w', 7))), shown(V), shown(('$', 'w'))]),
    ]
    return out

def same(number):
    if number == '500':
        return 'step', [step_case(v, f) for v in VALUES for f in FORMS]
    if number == '501':
        # Thinned, to keep the test to about three thousand statements: every
        # use meets every form, and every third value some of the uses.
        return 'step-after-use', [step_case(v, f, u) for n, v in enumerate(VALUES[::3]) for f in FORMS for u in USES[n % 3::3]]
    if number == '502':
        return 'assigning', assigning_cases()
    if number == '503':
        return 'late-reads', late_cases()
    if number == '504':
        return 'control', control_cases()
    raise KeyError(number)

SAME = {'500': 'step', '501': 'step-after-use', '502': 'assigning', '503': 'late-reads', '504': 'control'}

def case(v, *statements):
    return ('block', [('my', 'v', v)] + list(statements) + [shown(V)])

def stepped(op, before=False):
    return ('do', ('step', op, before, 'v'))

def quiet(v, statement):
    """A case whose answer is a whole float that can't be printed (D36)."""
    return ('block', [('my', 'v', v), statement, ('say', ('call', 'defined', [V]))])

# number: (name, a near case that prints, the one that faults)
FAULTS = {
    '520': ('step-overflow', case(MAX - 1, stepped('++')), case(MAX, stepped('++'))),
    '521': ('step-overflow-down', case(MIN + 1, stepped('--', True)), case(MIN, stepped('--', True))),
    '522': ('step-float-lost', quiet(-(2.0**53), stepped('++')), quiet(2.0**53, stepped('++'))),
    '523': ('step-float-lost-down', quiet(2.0**53, stepped('--')), quiet(2.0**53 + 2, stepped('--'))),
    '524': ('step-float-two', quiet(-(2.0**53) + 2, stepped('--')), quiet(-(2.0**53) + 1, stepped('--'))),
    '525': ('step-string', case('12', stepped('++')), case('ab', stepped('++'))),
    '526': ('step-string-down', case(' 12 ', stepped('--')), case('ab', stepped('--'))),
    '527': ('step-string-empty', case('0', stepped('++', True)), case('', stepped('++', True))),
    '528': ('step-string-zero', case('90', stepped('++')), case('09', stepped('++'))),
    '529': ('step-string-large', quiet('9007199254740990', stepped('++')), quiet('9007199254740991', stepped('++'))),
    '530': ('step-string-large-down', quiet('-9007199254740990', stepped('--')), quiet('-9007199254740991', stepped('--'))),
    # What kind of number a step leaves, by a fault only one kind has
    # (D45): `++` on a whole Num leaves an Int, and `--` a Num.
    '531': ('step-float-down-is-a-float', case(5.0, stepped('++'), ('do', ('set', '+=', 'v', 10**16))), case(5.0, stepped('--'), ('do', ('set', '+=', 'v', 10**16)))),
    '532': ('step-string-is-a-float', case(5, stepped('++'), ('do', ('set', '+=', 'v', 10**16))), case('5', stepped('++'), ('do', ('set', '+=', 'v', 10**16)))),
    '533': ('step-whole-float-printed', case(999999999999998.0, stepped('--')), case(1e15 + 1, stepped('--'))),
    # An undef on the left of an assigning operator: + - and . take it.
    '534': ('assign-undef-times', case(UNDEF, ('do', ('set', '+=', 'v', 2))), case(UNDEF, ('do', ('set', '*=', 'v', 2)))),
    '535': ('assign-undef-divide', case(UNDEF, ('do', ('set', '-=', 'v', 2))), case(UNDEF, ('do', ('set', '/=', 'v', 2)))),
    '536': ('assign-undef-power', case(FALSE, ('do', ('set', '**=', 'v', 2))), case(UNDEF, ('do', ('set', '**=', 'v', 2)))),
    '537': ('assign-undef-modulus', case(FALSE, ('do', ('set', '%=', 'v', 2))), case(UNDEF, ('do', ('set', '%=', 'v', 2)))),
    '538': ('assign-undef-repeat', case(UNDEF, ('do', ('set', '.=', 'v', 'a'))), case(UNDEF, ('do', ('set', 'x=', 'v', 2)))),
    '539': ('assign-undef-right', case(1, ('do', ('set', '+=', 'v', FALSE))), case(1, ('do', ('set', '+=', 'v', UNDEF)))),
    '540': ('assign-fault', case('12', ('do', ('set', '+=', 'v', 1))), case('abc', ('do', ('set', '+=', 'v', 1)))),
    # A variable that was never given a value is an undef (D48).
    '541': ('undef-variable', ('block', [('my', 'v', None), ('say', ('//', V, 'undef'))]), ('block', [('my', 'v', None), ('say', V)])),
    '542': ('undef-variable-added', ('block', [('my', 'v', None), ('say', ('+', ('||', V, 0), 1))]), ('block', [('my', 'v', None), ('say', ('+', V, 1))])),
    # A fault in a branch that is taken, and not in one that isn't.
    '543': ('fault-in-branch', ('block', [('my', 'v', 0), ('if', [(V, [('say', ('/', 1, V))])], [('say', 'else')])]),
            ('block', [('my', 'v', 0), ('if', [(('!', V), [('say', ('/', 1, V))])], [('say', 'else')])])),
    '544': ('fault-under-modifier', ('block', [('my', 'v', 0), ('mod', ('say', ('/', 1, V)), 'if', V), ('say', 'after')]),
            ('block', [('my', 'v', 0), ('mod', ('say', ('/', 1, V)), 'unless', V), ('say', 'after')])),
    '545': ('fault-in-condition', ('block', [('my', 'v', '0'), ('if', [(('==', V, 0), [('say', 'zero')])], None)]),
            ('block', [('my', 'v', 'zero'), ('if', [(('==', V, 0), [('say', 'zero')])], None)])),
    # The assignment is made before the fault that follows it in the statement.
    '546': ('late-read-fault', ('block', [('my', 'v', 1), ('say', ('/', 10, ('set', '=', 'v', 5))), shown(V)]),
            ('block', [('my', 'v', 1), ('say', ('/', V, ('set', '=', 'v', 0)))])),
    # A string that is 2^53 already, stepped back under it: found by
    # breaking the runtime (docs/briefs/step5-mutations.py).
    '550': ('step-string-edge', quiet('9007199254740991', stepped('--')), quiet('9007199254740992', stepped('--'))),
    '551': ('step-string-edge-up', quiet('-9007199254740991', stepped('++')), quiet('-9007199254740992', stepped('++'))),
    # A float past 2^53 whose step is not lost, one more being a tie
    # that rounds away: perl warns all the same (T130, by the review).
    '552': ('step-float-lost-tie', quiet(2.0**53, stepped('--')), quiet(2.0**53 + 2, stepped('++'))),
    '553': ('step-float-lost-negative', quiet(-(2.0**53), stepped('++')), quiet(-(2.0**53), stepped('--'))),
    '554': ('step-float-lost-negative-up', quiet(-(2.0**53), stepped('++')), quiet(-(2.0**53) - 2, stepped('++'))),
}

def commands():
    return ''.join(f'    python3 t/models/var.py --program {n} > t/{n}-{FAULTS[n][0]}.pl\n'
                   f'    python3 t/models/var.py {n} > t/{n}-{FAULTS[n][0]}.expected\n' for n in sorted(FAULTS))

def program(statements, header):
    lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in lines)

def main(argv):
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    # The list in the docstring is what t/checks.py reads, so it has to be
    # the whole list.
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/var.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/var.py']
    if number in SAME:
        name, cases = same(number)
        assert name == SAME[number]
        cases = [c for c in cases if output([c])[1] is None]
        out.write((program(cases, model) if want_program else output(cases)[0]).encode())
        return
    name, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    statements = [('say', 1), near, far, ('say', 2)]
    if want_program:
        out.write(program(statements, header).encode())
        return
    printed, fault, at = output(statements)
    assert fault is not None and output([('say', 1), near])[1] is None, (number, printed, fault)
    found = {}
    lines(statements, len(header) + 3, found)       # after the headers, `use v5.42;` and `use open`
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

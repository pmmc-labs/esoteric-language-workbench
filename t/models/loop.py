#!/usr/bin/env python3
"""t/700 to t/739: loops (step 6; D58 to D62).

The definition, which is all this file knows of the language beyond
t/models/var.py (variables, statements, and through it values and
operators).

  while (T) { ... }    T is worked out; if it is true the block runs and
                       T is worked out again
  until (T) { ... }    the same, while T is false
  for (F; T; E) { ... }   F once; then T, the block, E, T, the block, E.
                       F and E are assignments and steps with commas
                       between (D60), F a `my` too; no T is true
  S while T;  S until T;   T first, then S, then T
  last;  next;         out of the nearest loop round it; on to that
                       loop's E, if it has one, and its T
  last L;  next L;     the same for the loop labelled L (D61)

A `my` in a loop's block, or in the test of a `while` or an `until`, is a
new variable each time round, undef until it is given a value (T119). A
`my` in F is one variable for the whole loop, and gone after it.

A bare block is no loop (D59): a `last` or `next` with no label may not
have one as the nearest thing round it, and this model stops if a case of
its own does.

A fault in a T or an E names the line of its loop; under a modifier, the
line its statement starts on (D62).

Every loop here ends, and ends under perl too: where the language faults
perl may only warn and carry on, so a fault test's loop is counted by
something the fault doesn't touch.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

700 is each kind of loop, run no times, once and many, counting each way.
701 is `last` and `next`: from a loop inside a loop, of each kind, to the
inner or the outer, through an `if`, an `else`, a modifier and (with a
label) a bare block. 702 is what is new each time round and what is not.
703 is the same operation run more than once: the operators of steps 1 to
5, each in a loop, with the kinds of its operands changing from one time
round to the next. 720 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/loop.py --program 700 > t/700-loops.pl
    python3 t/models/loop.py 700 > t/700-loops.expected
    python3 t/models/loop.py --program 701 > t/701-jumps.pl
    python3 t/models/loop.py 701 > t/701-jumps.expected
    python3 t/models/loop.py --program 702 > t/702-each-time-round.pl
    python3 t/models/loop.py 702 > t/702-each-time-round.expected
    python3 t/models/loop.py --program 703 > t/703-again.pl
    python3 t/models/loop.py 703 > t/703-again.expected
    python3 t/models/loop.py --program 720 > t/720-fault-third-time.pl
    python3 t/models/loop.py 720 > t/720-fault-third-time.expected
    python3 t/models/loop.py --program 721 > t/721-fault-while-test.pl
    python3 t/models/loop.py 721 > t/721-fault-while-test.expected
    python3 t/models/loop.py --program 722 > t/722-fault-while-test-later.pl
    python3 t/models/loop.py 722 > t/722-fault-while-test-later.expected
    python3 t/models/loop.py --program 723 > t/723-fault-until-test.pl
    python3 t/models/loop.py 723 > t/723-fault-until-test.expected
    python3 t/models/loop.py --program 724 > t/724-fault-for-each.pl
    python3 t/models/loop.py 724 > t/724-fault-for-each.expected
    python3 t/models/loop.py --program 725 > t/725-fault-for-test.pl
    python3 t/models/loop.py 725 > t/725-fault-for-test.expected
    python3 t/models/loop.py --program 726 > t/726-fault-for-first.pl
    python3 t/models/loop.py 726 > t/726-fault-for-first.expected
    python3 t/models/loop.py --program 727 > t/727-fault-while-modifier.pl
    python3 t/models/loop.py 727 > t/727-fault-while-modifier.expected
    python3 t/models/loop.py --program 728 > t/728-fault-until-modifier.pl
    python3 t/models/loop.py 728 > t/728-fault-until-modifier.expected
    python3 t/models/loop.py --program 729 > t/729-fault-counter-overflow.pl
    python3 t/models/loop.py 729 > t/729-fault-counter-overflow.expected
    python3 t/models/loop.py --program 730 > t/730-fault-my-is-undef-again.pl
    python3 t/models/loop.py 730 > t/730-fault-my-is-undef-again.expected
    python3 t/models/loop.py --program 731 > t/731-fault-after-next.pl
    python3 t/models/loop.py 731 > t/731-fault-after-next.expected
    python3 t/models/loop.py --program 732 > t/732-fault-inner-loop.pl
    python3 t/models/loop.py 732 > t/732-fault-inner-loop.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
from var import Fault, MIN, MAX, UNDEF, TRUE, FALSE, get, logic, strings, text

class Jump(Exception):
    def __init__(self, kind, label):
        self.kind, self.label = kind, label

# A statement is one of var.py's, or ('while', label, test, body), ('until',
# ...), ('for', label, first, test, each, body) with first and each lists
# of expressions and test None for none, ('last', label), ('next', label),
# and ('mod', statement, 'while' or 'until', test). A label is a name or
# None. An expression is one of var.py's, or ('decl', op, name, e) for
# `my $name op e`, where a `my` may stand in an expression: a test, and a
# `for`'s first part.
class Run(var.Run):
    def __init__(self):
        super().__init__()
        self.frames = []        # 'loop' and 'bare', what is round the statement that is running

    def ev(self, e):
        if isinstance(e, tuple) and e[0] == 'decl':
            _, op, name, right = e
            value = get(self.ev(right))             # before the variable exists (T58)
            self.scopes[-1][name] = var.Place()
            return self.ev(('set', op, name, value))
        return super().ev(e)

    def round(self, body, label):
        """One time round a loop's block: 'last' or 'next' if a jump meant
        for this loop ended it."""
        scopes, frames = len(self.scopes), len(self.frames)
        try:
            self.block(body)
        except Jump as j:
            if j.label not in (None, label):
                raise
            del self.scopes[scopes:]
            del self.frames[frames:]
            return j.kind
        return None

    def run(self, s):
        kind = s[0]
        if kind in ('while', 'until'):
            _, label, test, body = s
            self.frames.append('loop')
            while True:
                # The test's own scope: a `my` in it is new each time
                # round, and seen by the block (T119).
                self.scopes.append({})
                self.at = id(s)
                if logic.truth(get(self.ev(test))) != (kind == 'while') or self.round(body, label) == 'last':
                    break
                self.scopes.pop()
            self.scopes.pop()
            self.frames.pop()
        elif kind == 'for':
            _, label, first, test, each, body = s
            self.frames.append('loop')
            self.scopes.append({})                  # for what the first part declares
            self.at = id(s)
            for e in first:
                self.ev(e)
            while True:
                self.at = id(s)
                if test is not None and not logic.truth(get(self.ev(test))):
                    break
                if self.round(body, label) == 'last':
                    break
                self.at = id(s)
                for e in each:
                    self.ev(e)
            self.scopes.pop()
            self.frames.pop()
        elif kind in ('last', 'next'):
            assert 'loop' in self.frames, f'{kind} outside a loop'
            assert s[1] is not None or self.frames[-1] == 'loop', f'{kind} with no label, and a bare block is the nearest thing round it (D59)'
            self.at = id(s)
            raise Jump(kind, s[1])
        elif kind == 'block':
            self.frames.append('bare')
            super().run(s)
            self.frames.pop()
        elif kind == 'mod' and s[2] in ('while', 'until'):
            _, inner, word, test = s
            while True:
                self.at = id(s)
                if logic.truth(get(self.ev(test))) != (word == 'while'):
                    break
                self.run(inner)
        else:
            super().run(s)

def declared(e, top):
    s = f'my ${e[2]} {e[1]} {text(e[3], False)}'
    return s if top else f'({s})'

var.MORE['decl'] = declared

def source(s, depth=0):
    """A statement as lines of source."""
    pad = '    ' * depth
    kind = s[0]
    body = lambda statements: [line for t in statements for line in source(t, depth + 1)]
    label = lambda name: '' if name is None else name + ': '
    if kind in ('while', 'until'):
        return [f'{pad}{label(s[1])}{kind} ({text(s[2])}) {{'] + body(s[3]) + [pad + '}']
    if kind == 'for':
        _, name, first, test, each, statements = s
        parts = [', '.join(text(e) for e in first), '' if test is None else text(test), ', '.join(text(e) for e in each)]
        return [f'{pad}{label(name)}for ({"; ".join(parts)}) {{'] + body(statements) + [pad + '}']
    if kind in ('last', 'next'):
        return [f'{pad}{kind}{"" if s[1] is None else " " + s[1]};']
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
    if kind == 'mod':
        return [source(s[1], depth)[0][:-1] + f' {s[2]} {text(s[3])};']
    return var.source(s, depth)

def output(statements):
    """What a program prints, and the fault that ended it or None, and
    the statement it was in."""
    r = Run()
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.at
    assert len(r.scopes) == 1 and r.frames == [], 'a scope was left open'
    return r.out, None, None

def lines(statements, line, found):
    """The line each statement starts on, as `source` lays them out, into
    `found`; an `elsif`'s test is on the line that says `elsif`. Returns
    the line after the last."""
    for s in statements:
        found[id(s)] = line
        kind = s[0]
        if kind in ('block', 'unless', 'while', 'until', 'for'):
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

I, J, K, M, S, V, W, R = (('$', name) for name in 'ijkmsvwr')
shown = var.shown

def block(*statements):
    return ('block', list(statements))

def do(e):
    return ('do', e)

def step(name, op='++', before=False):
    return ('step', op, before, name)

def set_(name, e, op='='):
    return ('set', op, name, e)

def my(name, e, op='='):
    return ('decl', op, name, e)

def join(*pieces):
    """The pieces in a row of dots."""
    e = pieces[0]
    for p in pieces[1:]:
        e = ('.', e, p)
    return e

def loop_cases():
    out = []
    say_i = ('say', I)
    up = do(step('i'))
    # From each start, to 3: many times round, once, and not at all.
    for start in (0, 2, 3, 5):
        head = [('my', 'i', start)]
        loops = [
            ('while', None, ('<', I, 3), [say_i, up]),
            ('until', None, ('>=', I, 3), [say_i, up]),
            ('while', None, ('<', step('i'), 3), [say_i]),
            ('while', None, ('<', step('i', '++', True), 3), [say_i]),
            ('until', None, ('>', step('i'), 2), [say_i]),
            ('while', None, ('<', set_('i', 2, '+='), 7), [say_i]),
            ('while', None, ('!', ('>=', I, 3)), [say_i, up, up]),
            ('for', None, [my('k', start)], ('<', K, 3), [step('k')], [('say', K)]),
            ('for', None, [my('k', start)], ('<', K, 3), [step('k', '++', True)], [('say', K)]),
            ('for', None, [], ('<', I, 3), [], [say_i, up]),
            ('for', None, [], ('<', I, 3), [step('i')], [say_i]),
            ('for', None, [], None, [], [('mod', ('last', None), 'if', ('>=', I, 3)), say_i, up]),
            ('for', None, [set_('i', I)], ('<', I, 3), [set_('i', 2, '+=')], [say_i]),
            ('for', None, [my('k', start)], None, [step('k')], [('mod', ('last', None), 'if', ('>', K, 4)), ('say', K)]),
            ('for', None, [my('k', start), my('m', 9)], ('<', K, M), [set_('k', 2, '+='), set_('m', 3, '-=')], [('say', join(K, ':', M))]),
            ('for', None, [set_('i', start), my('m', 3)], ('<', I, M), [step('i'), step('m', '--')], [('say', join(I, ':', M))]),
            ('mod', ('say', step('i')), 'while', ('<', I, 3)),
            ('mod', up, 'while', ('<', I, 3)),
            ('mod', do(set_('i', 2, '+=')), 'until', ('>=', I, 3)),
            ('mod', ('say', step('i', '--')), 'while', ('>', I, 0)),
            ('mod', ('say', step('i', '--', True)), 'until', ('<=', I, 0)),
            ('mod', do(set_('i', I, '+=')), 'while', ('&&', I, ('<', I, 40))),
        ]
        out += [block(*head, loop, shown(I)) for loop in loops]
    # What is true, as a loop's test: a number counted down to 0, a float
    # to 0.0, a string cut down to '0' and to nothing, an undef.
    out += [
        block(('my', 'i', 3), ('while', None, I, [say_i, do(step('i', '--'))]), shown(I)),
        block(('my', 'i', 3), ('until', None, ('!', I), [say_i, do(step('i', '--'))]), shown(I)),
        block(('my', 'i', 1.5), ('while', None, I, [say_i, do(set_('i', 0.5, '-='))]), shown(I)),
        block(('my', 's', '3210'), ('while', None, S, [('say', S), do(set_('s', ('call', 'substr', [S, 1])))]), shown(S)),
        block(('my', 's', 'abc'), ('while', None, ('ne', S, ''), [('say', S), do(set_('s', ('call', 'substr', [S, 1])))]), shown(S)),
        block(('my', 's', 'abc'), ('until', None, ('eq', S, ''), [('say', S), do(set_('s', ('call', 'substr', [S, 0, ('-', ('call', 'length', [S]), 1)])))]), shown(S)),
        block(('my', 's', None), ('while', None, S, [('say', 'not reached')]), ('until', None, ('call', 'defined', [S]), [do(set_('s', 'now'))]), shown(S)),
        block(('my', 's', ''), ('mod', do(set_('s', 'ab', '.=')), 'while', ('<', ('call', 'length', [S]), 7)), shown(S)),
        block(('my', 's', 'x'), ('mod', do(set_('s', 2, 'x=')), 'until', ('>', ('call', 'length', [S]), 20)), shown(S)),
        block(('my', 'i', 1), ('while', None, ('<', I, 1000), [do(set_('i', 3, '*='))]), shown(I)),
        block(('my', 'i', 1), ('my', 's', 0), ('while', None, ('<=', I, 100), [do(set_('s', I, '+=')), up]), shown(S)),
        block(('my', 'i', 10), ('my', 's', 1), ('for', None, [], ('>', I, 1), [step('i', '--')], [do(set_('s', I, '*='))]), shown(S)),
        block(('my', 'i', 1.0), ('while', None, ('<', I, 2), [say_i, do(set_('i', 0.25, '+='))]), shown(I)),
        block(('my', 'i', 27), ('my', 'k', 0), ('until', None, ('==', I, 1), [do(set_('i', ('?:', ('%', I, 2), ('+', ('*', I, 3), 1), ('/', I, 2)))), do(step('k'))]), shown(K)),
    ]
    # A loop in a loop, each kind in each.
    def counted(kind, name, limit, body):
        v = ('$', name)
        if kind == 'for':
            return [('for', None, [my(name, 0)], ('<', v, limit), [step(name)], body)]
        test = ('<', v, limit) if kind == 'while' else ('>=', v, limit)
        return [('my', name, 0), (kind, None, test, body + [do(step(name))])]
    for outer in ('while', 'until', 'for'):
        for inner in ('while', 'until', 'for'):
            out.append(block(*counted(outer, 'i', 3, counted(inner, 'j', I, [('say', join(I, '.', J))]) + [('say', join('end of ', I))])))
            out.append(block(('my', 'n', 0), *counted(outer, 'i', 4, counted(inner, 'j', 3, [do(step('n'))])), shown(('$', 'n'))))
    # In an `if`, and an `if` in one; three deep; a loop after a loop.
    out += [
        block(('my', 'i', 0), ('if', [(('==', I, 0), [('while', None, ('<', I, 2), [say_i, up])])], [('say', 'not reached')]), shown(I)),
        block(('my', 'i', 0), ('while', None, ('<', I, 6), [('if', [(('==', ('%', I, 3), 0), [('say', join(I, ' fizz'))]), (('==', ('%', I, 2), 0), [('say', join(I, ' even'))])], [say_i]), up])),
        block(('my', 'n', 0), ('for', None, [my('i', 0)], ('<', I, 3), [step('i')], [('for', None, [my('j', 0)], ('<', J, 3), [step('j')],
              [('for', None, [my('k', 0)], ('<', K, 3), [step('k')], [do(set_('n', ('+', ('+', I, J), K), '+='))])])]), shown(('$', 'n'))),
        block(('my', 'i', 0), ('while', None, ('<', I, 2), [up]), ('while', None, ('<', I, 4), [say_i, up]), ('until', None, ('<', I, 3), [do(step('i', '--'))]), shown(I)),
        block(('my', 'i', 0), ('while', None, ('<', I, 3), [up, ('mod', ('say', 'odd'), 'if', ('%', I, 2)), ('mod', ('say', 'even'), 'unless', ('%', I, 2))])),
        block(('my', 'i', 0), ('while', None, ('<', I, 3), [('block', [up, say_i])]), shown(I)),
        block(('my', 'i', 0), ('while', None, ('<', I, 3), [('mod', up, 'while', ('<', I, 2)), say_i, up])),
        block(('my', 'i', 0), ('while', None, ('<', step('i'), 3), [])),
        block(('my', 'i', 0), ('for', None, [], ('<', step('i'), 3), [], []), shown(I)),
        # The expressions of a part run left to right: the second sees
        # what the first did.
        block(('for', None, [my('k', 0), my('m', 0)], ('<', K, 3), [step('k'), set_('m', ('*', K, 10))], [('say', join(K, ':', M))])),
        block(('for', None, [my('k', 0), my('m', 0)], ('<', K, 3), [set_('m', ('*', K, 10)), step('k')], [('say', join(K, ':', M))])),
        block(('my', 'i', 0), ('my', 'j', 0), ('for', None, [set_('i', 1), set_('j', ('+', I, 1))], ('<', I, 3), [set_('j', I, '+='), step('i')], [('say', join(I, ':', J))])),
    ]
    return out

def jump_cases():
    out = []
    def loop(kind, label, name, body):
        """A loop of a kind that takes `name` from 1 to 3."""
        v = ('$', name)
        if kind == 'for':
            return [('for', label, [my(name, 1)], ('<=', v, 3), [step(name)], body)]
        test = ('<', v, 3) if kind == 'while' else ('>=', v, 3)
        return [('my', name, 0), (kind, label, test, [do(step(name))] + body)]
    two = ('==', J, 2)
    not_two = ('!=', J, 2)
    turn = 0
    for outer in ('while', 'until', 'for'):
        for inner in ('while', 'until', 'for'):
            for kind in ('last', 'next'):
                for target in ('nearest', 'INNER', 'OUTER'):
                    jump = (kind, None if target == 'nearest' else target)
                    forms = [
                        [('mod', jump, 'if', two)],
                        [('mod', jump, 'unless', not_two)],
                        [('if', [(two, [('say', 'jump'), jump])], None)],
                        [('if', [(not_two, [('say', 'stay')])], [jump])],
                        [('if', [(('<', J, 2), [('say', 'low')]), (two, [('if', [(I, [jump])], None)])], None)],
                    ]
                    # Through a bare block only with a label (D59).
                    if target != 'nearest':
                        forms += [[('block', [('mod', jump, 'if', two)])],
                                  [('block', [('block', [('if', [(two, [jump])], None)]), ('say', 'in the block')])]]
                    # Thinned, to keep the test to about three thousand
                    # statements: every form meets every jump and target, and
                    # every other pair of loops.
                    turn += 1
                    for form in forms[turn % 2::2]:
                        body = [('say', join('a', I, J))] + form + [('say', join('b', I, J))]
                        inside = loop(inner, 'INNER' if target == 'INNER' else None, 'j', body)
                        out.append(block(*loop(outer, 'OUTER' if target == 'OUTER' else None, 'i', inside + [('say', join('c', I))]), ('say', 'd')))
    count = ('my', 'n', 0)
    N = ('$', 'n')
    out += [
        # `last` leaves before the third part runs, and `next` runs it.
        block(('my', 'k', 0), ('for', None, [set_('k', 0)], ('<', K, 5), [step('k')], [('mod', ('last', None), 'if', ('==', K, 2))]), shown(K)),
        block(('my', 'k', 0), count, ('for', None, [set_('k', 0)], ('<', K, 5), [step('k')], [('mod', ('next', None), 'if', ('==', K, 2)), do(step('n'))]), shown(K), shown(N)),
        block(('my', 'k', 0), count, ('for', None, [], ('<', K, 5), [step('k'), step('n')], [('next', None)]), shown(K), shown(N)),
        # The first statement and the last one; a loop that runs once.
        block(('my', 'i', 0), ('while', None, 1, [('last', None)]), ('say', 'after')),
        block(('my', 'i', 0), ('while', None, ('<', step('i'), 3), [('next', None)]), shown(I)),
        block(('my', 'i', 0), ('while', None, 1, [do(step('i')), say_(I), ('last', None)]), shown(I)),
        block(('my', 'i', 0), ('until', None, 0, [do(step('i')), ('mod', ('next', None), 'if', ('<', I, 3)), ('last', None)]), shown(I)),
        block(('my', 'i', 0), ('for', None, [], None, [], [do(step('i')), ('mod', ('next', None), 'unless', ('>', I, 4)), ('last', None)]), shown(I)),
        # One name on two loops: the inner is meant.
        block(('my', 'i', 0), ('while', 'L', ('<', step('i'), 3), [('my', 'j', 0), ('while', 'L', 1, [do(step('j')), ('mod', ('last', 'L'), 'if', ('==', J, 2))]), ('say', join(I, J))])),
        block(('my', 'i', 0), ('while', 'L', ('<', step('i'), 3), [('my', 'j', 0), ('while', 'L', ('<', step('j'), 3), [('mod', ('next', 'L'), 'if', ('==', J, 2)), ('say', join(I, J))])])),
        # Out of three at once, and on to the middle one's next time round.
        block(count, ('for', 'A', [my('i', 0)], ('<', I, 3), [step('i')], [('for', 'B', [my('j', 0)], ('<', J, 3), [step('j')], [('for', 'C', [my('k', 0)], ('<', K, 3), [step('k')],
              [do(step('n')), ('mod', ('last', 'A'), 'if', ('==', N, 14))])])]), shown(N)),
        block(count, ('for', 'A', [my('i', 0)], ('<', I, 3), [step('i')], [('for', 'B', [my('j', 0)], ('<', J, 3), [step('j')], [('for', 'C', [my('k', 0)], ('<', K, 3), [step('k')],
              [('mod', ('next', 'B'), 'if', ('==', K, 1)), do(step('n'))])])]), shown(N)),
        block(count, ('for', 'A', [my('i', 0)], ('<', I, 3), [step('i')], [('for', 'B', [my('j', 0)], ('<', J, 3), [step('j')], [('for', 'C', [my('k', 0)], ('<', K, 3), [step('k')],
              [('mod', ('next', 'A'), 'if', ('==', J, 1)), ('mod', ('last', 'B'), 'if', ('==', I, 2)), ('mod', ('next', 'C'), 'unless', K), do(step('n'))])])]), shown(N)),
        # A jump under a test that has a `my` of its own; a labelled jump
        # from the test's loop's own block; a label nothing jumps to.
        block(('my', 'i', 0), ('while', None, ('<', my('d', step('i')), 5), [('mod', ('next', None), 'if', ('%', ('$', 'd'), 2)), ('say', ('$', 'd'))])),
        block(('my', 'i', 0), ('while', 'ONLY', ('<', step('i'), 5), [('mod', ('next', 'ONLY'), 'if', ('==', I, 2)), ('mod', ('last', 'ONLY'), 'if', ('==', I, 4)), say_(I)])),
        block(('my', 'i', 0), ('until', 'UNUSED_1', ('>=', step('i'), 2), [say_(I)])),
        # A loop left by `last` is left with its variables as they were.
        block(('my', 'i', 0), ('my', 's', ''), ('while', None, 1, [do(set_('s', I, '.=')), ('mod', ('last', None), 'if', ('>=', step('i'), 3)), do(set_('s', '-', '.='))]), shown(S), shown(I)),
    ]
    return out

def say_(e):
    return ('say', e)

def fresh_cases():
    def loops(body, head=()):
        """The body in a loop of each kind, three times round, `$i` 1 to 3."""
        return [block(*head, ('my', 'i', 0), ('while', None, ('<', step('i'), 3), body)),
                block(*head, ('my', 'i', 0), ('until', None, ('>=', I, 3), [do(step('i'))] + body)),
                block(*head, ('for', None, [my('i', 1)], ('<=', I, 3), [step('i')], body))]
    X = ('$', 'x')
    out = []
    # A `my` in the block: undef each time round, whatever it held last.
    out += loops([('my', 'x', None), shown(X), do(set_('x', I)), shown(X)])
    out += loops([('my', 'x', None), do(set_('x', 'a', '.=')), say_(X)])
    out += loops([('my', 'x', None), do(step('x')), say_(X)])
    out += loops([('my', 'x', None), do(set_('x', I, '+=')), say_(X)])
    out += loops([('my', 'x', None), do(set_('x', I, '//=')), say_(X)])
    out += loops([('my', 'x', None), do(set_('x', I, '||=')), say_(X)])
    out += loops([('my', 'x', None), ('if', [(('==', I, 1), [do(set_('x', 'one'))]), (('==', I, 2), [do(set_('x', 2.5))])], None), shown(X)])
    out += loops([('mod', ('next', None), 'if', ('==', I, 2)), ('my', 'x', None), do(set_('x', 'a', '.=')), say_(X)])
    out += loops([('my', 'x', None), do(set_('x', 'a', '.=')), ('mod', ('next', None), 'if', ('==', I, 2)), do(set_('x', 'b', '.=')), say_(X)])
    out += loops([('if', [(('!=', I, 2), [('my', 'x', None), do(set_('x', I, '.=')), say_(X)])], [('my', 'x', None), do(step('x', '--')), say_(X)])])
    out += loops([('block', [('my', 'x', None), do(set_('x', I, '.=')), say_(X)])])
    out += loops([('my', 'x', I), ('block', [('my', 'x', None), shown(X), do(set_('x', 'inner'))]), say_(X)])
    out += loops([('my', 'x', ('*', I, 10)), say_(X), do(step('x')), ('my', 'y', X), say_(('$', 'y'))])
    # An inner loop's, each time round the inner and the outer.
    out += loops([('my', 'j', 0), ('while', None, ('<', step('j'), 2), [('my', 'x', None), do(set_('x', join(I, J), '.=')), say_(X)])])
    out += loops([('my', 'x', None), ('for', None, [my('j', 0)], ('<', J, 2), [step('j')], [do(set_('x', J, '.='))]), say_(X)])
    # One declared before the loop is not new each time round.
    out += loops([do(set_('x', I, '.=')), say_(X)], head=[('my', 'x', None)])
    out += loops([do(step('x')), ('my', 'x', 'hidden'), do(set_('x', '!', '.='))], head=[('my', 'x', 10)])
    # A `my` in a test: new each time round, seen in the block, and a
    # `my` of the same name in the block hides it.
    out += [
        block(('my', 'i', 0), ('while', None, ('&&', my('x', 'a', '.='), ('<', step('i'), 3)), [say_(X), do(set_('x', 'b', '.=')), say_(X)])),
        block(('my', 'i', 0), ('until', None, ('>', my('x', step('i')), 2), [say_(X), do(set_('x', 10, '+='))])),
        block(('my', 'i', 0), ('while', None, ('<', my('x', step('i'), '+='), 3), [say_(X)])),
        block(('my', 'i', 0), ('while', None, ('<', my('x', step('i'), '//='), 3), [say_(X), do(set_('x', 99))])),
        block(('my', 'i', 3), ('while', None, my('x', step('i', '--')), [say_(X)])),
        block(('my', 'i', 0), ('while', None, ('<', my('x', step('i')), 3), [('my', 'x', 's'), say_(X)])),
        block(('my', 'x', 'outer'), ('my', 'i', 0), ('while', None, ('<', my('x', step('i')), 2), [say_(X)]), say_(X)),
        block(('my', 'i', 0), ('while', None, ('<', my('x', step('i')), 3), [('my', 'j', 0), ('while', None, ('<', my('y', step('j')), 2), [say_(join(X, ('$', 'y')))])])),
    ]
    # A `my` in the first part of a `for`: one variable for the whole loop.
    out += [
        block(('for', None, [my('k', 0), my('x', '')], ('<', K, 3), [step('k')], [do(set_('x', K, '.=')), say_(X)])),
        block(('for', None, [my('k', 0)], ('<', K, 3), [step('k')], [('my', 'k', 9), say_(K)])),
        block(('for', None, [my('k', 0)], ('<', K, 6), [step('k')], [do(step('k')), say_(K)])),
        block(('my', 'k', 'outer'), ('for', None, [my('k', 0)], ('<', K, 2), [step('k')], [say_(K)]), say_(K)),
        block(('my', 'k', 5), ('for', None, [my('k', ('+', K, 1))], ('<', K, 8), [step('k')], [say_(K)]), say_(K)),
        block(('for', None, [my('k', 0)], ('<', K, 2), [step('k')], [('for', None, [my('k', 5)], ('<', K, 7), [step('k')], [say_(K)]), say_(K)])),
    ]
    return out

# The same operation, run more than once: operands of every kind, in pairs
# that are each other's neighbours a few places on.
OPERANDS = [0, 1, -7, 2**53, MAX, MIN, 0.5, -2.5, 3.0, 2.0**53, '12', ' 3 ', '3.0', '1e3', 'ab', '', '0', TRUE, FALSE, UNDEF]
PAIRS = [(OPERANDS[n], OPERANDS[(n * 7 + r) % len(OPERANDS)]) for r in (1, 4, 9) for n in range(len(OPERANDS))]

def again_cases():
    bodies = [[shown((op, V, W))] for op in ('+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '<=', '>', '>=', '<=>', 'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'cmp',
                                             '&&', '||', '//', 'and', 'or', 'xor')]
    bodies += [[shown((op, V))] for op in ('-', '!', 'not')] + [[shown(('call', name, [V]))] for name in ('length', 'uc', 'lc', 'defined')]
    bodies += [[shown(('?:', V, W, V))], [shown(('call', 'substr', ['abcdefgh', V])) ], [shown(('call', 'index', [V, W]))]]
    bodies += [[('my', 'r', ('step', op, before, 'v')), shown(V), shown(R)] for op in ('++', '--') for before in (True, False)]
    bodies += [[('my', 'r', ('set', op, 'v', W)), shown(V), shown(R)] for op in ('+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=')]
    out = []
    for body in bodies:
        quiet = [pair for pair in PAIRS if output([block(('my', 'v', pair[0]), ('my', 'w', pair[1]), *body)])[1] is None]
        pairs = quiet[::max(1, len(quiet) // 12)][:12]
        arms = [(('==', K, n), [do(set_('v', a)), do(set_('w', b))]) for n, (a, b) in enumerate(pairs)]
        out.append(block(('my', 'v', None), ('my', 'w', None), ('my', 'k', 0),
                         ('while', None, ('<', K, len(pairs)), [('if', arms, None)] + body + [do(step('k'))])))
    return out

SAME = {'700': ('loops', loop_cases), '701': ('jumps', jump_cases), '702': ('each-time-round', fresh_cases), '703': ('again', again_cases)}

def counting(test, body, start=0):
    return block(('my', 'i', start), ('while', None, test, body))

# number: (name, a near case that prints, the one that faults)
FAULTS = {
    # The third time round, after what the first two printed.
    '720': ('fault-third-time', counting(('<', I, 2), [say_(('/', 10, ('-', 2, I))), do(step('i'))]), counting(('<', I, 3), [say_(('/', 10, ('-', 2, I))), do(step('i'))])),
    # In a test: the first time it is worked out, and a later time. The
    # line is the loop's.
    '721': ('fault-while-test', block(('my', 'v', '0'), ('while', None, ('==', V, 1), [say_('in')]), say_('after')),
            block(('my', 'v', 'zero'), ('while', None, ('==', V, 1), [say_('in')]), say_('after'))),
    '722': ('fault-while-test-later', counting(('>', ('/', 10, ('-', 3, I)), 0), [say_(I), do(step('i')), ('mod', ('last', None), 'if', ('==', I, 3))]),
            counting(('>', ('/', 10, ('-', 3, I)), 0), [say_(I), do(step('i'))])),
    '723': ('fault-until-test', block(('my', 'i', 2), ('until', None, ('||', ('==', I, 0), ('<', ('/', 10, I), 2)), [say_(I), do(step('i', '--'))])),
            block(('my', 'i', 2), ('until', None, ('<', ('/', 10, I), 2), [say_(I), do(step('i', '--'))]))),
    # In the third part of a `for`, in its test, and in its first part.
    # (perl says nothing at an overflow and carries on, unsigned and then
    # as a float, so the loop must end on something else: a test that the
    # fault alone would end runs for ever under perl.)
    '724': ('fault-for-each', block(('for', None, [my('i', MAX - 2), my('k', 0)], ('<', K, 2), [step('i'), step('k')], [say_(I)])),
            block(('for', None, [my('i', MAX - 2), my('k', 0)], ('<', K, 5), [step('i'), step('k')], [say_(I)]))),
    '725': ('fault-for-test', block(('for', None, [my('i', 2)], ('&&', ('>', I, 0), ('>', ('/', 10, I), 1)), [step('i', '--')], [say_(I)])),
            block(('for', None, [my('i', 2)], ('>', ('/', 10, I), 1), [step('i', '--')], [say_(I)]))),
    '726': ('fault-for-first', block(('my', 'v', 5), ('for', None, [my('i', ('/', 10, V))], ('<', I, 4), [step('i')], [say_(I)])),
            block(('my', 'v', 0), ('for', None, [my('i', ('/', 10, V))], ('<', I, 4), [step('i')], [say_(I)]))),
    # Under a modifier: the line the statement starts on.
    '727': ('fault-while-modifier', block(('my', 'i', 0), ('mod', say_(step('i')), 'while', ('&&', ('<', I, 2), ('>', ('/', 10, ('-', 2, I)), 0)))),
            block(('my', 'i', 0), ('mod', say_(step('i')), 'while', ('>', ('/', 10, ('-', 2, I)), 0)))),
    '728': ('fault-until-modifier', block(('my', 'i', 0), ('mod', say_(step('i')), 'until', ('||', ('==', I, 2), ('<', ('/', 10, ('-', 2, I)), 0)))),
            block(('my', 'i', 0), ('mod', say_(step('i')), 'until', ('<', ('/', 10, ('-', 2, I)), 0)))),
    '729': ('fault-counter-overflow', block(('my', 'k', 0), counting(('<', step('k'), 2), [do(step('i')), say_(I)], MAX - 2)),
            block(('my', 'k', 0), counting(('<', step('k'), 5), [do(step('i')), say_(I)], MAX - 2))),
    # A `my` in a block is undef again the second time round: what it
    # held the first time is not there to print. (One in a test is undef
    # the first time too, so no fault can tell: 702 prints it.)
    '730': ('fault-my-is-undef-again', counting(('<', step('i'), 2), [('my', 'x', None), ('mod', say_(('.', ('$', 'x'), 'a')), 'if', ('==', I, 3)), do(set_('x', 'set'))]),
            counting(('<', step('i'), 2), [('my', 'x', None), ('mod', say_(('.', ('$', 'x'), 'a')), 'if', ('==', I, 2)), do(set_('x', 'set'))])),
    # After a `next`, and in a loop inside a loop.
    '731': ('fault-after-next', counting(('<', step('i'), 3), [('mod', ('next', None), 'if', ('>=', I, 2)), say_(('/', 6, ('-', 2, I)))]),
            counting(('<', step('i'), 3), [('mod', ('next', None), 'if', ('==', I, 1)), say_(('/', 6, ('-', 2, I)))])),
    '732': ('fault-inner-loop', block(('for', 'OUT', [my('i', 0)], ('<', I, 3), [step('i')], [('for', None, [my('j', 0)], ('<', J, 3), [step('j')],
                                      [('mod', ('next', 'OUT'), 'if', ('==', J, I)), say_(('/', 6, ('-', I, J)))])])),
            block(('for', 'OUT', [my('i', 0)], ('<', I, 3), [step('i')], [('for', None, [my('j', 0)], ('<', J, 3), [step('j')],
                  [('mod', ('next', 'OUT'), 'if', ('>', J, I)), say_(('/', 6, ('-', I, J)))])]))),
}

def commands():
    return ''.join(f'    python3 t/models/loop.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/loop.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    # The list in the docstring is what t/checks.py reads, so it has to be
    # the whole list.
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/loop.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/loop.py']
    if number in SAME:
        cases = [c for c in SAME[number][1]() if output([c])[1] is None]
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

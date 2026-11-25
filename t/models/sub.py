#!/usr/bin/env python3
"""t/900 to t/939: subs (step 8; D67 to D73).

The definition, which is all this file knows of the language beyond
t/models/loop.py (loops, and through it variables, values and operators).

  sub NAME(PARAMETERS) { ... }   at the top level; called before or after
  NAME(ARGUMENTS)                an expression, and a statement

A parameter is `$p` (required), `$p = E`, `$p //= E` or `$p ||= E`
(optional), or a placeholder, `$` with or without a default, which takes
an argument and names nothing. **A sub copies each argument as its
parameter's turn comes, left to right** (T144): an argument that is a
variable is read then, after the arguments that are not variables were
worked out at the call (D14, T1), and after the defaults of the
parameters before it. A default is used when its argument is missing;
with `//=` also when it is undef, with `||=` also when it is false. It is
resolved before its own parameter exists (T138).

Too few arguments, or too many, is a fault, after every argument has been
worked out, at the caller's line.

A call has one of perl's three contexts, void, scalar or list (D18): void
as a statement and as a part of a `for`; list as an argument of `say` or
of another call; scalar anywhere else. `return E;`, a last statement that
is an expression, the arms of `? :`, the right side of `|| && // and or`,
brackets and a unary plus hand their own on (T146).

What a call is worth: the value of the `return` that ended it, a copy;
with no `return`, the value of its last statement if that is an
expression with no modifier; `true` if that is a `say` (D70). `return;`
and an empty body give undef to a scalar call, and to a list they are a
fault (D71). A sub that ends any other way has no value, and that is a
fault unless the call was void (D18, T145). Nothing is skipped under void
(T148).

A sub names its own variables, new at each call, and the file's: those
declared at the top level. **A file variable is undef as the program
starts, and its `my` stores nothing** (T134): `my $x;` leaves what a sub
called before it put there, and `my $x += 10;` adds to it (T147).

A fault names the line of the statement that was running (D34): the
sub's own while the sub runs, and the caller's again when it has returned.
A fault in a default names the line of its `sub`.

There is no limit on depth here: D68's is the implementation's, and its
tests are by hand. Nothing in this model goes 100 calls deep.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

900 is every form of parameter and default with each kind of value, and
every way a sub has a value. 901 is what is read when: arguments, returns,
defaults, the file's variables from three calls deep, a call before a
`my`. 902 is recursion: a sub that calls itself, two that call each other,
calls before the definition, `return` out of loops in loops. 903 is
context: what a sub that returns nothing is worth, and how a context is
handed on. 904 is a value with no past: the operators of steps 1 to 6 on
values that came through a sub, as an argument and as a return. 920 on
each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/sub.py --program 900 > t/900-subs.pl
    python3 t/models/sub.py 900 > t/900-subs.expected
    python3 t/models/sub.py --program 901 > t/901-read-when.pl
    python3 t/models/sub.py 901 > t/901-read-when.expected
    python3 t/models/sub.py --program 902 > t/902-recursion.pl
    python3 t/models/sub.py 902 > t/902-recursion.expected
    python3 t/models/sub.py --program 903 > t/903-context.pl
    python3 t/models/sub.py 903 > t/903-context.expected
    python3 t/models/sub.py --program 904 > t/904-through-a-sub.pl
    python3 t/models/sub.py 904 > t/904-through-a-sub.expected
    python3 t/models/sub.py --program 920 > t/920-fault-too-few.pl
    python3 t/models/sub.py 920 > t/920-fault-too-few.expected
    python3 t/models/sub.py --program 921 > t/921-fault-too-many.pl
    python3 t/models/sub.py 921 > t/921-fault-too-many.expected
    python3 t/models/sub.py --program 922 > t/922-fault-too-few-optional.pl
    python3 t/models/sub.py 922 > t/922-fault-too-few-optional.expected
    python3 t/models/sub.py --program 923 > t/923-fault-too-many-optional.pl
    python3 t/models/sub.py 923 > t/923-fault-too-many-optional.expected
    python3 t/models/sub.py --program 924 > t/924-fault-arguments-ran-first.pl
    python3 t/models/sub.py 924 > t/924-fault-arguments-ran-first.expected
    python3 t/models/sub.py --program 925 > t/925-fault-ends-in-if.pl
    python3 t/models/sub.py 925 > t/925-fault-ends-in-if.expected
    python3 t/models/sub.py --program 926 > t/926-fault-ends-in-loop.pl
    python3 t/models/sub.py 926 > t/926-fault-ends-in-loop.expected
    python3 t/models/sub.py --program 927 > t/927-fault-ends-in-modifier.pl
    python3 t/models/sub.py 927 > t/927-fault-ends-in-modifier.expected
    python3 t/models/sub.py --program 928 > t/928-fault-ends-in-return-if.pl
    python3 t/models/sub.py 928 > t/928-fault-ends-in-return-if.expected
    python3 t/models/sub.py --program 929 > t/929-fault-no-value-handed-on.pl
    python3 t/models/sub.py 929 > t/929-fault-no-value-handed-on.expected
    python3 t/models/sub.py --program 930 > t/930-fault-nothing-said.pl
    python3 t/models/sub.py 930 > t/930-fault-nothing-said.expected
    python3 t/models/sub.py --program 931 > t/931-fault-nothing-as-argument.pl
    python3 t/models/sub.py 931 > t/931-fault-nothing-as-argument.expected
    python3 t/models/sub.py --program 932 > t/932-fault-nothing-handed-on.pl
    python3 t/models/sub.py 932 > t/932-fault-nothing-handed-on.expected
    python3 t/models/sub.py --program 933 > t/933-fault-empty-body-in-list.pl
    python3 t/models/sub.py 933 > t/933-fault-empty-body-in-list.expected
    python3 t/models/sub.py --program 934 > t/934-fault-in-the-sub.pl
    python3 t/models/sub.py 934 > t/934-fault-in-the-sub.expected
    python3 t/models/sub.py --program 935 > t/935-fault-after-the-call.pl
    python3 t/models/sub.py 935 > t/935-fault-after-the-call.expected
    python3 t/models/sub.py --program 936 > t/936-fault-in-a-default.pl
    python3 t/models/sub.py 936 > t/936-fault-in-a-default.expected
    python3 t/models/sub.py --program 937 > t/937-fault-void-works-it-out.pl
    python3 t/models/sub.py 937 > t/937-fault-void-works-it-out.expected
    python3 t/models/sub.py --program 938 > t/938-fault-undef-argument.pl
    python3 t/models/sub.py 938 > t/938-fault-undef-argument.expected
    python3 t/models/sub.py --program 939 > t/939-fault-three-deep.pl
    python3 t/models/sub.py 939 > t/939-fault-three-deep.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
from var import Fault, MIN, MAX, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join

VOID, SCALAR, LIST = 'void', 'scalar', 'list'

class Return(Exception):
    def __init__(self, value):
        self.value = value

NO_VALUE = 'has no value: it does not end in a return or an expression'
NOTHING = 'returned nothing where a list is wanted'

def arity(name, got, least, most):
    """The fault for a wrong number of arguments, or None."""
    if least <= got <= most:
        return None
    few = got < least
    wanted = str(least) if least == most else f'at least {least}' if few else f'at most {most}'
    return f'too {"few" if few else "many"} arguments for {name}: got {got}, expected {wanted}'

# A program is a list of statements at the top level, among them ('sub',
# name, parameters, body): a parameter is (name or None, op or None,
# default or None). In a sub, ('return', e) with e None for `return;`. A
# call is the expression ('ucall', name, [arguments]).
class Run(loop.Run):
    def __init__(self, statements):
        super().__init__()
        self.ctx = SCALAR           # the context of the expression about to be worked out
        self.wants = []             # of each call that is open
        self.subs = {s[1]: s for s in statements if s[0] == 'sub'}
        # The file's variables are there, undef, before anything runs.
        for s in statements:
            name = s[1] if s[0] == 'my' else s[1][2] if s[0] == 'do' and isinstance(s[1], tuple) and s[1][0] == 'decl' else None
            if name is not None:
                self.scopes[0][name] = var.Place()
                self.scopes[0][name].value = UNDEF

    def top(self):
        return len(self.scopes) == 1 and not self.wants

    def ev(self, e):
        want, self.ctx = self.ctx, SCALAR
        try:
            if not isinstance(e, tuple):
                return e
            kind = e[0]
            if kind == 'ucall':
                results = []
                for a in e[2]:
                    self.ctx = LIST
                    results.append(self.ev(a))
                return self.call(e[1], results, want)
            if kind == 'decl' and self.top():
                # `my $x OP E` at the top level: the operator, on what the
                # variable holds (T147).
                return self.ev(('set', e[1], e[2], e[3]))
            if kind == '?:':
                test = logic.truth(get(self.ev(e[1])))
                self.ctx = want
                return self.ev(e[2] if test else e[3])
            if kind == '+' and len(e) == 2:
                self.ctx = want
                return self.ev(e[1])
            if len(e) == 3 and (kind in var.LAZY or kind == '//'):
                left = self.ev(e[1])
                wanted = get(left) is UNDEF if kind == '//' else logic.truth(get(left)) == var.LAZY[kind]
                if not wanted:
                    return left
                self.ctx = want
                return self.ev(e[2])
            return super().ev(e)
        finally:
            self.ctx = SCALAR

    def call(self, name, args, want):
        _, _, params, body = sub = self.subs[name]
        least = sum(1 for _, op, _ in params if op is None)
        fault = arity(name, len(args), least, len(params))
        if fault:
            raise Fault(fault)
        saved = self.scopes, self.frames, self.at
        self.scopes, self.frames = [self.scopes[0], {}], []
        self.wants.append(want)
        try:
            for k, (pname, op, default) in enumerate(params):
                given = k < len(args)
                v = get(args[k]) if given else UNDEF        # read now, at this parameter's turn
                if not given or (op == '//=' and v is UNDEF) or (op == '||=' and not logic.truth(v)):
                    self.at = id(sub)
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

    def body(self, name, body, want):
        for s in body[:-1]:
            self.run(s)
        if not body:
            if want == LIST:
                self.at = id(self.subs[name])
                raise Fault(f'{name} {NOTHING}')
            return UNDEF
        last = body[-1]
        if last[0] == 'do':
            self.at = id(last)
            self.ctx = want
            return get(self.ev(last[1]))
        self.run(last)
        if last[0] == 'say':
            return TRUE
        if want != VOID:
            self.at = id(last)
            raise Fault(f'{name} {NO_VALUE}')
        return UNDEF

    def run(self, s):
        kind = s[0]
        if kind == 'sub':
            return
        if kind == 'return':
            self.at = id(s)
            want = self.wants[-1]
            if s[1] is None:
                if want == LIST:
                    raise Fault(f'{self.names[-1]} {NOTHING}')
                raise Return(UNDEF)
            self.ctx = want
            raise Return(get(self.ev(s[1])))
        if kind == 'my' and self.top():
            # At the top level a `my` stores nothing (T134).
            self.at = id(s)
            if s[2] is not None:
                self.scopes[0][s[1]].value = get(self.ev(s[2]))
            return
        if kind == 'say':
            # The value first: working it out may print.
            self.at = id(s)
            self.ctx = LIST
            line = logic.printed(get(self.ev(s[1]))) + '\n'
            self.out += line
            return
        if kind == 'do':
            self.ctx = VOID
        super().run(s)

class Program(Run):
    """A Run that knows which sub each open call is of, for a fault's
    words, and that the first and third parts of a `for` are void."""
    def __init__(self, statements):
        super().__init__(statements)
        self.names = []
        self.alias = {}             # a `for` as it is run, to the statement it was

    def call(self, name, args, want):
        self.names.append(name)
        try:
            return super().call(name, args, want)
        finally:
            self.names.pop()

    def name(self):
        return self.names[-1]

    def ev(self, e):
        if isinstance(e, tuple) and e[0] == 'void':
            self.ctx = VOID
            return self.ev(e[1])
        return super().ev(e)

    def run(self, s):
        if s[0] == 'for':
            marked = ('for', s[1], [('void', e) for e in s[2]], s[3], [('void', e) for e in s[4]], s[5])
            self.alias[id(marked)] = id(s)
            self.kept = getattr(self, 'kept', []) + [marked]    # so that no other object is given its id
            loop.Run.run(self, marked)
            return
        super().run(s)

def ucall(name, *args):
    return ('ucall', name, list(args))

def called(e, top):
    return f'{e[1]}({", ".join(text(a) for a in e[2])})'

var.MORE['ucall'] = called

def parameter(p):
    name, op, default = p
    head = '$' if name is None else '$' + name
    return head if op is None else f'{head} {op} {text(default)}'

WORDS = ('and', 'or', 'xor', 'not')

def source(s, depth=0):
    """A statement as lines of source. Every statement that holds
    statements is laid out here, since one of them may be a `return`."""
    pad = '    ' * depth
    kind = s[0]
    inner = lambda statements: [line for t in statements for line in source(t, depth + 1)]
    label = lambda name: '' if name is None else name + ': '
    if kind == 'sub':
        return [f'{pad}sub {s[1]}({", ".join(parameter(p) for p in s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind == 'return':
        if s[1] is None:
            return [f'{pad}return;']
        # perl warns of a word operator after `return`, which binds
        # tighter than it does.
        loose = isinstance(s[1], tuple) and s[1][0] in WORDS
        return [f'{pad}return {text(s[1], not loose)};']
    if kind in ('while', 'until'):
        return [f'{pad}{label(s[1])}{kind} ({text(s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind == 'for':
        return [loop.source(('for',) + tuple(s[1:5]) + ([],))[0].replace('for', pad + 'for', 1) if s[1] is None
                else pad + loop.source(('for',) + tuple(s[1:5]) + ([],))[0]] + inner(s[5]) + [pad + '}']
    if kind == 'block':
        return [pad + '{'] + inner(s[1]) + [pad + '}']
    if kind == 'if':
        out = []
        for n, (test, statements) in enumerate(s[1]):
            out += [f'{pad}{"if" if n == 0 else "} elsif"} ({text(test)}) {{'] + inner(statements)
        if s[2] is not None:
            out += [pad + '} else {'] + inner(s[2])
        return out + [pad + '}']
    if kind == 'unless':
        return [f'{pad}unless ({text(s[1])}) {{'] + inner(s[2]) + [pad + '}']
    if kind == 'mod':
        return [source(s[1], depth)[0][:-1] + f' {s[2]} {text(s[3])};']
    return loop.source(s, depth)

def output(statements):
    """What a program prints, and the fault that ended it or None, and the
    statement it was in."""
    r = Program(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

def lines(statements, line, found):
    """The line each statement starts on, as `source` lays them out."""
    for s in statements:
        found[id(s)] = line
        kind = s[0]
        if kind in ('block', 'unless', 'while', 'until', 'for', 'sub'):
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

# ---- the cases. A case is a list of statements at the top level; every
# name in it, of a sub and of a file variable, ends in the case's number,
# so that the cases of a test are one program.

shown = var.shown
P, Q, R, N = (('$', name) for name in 'pqrn')

def sub(name, params, *body):
    return ('sub', name, list(params), list(body))

def req(name):
    return (name, None, None)

def opt(name, default, op='='):
    return (name, op, default)

def ret(e=None):
    return ('return', e)

def say_(e):
    return ('say', e)

def named(k):
    """Names for case k: f('id') is a sub's, g('n') a file variable's and
    G('n') that variable."""
    f = lambda base: f'{base}{k}'
    g = lambda base: f'{base}{k}'
    return f, g, lambda base: ('$', g(base))

VALUES = [0, 1, -7, 41, 0.5, 3.0, '', '0', 'ab', ' 3 ', '00', TRUE, FALSE, UNDEF]

def subs_cases():
    out = []
    k = 0
    def case(make):
        nonlocal k
        k += 1
        out.append(make(*named(k)))
    # A value in and out, each kind; by `return`, and as the last statement.
    case(lambda f, g, G: [sub(f('id'), [req('p')], ret(P)), sub(f('last'), [req('p')], do(P))]
         + [shown(ucall(f('id'), v)) for v in VALUES] + [shown(ucall(f('last'), v)) for v in VALUES])
    # Each kind of default, with nothing, and with each kind of value.
    for op in ('=', '//=', '||='):
        case(lambda f, g, G: [sub(f('d'), [opt('p', 'dflt', op)], ret(P)), shown(ucall(f('d')))] + [shown(ucall(f('d'), v)) for v in VALUES])
    # Two parameters, the second optional; and a default that reads the
    # first, that reads the file's variable, that calls a sub.
    case(lambda f, g, G: [('my', g('n'), 10),
                          sub(f('two'), [req('p'), opt('q', 2)], ret(join(P, ',', Q))),
                          sub(f('twice'), [req('p'), opt('q', ('*', P, 2))], ret(join(P, ',', Q))),
                          sub(f('file'), [opt('p', G('n'))], ret(P)),
                          sub(f('one'), [], ret(1)),
                          sub(f('viasub'), [opt('p', ('+', ucall(f('one')), 1))], ret(P)),
                          say_(ucall(f('two'), 1)), say_(ucall(f('two'), 1, 5)), say_(ucall(f('twice'), 4)), say_(ucall(f('twice'), 4, 1)),
                          say_(ucall(f('file'))), do(set_(g('n'), 11)), say_(ucall(f('file'))), say_(ucall(f('file'), 3)),
                          say_(ucall(f('viasub'))), say_(ucall(f('viasub'), 9))])
    # A default is worked out each time it is needed, and only then.
    case(lambda f, g, G: [('my', g('n'), 0), sub(f('count'), [opt('p', step(g('n')))], ret(P)),
                          say_(ucall(f('count'))), say_(ucall(f('count'), 9)), say_(ucall(f('count'))), say_(G('n'))])
    # Placeholders: an argument taken and not named; with a default, which
    # still runs.
    case(lambda f, g, G: [('my', g('n'), 0),
                          sub(f('skip'), [req(None), req('q')], ret(Q)),
                          sub(f('maybe'), [opt(None, step(g('n'))), opt('q', 6)], ret(Q)),
                          say_(ucall(f('skip'), 1, 2)), say_(ucall(f('maybe'))), say_(ucall(f('maybe'), 1)), say_(ucall(f('maybe'), 1, 2)), say_(G('n'))])
    # A default sees the file's variable of its own parameter's name, and
    # of a later parameter's (T138); a parameter hides the file's.
    case(lambda f, g, G: [('my', 'p', 3), ('my', 'q', 10),
                          sub(f('own'), [opt('p', P)], do(set_('p', 1, '+=')), ret(P)),
                          sub(f('later'), [opt('r', Q), opt('q', 2)], ret(join(R, ' ', Q))),
                          say_(ucall(f('own'))), say_(ucall(f('own'), 7)), say_(P), say_(ucall(f('later'))), say_(ucall(f('later'), 1, 5))])
    # A parameter is a variable: assigned, stepped, and the caller's is
    # not touched.
    case(lambda f, g, G: [('my', g('v'), 4),
                          sub(f('work'), [req('p')], do(set_('p', ('*', P, 2))), do(step('p')), do(set_('p', '!', '.=')), ret(P)),
                          say_(ucall(f('work'), G('v'))), say_(G('v'))])
    # Every way to have a value with no `return`: an assignment, each
    # step, a `my`, a value alone, a call, a `say`.
    case(lambda f, g, G: [('my', g('n'), 3),
                          sub(f('assign'), [req('p')], do(set_('p', 5, '+='))),
                          sub(f('after'), [], do(step(g('n')))),
                          sub(f('before'), [], do(step(g('n'), '++', True))),
                          sub(f('down'), [], do(step(g('n'), '--'))),
                          sub(f('decl'), [], do(my('x', 5))),
                          sub(f('alone'), [req('p')], do(('*', P, 2))),
                          sub(f('const'), [], do(42)),
                          sub(f('str'), [], do('s')),
                          sub(f('tern'), [req('p')], do(('?:', P, 'yes', 'no'))),
                          sub(f('call'), [req('p')], do(ucall(f('alone'), P))),
                          sub(f('says'), [], say_('said')),
                          say_(ucall(f('assign'), 1)), say_(ucall(f('after'))), say_(ucall(f('before'))), say_(ucall(f('down'))), say_(G('n')),
                          say_(ucall(f('decl'))), say_(ucall(f('alone'), 4)), say_(ucall(f('const'))), say_(ucall(f('str'))),
                          say_(ucall(f('tern'), 1)), say_(ucall(f('tern'), 0)), say_(ucall(f('call'), 5)),
                          ('my', g('r'), ucall(f('says'))), say_(G('r')), say_(('+', ucall(f('says')), 1))])
    # `return` from the middle, with a modifier, and what follows it never
    # runs.
    case(lambda f, g, G: [sub(f('sign'), [req('p')], ('mod', ret('neg'), 'if', ('<', P, 0)), ('mod', ret('zero'), 'unless', P), ret('pos'), say_('never')),
                          sub(f('early'), [req('p')], ('if', [(P, [say_('in'), ret('a')])], [ret('b')]), say_('never')),
                          say_(ucall(f('sign'), -3)), say_(ucall(f('sign'), 0)), say_(ucall(f('sign'), 8)),
                          say_(ucall(f('early'), 1)), say_(ucall(f('early'), 0))])
    # A sub's variables are new at each call, and a block's in it too.
    case(lambda f, g, G: [sub(f('fresh'), [req('p')], ('my', 'x', None), say_(('?:', ('call', 'defined', [('$', 'x')]), 'kept', 'new')), do(set_('x', P)), ret(('$', 'x'))),
                          say_(ucall(f('fresh'), 1)), say_(ucall(f('fresh'), 2))])
    # Calls as operands, as arguments, as tests, in loops.
    case(lambda f, g, G: [sub(f('inc'), [req('p')], ret(('+', P, 1))), sub(f('dbl'), [req('p')], ret(('*', P, 2))),
                          say_(('+', ucall(f('inc'), 1), ucall(f('dbl'), 2))), say_(ucall(f('inc'), ucall(f('dbl'), ucall(f('inc'), 1)))),
                          say_(('-', ucall(f('inc'), 5))), say_(('!', ucall(f('inc'), -1))), say_(('x', 'ab', ucall(f('inc'), 1))),
                          say_(('call', 'length', [ucall(f('dbl'), 50)])), say_(('call', 'substr', ['abcdef', ucall(f('inc'), 0), ucall(f('dbl'), 1)])),
                          ('if', [(('>', ucall(f('inc'), 1), 1), [say_('more')])], [say_('less')]),
                          ('mod', say_('mod'), 'if', ucall(f('inc'), 0)),
                          ('my', g('i'), 0), ('while', None, ('<', ucall(f('inc'), G('i')), 4), [say_(G('i')), do(set_(g('i'), ucall(f('inc'), G('i'))))]),
                          ('for', None, [my('j', ucall(f('inc'), 0))], ('<', ('$', 'j'), ucall(f('dbl'), 2)), [set_('j', ucall(f('inc'), ('$', 'j')))], [say_(('$', 'j'))]),
                          say_(('?:', ucall(f('inc'), -1), ucall(f('dbl'), 1), ucall(f('dbl'), 2))),
                          say_(('||', ucall(f('inc'), -1), ucall(f('dbl'), 4))), say_(('&&', ucall(f('inc'), 1), ucall(f('dbl'), 4))),
                          say_(('//', ucall(f('inc'), 1), ucall(f('dbl'), 4)))])
    return out

def late_cases():
    out = []
    k = 100
    def case(make):
        nonlocal k
        k += 1
        out.append(make(*named(k)))
    # T1: an argument that is the variable is read as the sub begins, after
    # the arguments that are not; one that is a value was read at the call.
    def t1(f, g, G):
        x = g('x')
        X = G('x')
        show = f('show')
        s = [('my', x, 1), sub(f('set'), [], do(set_(x, 9)), ret(0)), sub(show, [req('p'), req('q')], ret(join(P, ',', Q)))]
        for first in (X, ('+', X, 0), ('+', X), set_(x, 4), set_(x, 4, '+='), step(x, '++', True), step(x), ('-', X), ('?:', 1, X, 0), ('||', X, 0),
                      ('&&', X, X), ('//', X, 0), ('x', X, 2), ('call', 'length', [X])):
            s += [do(set_(x, 1)), say_(ucall(show, first, ucall(f('set')))), say_(X)]
        s += [do(set_(x, 1)), say_(ucall(show, X, step(x))), do(set_(x, 1)), say_(ucall(show, X, set_(x, 5))),
              do(set_(x, 1)), say_(ucall(show, step(x), X)), do(set_(x, 1)), say_(ucall(show, ucall(f('set')), X))]
        return s
    case(t1)
    # What a sub returns is a copy: a later change to the variable it
    # returned doesn't show.
    def copy(f, g, G):
        t = g('t')
        T = G('t')
        return [('my', t, 5), sub(f('step'), [], do(set_(t, 100, '+=')), ret(1)), sub(f('get'), [], ret(T)), sub(f('last'), [], do(T)),
                sub(f('tern'), [], ret(('?:', 1, T, 0))), sub(f('or'), [], ret(('||', T, 0))), sub(f('show'), [req('p'), req('q')], ret(P)),
                say_(('+', T, ucall(f('step')))), do(set_(t, 5)),
                say_(('+', ucall(f('get')), ucall(f('step')))), do(set_(t, 5)),
                say_(('+', ucall(f('last')), ucall(f('step')))), do(set_(t, 5)),
                say_(('+', ucall(f('tern')), ucall(f('step')))), do(set_(t, 5)),
                say_(('+', ucall(f('or')), ucall(f('step')))), do(set_(t, 5)),
                say_(ucall(f('show'), ucall(f('get')), ucall(f('step')))), do(set_(t, 5)),
                say_(ucall(f('show'), T, ucall(f('step'))))]
    case(copy)
    # T144: a `//=` or `||=` default runs before the arguments after it
    # are copied.
    def order(f, g, G):
        v = g('v')
        V = G('v')
        return [('my', v, 1), sub(f('bump'), [], do(set_(v, 9)), ret(5)),
                sub(f('dd'), [opt('p', ucall(f('bump')), '//='), opt('q', 0)], ret(join(P, ',', Q))),
                sub(f('oo'), [opt('p', ucall(f('bump')), '||='), opt('q', 0)], ret(join(P, ',', Q))),
                sub(f('three'), [req('p'), opt('q', ucall(f('bump')), '//='), opt('r', 0)], ret(join(P, ',', Q, ',', R))),
                say_(ucall(f('dd'), UNDEF, V)), do(set_(v, 1)), say_(ucall(f('dd'), 3, V)), do(set_(v, 1)),
                say_(ucall(f('oo'), 0, V)), do(set_(v, 1)), say_(ucall(f('dd'), UNDEF, ('+', V, 0))), do(set_(v, 1)),
                say_(ucall(f('three'), V, UNDEF, V)), do(set_(v, 1)),
                say_(ucall(f('three'), V, 2, V))]
    case(order)
    # The file's variables, read and written from three calls deep, and by
    # a sub written after its caller.
    def deep(f, g, G):
        n = g('n')
        return [('my', n, 0), ('my', g('log'), ''),
                sub(f('a'), [req('p')], do(set_(n, P, '+=')), ret(ucall(f('b'), ('+', P, 1)))),
                sub(f('b'), [req('p')], do(set_(n, P, '+=')), do(set_(g('log'), 'b', '.=')), ret(ucall(f('c'), ('+', P, 1)))),
                sub(f('c'), [req('p')], do(set_(n, P, '+=')), do(set_(g('log'), 'c', '.=')), ret(G('n'))),
                say_(ucall(f('a'), 1)), say_(G('n')), say_(ucall(f('a'), 10)), say_(G('log'))]
    case(deep)
    # T134, T147: a sub called before a `my` of the file's runs; the `my`
    # stores nothing, and with an operator it works on what is there.
    def before(f, g, G):
        return [do(ucall(f('bump'))), ('my', g('x'), None), shown(G('x')),
                do(ucall(f('bump'))), do(ucall(f('bump'))), do(my(g('y'), 10, '+=')), shown(G('y')),
                do(ucall(f('tag'))), do(my(g('s'), 'a', '.=')), shown(G('s')),
                do(ucall(f('one'))), do(my(g('d'), 10, '//=')), shown(G('d')),
                do(my(g('e'), 10, '//=')), shown(G('e')),
                ('my', g('z'), ucall(f('setz'))), shown(G('z')),
                sub(f('bump'), [], do(step(g('x'))), do(step(g('y')))),
                sub(f('tag'), [], do(set_(g('s'), 'q'))),
                sub(f('one'), [], do(set_(g('d'), 1))),
                sub(f('setz'), [], do(set_(g('z'), 7)), ret(8))]
    case(before)
    # An assignment whose right side is a call that changes the variable
    # on its left; an assigning operator beside one.
    def assign(f, g, G):
        x = g('x')
        return [('my', x, 1), sub(f('set'), [req('p')], do(set_(x, P)), ret(3)),
                do(set_(x, ucall(f('set'), 50))), say_(G('x')),
                do(set_(x, ucall(f('set'), 50), '+=')), say_(G('x')),
                # (`$x .= set('z')` is refused: D69 has the left of `.=` for
                # the first piece of a row, as D57 does.)
                do(set_(x, ucall(f('set'), 0), '||=')), say_(G('x')),
                do(set_(x, 2)), say_(('*', G('x'), ucall(f('set'), 10))),
                do(set_(x, 2)), say_(('*', ucall(f('set'), 10), G('x'))),
                do(set_(x, 2)), say_(('<', G('x'), ucall(f('set'), 10)))]
    case(assign)
    return out

def recursion_cases():
    out = []
    k = 200
    def case(make):
        nonlocal k
        k += 1
        out.append(make(*named(k)))
    case(lambda f, g, G: [say_(ucall(f('fact'), 10)), say_(ucall(f('fact'), 20)),
                          sub(f('fact'), [req('n')], ('mod', ret(1), 'if', ('<', N, 2)), ret(('*', N, ucall(f('fact'), ('-', N, 1)))))])
    case(lambda f, g, G: [sub(f('fib'), [req('n')], ret(('?:', ('<', N, 2), N, ('+', ucall(f('fib'), ('-', N, 1)), ucall(f('fib'), ('-', N, 2))))))]
         + [say_(ucall(f('fib'), n)) for n in (0, 1, 2, 10, 15)])
    case(lambda f, g, G: [sub(f('even'), [req('n')], ret(('?:', ('==', N, 0), TRUE, ucall(f('odd'), ('-', N, 1))))),
                          sub(f('odd'), [req('n')], ret(('?:', ('==', N, 0), FALSE, ucall(f('even'), ('-', N, 1)))))]
         + [shown(ucall(f('even'), n)) for n in (0, 1, 2, 7, 60, 97)])
    case(lambda f, g, G: [sub(f('gcd'), [req('p'), req('q')], ('mod', ret(P), 'unless', Q), ret(ucall(f('gcd'), Q, ('%', P, Q))))]
         + [say_(ucall(f('gcd'), a, b)) for a, b in ((12, 18), (17, 5), (0, 9), (9, 0), (1071, 462))])
    case(lambda f, g, G: [sub(f('ack'), [req('p'), req('q')], ('mod', ret(('+', Q, 1)), 'if', ('==', P, 0)),
                              ('mod', ret(ucall(f('ack'), ('-', P, 1), 1)), 'if', ('==', Q, 0)),
                              ret(ucall(f('ack'), ('-', P, 1), ucall(f('ack'), P, ('-', Q, 1))))),
                          say_(ucall(f('ack'), 2, 3))])
    case(lambda f, g, G: [sub(f('rev'), [req('p')], ('mod', ret(P), 'if', ('<', ('call', 'length', [P]), 2)),
                              ret(('.', ucall(f('rev'), ('call', 'substr', [P, 1])), ('call', 'substr', [P, 0, 1])))),
                          say_(ucall(f('rev'), 'abcdefg')), say_(ucall(f('rev'), '')), say_(ucall(f('rev'), 'x'))])
    # Each call's variables are its own, across a call of itself.
    case(lambda f, g, G: [sub(f('down'), [req('n')], ('my', 'mine', ('*', N, 10)), ('mod', do(ucall(f('down'), ('-', N, 1))), 'if', ('>', N, 0)),
                              say_(join(N, ':', ('$', 'mine')))),
                          do(ucall(f('down'), 3))])
    # 99 calls of one sub open at once, where perl says nothing yet.
    case(lambda f, g, G: [sub(f('depth'), [req('n')], ret(('?:', ('==', N, 0), 0, ('+', 1, ucall(f('depth'), ('-', N, 1)))))),
                          say_(ucall(f('depth'), 98)), say_(ucall(f('depth'), 98))])
    # `return` out of loops in loops, and out of blocks.
    def out_of(f, g, G):
        I, J = ('$', 'i'), ('$', 'j')
        find = sub(f('find'), [req('p')],
                   ('for', 'OUT', [my('i', 0)], ('<', I, 4), [step('i')], [
                       ('my', 'j', 0),
                       ('while', None, ('<', J, 4), [
                           ('mod', ret(join(I, ',', J)), 'if', ('==', ('*', I, J), P)),
                           ('mod', ('next', 'OUT'), 'if', ('>', ('*', I, J), P)),
                           do(step('j'))])]),
                   ret('none'))
        nest = sub(f('nest'), [req('p')], ('block', [('block', [('if', [(P, [ret('in')])], None)])]), ret('out'))
        until = sub(f('until'), [], ('my', 'i', 0), ('until', None, FALSE, [do(step('i')), ('mod', ret(I), 'if', ('>', I, 3))]))
        return [find, nest, until] + [say_(ucall(f('find'), n)) for n in (0, 2, 6, 9, 7)] + [say_(ucall(f('nest'), 1)), say_(ucall(f('nest'), 0)), say_(ucall(f('until')))]
    case(out_of)
    return out

def context_cases():
    out = []
    k = 300
    def case(make):
        nonlocal k
        k += 1
        out.append(make(*named(k)))
    # A sub that returns nothing is undef to a scalar call, each way a call
    # is scalar; and nothing is wrong under void.
    def nothing(f, g, G):
        none, empty = f('none'), f('empty')
        calls = lambda name: [
            ('my', g(name), ucall(name)), shown(G(name)),
            do(set_(g(name), ucall(name))), shown(G(name)),
            say_(('?:', ('call', 'defined', [ucall(name)]), 'defined', 'undef')),
            say_(('?:', ucall(name), 'true', 'false')),
            say_(('//', ucall(name), 'left is scalar')),
            say_(('||', ucall(name), 'left is scalar')),
            ('if', [(ucall(name), [say_('yes')])], [say_('no')]),
            ('mod', say_('unless'), 'unless', ucall(name)),
            say_(('!', ucall(name))),
            do(ucall(name)),
            ('mod', do(ucall(name)), 'if', 1),
            ('for', None, [set_(g(name), ucall(name))], ('!', ('call', 'defined', [G(name)])), [set_(g(name), 1)], [say_('for')]),
        ]
        return [sub(none, [], ret()), sub(empty, [])] + calls(none) + calls(empty)
    case(nothing)
    # A context is handed on: by `return f()`, by a last statement, through
    # `? :`, `||`, `&&`, `//`, brackets and a unary plus. Scalar all the
    # way, each gives undef.
    def handed(f, g, G):
        none = f('none')
        subs = [sub(none, [], ret()),
                sub(f('ret'), [], ret(ucall(none))),
                sub(f('last'), [], do(ucall(none))),
                sub(f('tern'), [req('p')], ret(('?:', P, ucall(none), 5))),
                sub(f('or'), [], ret(('||', 0, ucall(none)))),
                sub(f('and'), [], ret(('&&', 1, ucall(none)))),
                sub(f('dor'), [], ret(('//', UNDEF, ucall(none)))),
                sub(f('plus'), [], ret(('+', ucall(none)))),
                sub(f('two'), [], ret(ucall(f('ret'))))]
        says = [('my', g('v'), None)]
        for name, args in (('ret', []), ('last', []), ('tern', [1]), ('tern', [0]), ('or', []), ('and', []), ('dor', []), ('plus', []), ('two', [])):
            says += [do(set_(g('v'), ucall(f(name), *args))), shown(G('v')), do(ucall(f(name), *args))]
        return subs + says
    case(handed)
    # A sub with no value, called void, each way of ending; and each way a
    # call is void.
    def void(f, g, G):
        I = ('$', 'i')
        subs = [sub(f('if'), [req('p')], ('if', [(P, [say_('if')])], None)),
                sub(f('else'), [req('p')], ('if', [(P, [say_('if')])], [say_('else')])),
                sub(f('unless'), [req('p')], ('unless', P, [say_('unless')])),
                sub(f('while'), [req('p')], ('my', 'i', 0), ('while', None, ('<', I, P), [do(step('i'))]), ),
                sub(f('for'), [req('p')], ('for', None, [my('i', 0)], ('<', I, P), [step('i')], [say_(I)])),
                sub(f('block'), [req('p')], ('block', [say_('block')])),
                sub(f('mod'), [req('p')], ('mod', say_('mod'), 'if', P)),
                sub(f('retif'), [req('p')], ('mod', ret(1), 'if', P)),
                sub(f('setif'), [req('p')], ('my', 'x', 0), ('mod', do(set_('x', 7)), 'unless', P)),
                sub(f('tail'), [req('p')], do(ucall(f('if'), P)))]
        calls = []
        for name in ('if', 'else', 'unless', 'while', 'for', 'block', 'mod', 'retif', 'setif', 'tail'):
            calls += [do(ucall(f(name), 1)), do(ucall(f(name), 0)), ('mod', do(ucall(f(name), 2)), 'if', 1)]
        calls += [('my', g('k'), 0), ('for', None, [set_(g('k'), 0)], ('<', G('k'), 2), [step(g('k'))], [do(ucall(f('if'), G('k')))])]
        calls += [('mod', do(ucall(f('mod'), 1)), 'while', ('<', step(g('k')), 4))]
        # A sub that has a value when it returns one, though it ends
        # without: the value is the `return`'s.
        calls += [say_(ucall(f('retif'), 1))]
        return subs + calls
    case(void)
    # One value to a list: a `my` with nothing, an undef returned.
    case(lambda f, g, G: [sub(f('decl'), [], do(('decl0', 'x'))), sub(f('undef'), [], ret(UNDEF)), sub(f('show'), [opt('p', 'default')], ret(logic.shown(P))),
                          say_(ucall(f('show'), ucall(f('decl')))), say_(ucall(f('show'), ucall(f('undef')))), say_(ucall(f('show')))])
    return out

def through_cases():
    """loop.py's `again`, with each operand an argument of a sub that works
    the operator out, or the return of one that hands it back."""
    ops = [(op, V2, W2) for op in ('+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '<=', '>', '>=', '<=>', 'eq', 'ne', 'lt', 'le', 'gt', 'ge', 'cmp',
                                   '&&', '||', '//', 'xor')]
    ops += [(op, V2) for op in ('-', '!')] + [('call', name, [V2]) for name in ('length', 'uc', 'lc', 'defined')]
    ops += [('?:', V2, W2, V2), ('call', 'index', [V2, W2])]
    out = []
    for n, e in enumerate(ops):
        f, g, G = named(400 + n)
        inside = sub(f('in'), [req('v'), req('w')], ret(e))
        back = sub(f('id'), [req('p')], ret(P))
        quiet = [pair for pair in loop.PAIRS if output([inside, shown(ucall(f('in'), *pair))])[1] is None]
        pairs = quiet[::max(1, len(quiet) // 10)][:10]
        case = [inside, back]
        for a, b in pairs:
            # As arguments; and as what a sub returned, held in the file's
            # variables.
            case += [('my', 'v', ucall(f('id'), a)), ('my', 'w', ucall(f('id'), b)), shown(ucall(f('in'), a, b)), shown(e)]
            case = case[:-4] + [('block', case[-4:])]
        out.append(case)
    # `++` and `--`, and the assigning operators, on a parameter and on
    # what a sub returned.
    for n, form in enumerate([('step', op, before, 'v') for op in ('++', '--') for before in (True, False)]
                             + [('set', op, 'v', W2) for op in ('+=', '-=', '*=', '.=', 'x=', '||=', '&&=', '//=')]):
        f, g, G = named(450 + n)
        inside = sub(f('in'), [req('v'), req('w')], ('my', 'r', form), ret(join(logic.shown(V2), ' ', logic.shown(('$', 'r')))))
        quiet = [pair for pair in loop.PAIRS if output([inside, say_(ucall(f('in'), *pair))])[1] is None]
        out.append([inside] + [say_(ucall(f('in'), a, b)) for a, b in quiet[::max(1, len(quiet) // 10)][:10]])
    return out

V2, W2 = ('$', 'v'), ('$', 'w')

def declared0(e, top):
    return f'my ${e[1]}'

var.MORE['decl0'] = declared0

_program_ev = Program.ev
def ev_with_decl0(self, e):
    if isinstance(e, tuple) and e[0] == 'decl0':
        self.ctx = SCALAR
        self.scopes[-1][e[1]] = var.Place()
        self.scopes[-1][e[1]].value = UNDEF
        return self.scopes[-1][e[1]]
    return _program_ev(self, e)
Program.ev = ev_with_decl0

SAME = {'900': ('subs', subs_cases), '901': ('read-when', late_cases), '902': ('recursion', recursion_cases), '903': ('context', context_cases),
        '904': ('through-a-sub', through_cases)}

# number: (name, the subs, a near case that prints, the one that faults)
def faults():
    none = sub('none', [], ret())
    show = sub('show', [opt('p', 'default')], ret(P))
    two = sub('two', [req('p'), req('q')], ret(join(P, ',', Q)))
    opt2 = sub('opt', [req('p'), opt('q', 2), opt('r', 3)], ret(join(P, ',', Q, ',', R)))
    loud = sub('loud', [req('p')], say_(P), ret(P))
    return {
        '920': ('fault-too-few', [two], say_(ucall('two', 1, 2)), say_(ucall('two', 1))),
        '921': ('fault-too-many', [two], say_(ucall('two', 1, 2)), say_(ucall('two', 1, 2, 3))),
        '922': ('fault-too-few-optional', [opt2], say_(ucall('opt', 1)), say_(ucall('opt'))),
        '923': ('fault-too-many-optional', [opt2], say_(ucall('opt', 1, 5, 6)), say_(ucall('opt', 1, 5, 6, 7))),
        # Every argument is worked out before the count is looked at.
        '924': ('fault-arguments-ran-first', [two, loud], say_(ucall('two', ucall('loud', 'a'), ucall('loud', 'b'))),
                say_(ucall('two', ucall('loud', 'c'), ucall('loud', 'd'), ucall('loud', 'e')))),
        # A sub with no value, and the value used. Void, each is fine.
        '925': ('fault-ends-in-if', [sub('ends', [req('p')], ('if', [(P, [say_('yes')])], None))], do(ucall('ends', 1)), ('my', 'v', ucall('ends', 0))),
        '926': ('fault-ends-in-loop', [sub('ends', [req('p')], ('my', 'i', 0), ('while', None, ('<', ('$', 'i'), P), [do(step('i'))]))],
                do(ucall('ends', 2)), say_(('+', ucall('ends', 2), 1))),
        '927': ('fault-ends-in-modifier', [sub('ends', [req('p')], ('my', 'x', 1), ('mod', do(set_('x', 7)), 'if', P))],
                ('mod', do(ucall('ends', 1)), 'if', 1), ('if', [(ucall('ends', 1), [say_('never')])], None)),
        '928': ('fault-ends-in-return-if', [sub('ends', [req('p')], ('mod', ret('yes'), 'if', P))], say_(ucall('ends', 1)), say_(ucall('ends', 0))),
        '929': ('fault-no-value-handed-on', [sub('ends', [req('p')], ('block', [say_('in')])), sub('tail', [req('p')], ret(('?:', P, 5, ucall('ends', P))))],
                block(say_(ucall('tail', 1)), do(ucall('tail', 0))), ('my', 'v', ucall('tail', 0))),
        # A sub that returns nothing, where perl wants a list (D71).
        '930': ('fault-nothing-said', [none], ('my', 'v', ucall('none')), say_(ucall('none'))),
        '931': ('fault-nothing-as-argument', [none, show], say_(ucall('show', ('!', ucall('none')))), say_(ucall('show', ucall('none')))),
        '932': ('fault-nothing-handed-on', [none, show, sub('tail', [req('p')], ret(('||', P, ('+', ucall('none')))))],
                block(('my', 'v', ucall('tail', 0)), say_(ucall('show', ucall('tail', 4)))), say_(ucall('show', ucall('tail', 0)))),
        '933': ('fault-empty-body-in-list', [sub('empty', []), show], block(do(ucall('empty')), say_(ucall('show', ('//', ucall('empty'), 'scalar')))),
                say_(ucall('show', ('?:', 1, ucall('empty'), 0)))),
        # The line: the sub's own statement while it runs, the caller's
        # again after it has returned, and the `sub`'s for a default.
        '934': ('fault-in-the-sub', [sub('div', [req('p')], ('my', 'x', 10), say_('in'), ret(('/', ('$', 'x'), P)))], say_(ucall('div', 5)), say_(ucall('div', 0))),
        '935': ('fault-after-the-call', [sub('div', [req('p')], say_('in'), ret(P))], say_(('/', 10, ucall('div', 5))), say_(('/', 10, ucall('div', 0)))),
        '936': ('fault-in-a-default', [sub('dflt', [req('p'), opt('q', ('/', 10, P))], ret(Q))], block(say_(ucall('dflt', 5)), say_(ucall('dflt', 0, 1))), say_(ucall('dflt', 0))),
        # T148: a void call still works its value out.
        '937': ('fault-void-works-it-out', [sub('twice', [req('p')], do(('*', P, 2))), sub('tag', [req('p')], ret(('.', P, 'a')))],
                block(do(ucall('twice', 4)), do(ucall('tag', 'x'))), do(ucall('twice', UNDEF))),
        '938': ('fault-undef-argument', [sub('len', [opt('p', UNDEF)], ret(('+', P, 1)))], say_(ucall('len', 1)), say_(ucall('len'))),
        '939': ('fault-three-deep', [sub('a', [req('p')], ret(('+', 1, ucall('b', P)))), sub('b', [req('p')], ret(('+', 1, ucall('c', P)))),
                                     sub('c', [req('p')], ret(('%', 7, P)))], say_(ucall('a', 2)), say_(ucall('a', 0))),
    }

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/sub.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/sub.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    # A call here is a dozen of Python's, and 902 goes 99 deep.
    sys.setrecursionlimit(20000)
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/sub.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/sub.py']
    if number in SAME:
        cases = SAME[number][1]()
        for c in cases:
            assert output(c)[1] is None, (number, c[:2], output(c)[1])
        statements = [s for c in cases for s in c]
        out.write((program(statements, model) if want_program else output(statements)[0]).encode())
        return
    name, subs, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    statements = subs + [('say', 1), near, far, ('say', 2)]
    if want_program:
        out.write(program(statements, header).encode())
        return
    printed, fault, at = output(statements)
    assert fault is not None and output(subs + [('say', 1), near])[1] is None, (number, printed, fault)
    found = {}
    lines(statements, len(header) + 3, found)       # after the headers, `use v5.42;` and `use open`
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])

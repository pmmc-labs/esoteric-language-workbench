#!/usr/bin/env python3
"""t/3010 to t/3017: `die`, `try` and `catch` (step 15; D141 to D143, D150).

The definition, which is all this file knows of the language beyond the
models before it:

  die LIST            the message is the values joined with nothing
                      between, each made a string as `.` makes one;
                      `Died` if that is empty; and ` at FILE line N.` and
                      a newline after it unless it ends in a newline.
                      FILE is the test's path, N the line the die's
                      statement is on (every statement here is on one
                      line, as D150 asks of a message with a line in it).
  try B catch ($e) C  B runs; a die in it, however deep in the subs B
                      calls, ends B, and C runs with $e the message.
                      A die in C goes to the try round this one.
  return, last, next  in B or C, what they are anywhere.

**Everything B had open is put back**: a loop over an array that a die
left ends, and the array may be changed after; a sort or a map that a
die left is over, and its list and its arrays are as they were. What the
die's statement had done before the die stays done (D80's orders: an
element made by `.=` stays made).

Python's try/except is the model of try/catch: each program is worked
out by Python code that does what the Perl does, written beside it.

The model is Python; perl is the second derivation (t/checks.py oracle).

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/die.py --program 3010 > t/3010-die-deep.pl
    python3 t/models/die.py 3010 > t/3010-die-deep.expected
    python3 t/models/die.py --program 3011 > t/3011-die-loops.pl
    python3 t/models/die.py 3011 > t/3011-die-loops.expected
    python3 t/models/die.py --program 3012 > t/3012-die-binders.pl
    python3 t/models/die.py 3012 > t/3012-die-binders.expected
    python3 t/models/die.py --program 3013 > t/3013-die-nested.pl
    python3 t/models/die.py 3013 > t/3013-die-nested.expected
    python3 t/models/die.py --program 3014 > t/3014-die-flow.pl
    python3 t/models/die.py 3014 > t/3014-die-flow.expected
    python3 t/models/die.py --program 3015 > t/3015-die-state.pl
    python3 t/models/die.py 3015 > t/3015-die-state.expected
    python3 t/models/die.py --program 3016 > t/3016-die-messages.pl
    python3 t/models/die.py 3016 > t/3016-die-messages.expected
"""

import random
import sys

NAMES = {
    3010: 'die-deep', 3011: 'die-loops', 3012: 'die-binders', 3013: 'die-nested',
    3014: 'die-flow', 3015: 'die-state', 3016: 'die-messages',
}


class Died(Exception):
    def __init__(self, message):
        self.message = message


class Program:
    """Lines of Perl, numbered as they are written, and the output the
    model works out for them."""

    def __init__(self, n):
        self.file = f't/{n}-{NAMES[n]}.pl'
        self.lines = ['# model: t/models/die.py', 'use v5.42;']
        self.out = []

    def line(self, text):
        self.lines.append(text)
        return len(self.lines)

    def say(self, *values):
        self.out.append(''.join(values) + '\n')

    def text(self):
        return '\n'.join(self.lines) + '\n'


def num(x):
    """A number as perl prints it (the models before this one have the
    rule; these are small and not whole floats from 10^15)."""
    if isinstance(x, int):
        return str(x)
    s = '%.15g' % x
    return '0' if s in ('0', '-0') else s


def message(p, values, line):
    text = ''.join(values)
    if text == '':
        text = 'Died'
    if not text.endswith('\n'):
        text += f' at {p.file} line {line}.\n'
    return text


def perl_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('$', '\\$').replace('@', '\\@') + '"'


# The messages a die may be given: the Perl of its list, and the strings
# perl makes of each value.
MESSAGES = [
    ('"plain"', ['plain']),
    ('"with newline\\n"', ['with newline\n']),
    ('"two\\nlines"', ['two\nlines']),
    ('"a", 1, "b", 2.5', ['a', '1', 'b', '2.5']),
    ('""', ['']),
    ('', []),
    ('false', ['']),
    ('true, "!"', ['1', '!']),
    ('0', ['0']),
    ('1e21', ['1e+21']),
    ('-7, "\\n"', ['-7', '\n']),
    ('"", "end\\n"', ['', 'end\n']),
]


def deep(p, rng):
    """A sub that calls itself to a depth and dies there, caught at the
    top, again and again: the frames a die drops are given back."""
    p.line("no warnings 'recursion';")
    line = p.line('sub down($n, $k, $m) { die "at depth $n\\n" if $n == $k && $m == 0; die "deep", $n if $n == $k && $m == 1; return down($n + 1, $k, $m) + 1 }')
    total = 0
    for k in [0, 1, 2, 5, 40, 300, 3, 0, 120]:
        for m in (0, 1):
            p.line(f'try {{ my $r = down(0, {k}, {m}); say "no die" }} catch ($e) {{ print "caught: ", $e }}')
            p.say('caught: ', message(p, [f'at depth {k}\n'] if m == 0 else ['deep', str(k)], line).rstrip('\n'))
            total += 1
    p.line('sub up($n) { return $n if $n == 0; return up($n - 1) + 1 }')
    p.line('say "and a call that returns: ", up(50);')
    p.say('and a call that returns: 50')


def loops(p, rng):
    """A die in a loop over an array, a hash's values and a range, caught
    outside: the loop's freeze is given back, and the container may be
    changed after."""
    for case in range(8):
        values = [rng.randint(1, 9) for _ in range(rng.randint(2, 6))]
        stop = rng.choice(values + [100])
        p.line(f'{{ my @a = ({", ".join(map(str, values))}); my $seen = 0;')
        dline = p.line(f'try {{ for my $x (@a) {{ $seen++; die "stop at $x\\n" if $x == {stop} }} say "ran all" }} catch ($e) {{ print $e }}')
        seen = 0
        try:
            for x in values:
                seen += 1
                if x == stop:
                    raise Died(f'stop at {x}\n')
            p.say('ran all')
        except Died as e:
            p.out.append(e.message)
        p.line(f'push @a, {case}; $a[0] = 0; say "$seen @a"; }}')
        values.append(case)
        values[0] = 0
        p.say(f'{seen} ' + ' '.join(map(str, values)))
    # A hash's values, frozen and given back.
    p.line('{ my %h = (a => 1, b => 2, c => 3);')
    p.line('try { for my $v (sort { $a <=> $b } values %h) { die "v $v\\n" if $v == 2 } } catch ($e) { print $e }')
    p.out.append('v 2\n')
    p.line('try { for my $k (sort keys %h) { die "k $k\\n" if $h{$k} == 3 } } catch ($e) { print $e }')
    p.out.append('k c\n')
    p.line('try { for my $v (sort { $a <=> $b } values %h) { die "plain\\n" } } catch ($e) { print $e }')
    p.out.append('plain\n')
    p.line('$h{d} = 4; delete $h{a}; say join(",", sort keys %h); }')
    p.say('b,c,d')
    # Loops in loops, the die from the inner one, caught between them.
    p.line('{ my @o = (1, 2, 3); my @i = (4, 5);')
    p.line('for my $x (@o) { try { for my $y (@i) { die "$x$y\\n" if $y == 5 } } catch ($e) { print $e; push @i, 6 if $x == 2 } }')
    inner = [4, 5]
    for x in [1, 2, 3]:
        try:
            for y in list(inner):
                if y == 5:
                    raise Died(f'{x}{y}\n')
        except Died as e:
            p.out.append(e.message)
            if x == 2:
                inner.append(6)
    p.line('say "@i"; }')
    p.say(' '.join(map(str, inner)))


def binders(p, rng):
    """A die in the block of a map, a grep and a sort; the sort's machine
    is freed, and the next sort is a sort; the list's arrays thawed."""
    for case in range(6):
        values = rng.sample(range(1, 30), rng.randint(3, 8))
        bad = rng.choice(values)
        vs = ', '.join(map(str, values))
        p.line(f'{{ my @a = ({vs}); my $n = 0;')
        p.line(f'try {{ my @m = map {{ $n++; die "map $_\\n" if $_ == {bad}; $_ * 2 }} @a; say "@m" }} catch ($e) {{ print $e }}')
        n = 0
        try:
            m = []
            for v in values:
                n += 1
                if v == bad:
                    raise Died(f'map {v}\n')
                m.append(v * 2)
            p.say(' '.join(map(str, m)))
        except Died as e:
            p.out.append(e.message)
        p.line(f'try {{ my @g = grep {{ die "grep $_\\n" if $_ == {bad}; $_ % 2 }} @a; say "@g" }} catch ($e) {{ print $e }}')
        p.out.append(f'grep {bad}\n')
        # The sort dies at the first comparison that has the bad value in
        # it; which comparisons perl makes is t/models/merge.py's, and the
        # first to touch `bad` is all that matters here, since the die ends
        # the sort whatever its order.
        p.line(f'try {{ my @s = sort {{ die "sort\\n" if $a == {bad} || $b == {bad}; $a <=> $b }} @a; say "@s" }} catch ($e) {{ print $e }}')
        p.out.append('sort\n')
        p.line('my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }')
        p.say(f'{n} ' + ' '.join(map(str, sorted(values))) + f' {len(values) + 1}')
    # A try in the block of a map and of a sort.
    p.line('{ my @a = (3, 1, 2);')
    p.line('my @m = map { my $v = $_; try { die "odd\\n" if $v % 2 } catch ($e) { $v = 0 } $v } @a; say "@m";')
    p.say('0 0 2')
    p.line('my @s = sort { my $c = 0; try { die "x\\n" if $a == 2; $c = $a <=> $b } catch ($e) { $c = $b <=> $a } $c } @a; say scalar(@s); }')
    p.say('3')


def nested(p, rng):
    """Tries in tries: a die in a catch goes out one; `die $e` throws the
    message again unchanged; a die with no newline carries its own line."""
    for case in range(10):
        depth = rng.randint(1, 4)
        acts = [rng.choice(['rethrow', 'wrap', 'swallow', 'fresh']) for _ in range(depth)]
        # Build from the inside out, on one line.
        dline = len(p.lines) + 1
        inner = 'die "core"'
        code = inner
        model = [('core', None)]
        for level, act in enumerate(acts):
            handler = {'rethrow': 'die $e', 'wrap': f'die "L{level}: $e"', 'swallow': f'print "L{level} kept: $e"', 'fresh': f'die "new{level}"'}[act]
            code = f'try {{ {code} }} catch ($e) {{ {handler} }}'
        p.line(f'try {{ {code} }} catch ($e) {{ print "top: $e" }}')
        # Work it out.
        msg = message(p, ['core'], dline)
        live = True
        for level, act in enumerate(acts):
            if not live:
                break
            if act == 'rethrow':
                pass
            elif act == 'wrap':
                msg = f'L{level}: {msg}'
            elif act == 'swallow':
                p.out.append(f'L{level} kept: {msg}')
                live = False
            else:
                msg = message(p, [f'new{level}'], dline)
        if live:
            p.out.append(f'top: {msg}')


def flow(p, rng):
    """`return`, `last` and `next` out of a try and out of a catch, each
    closing the try on the way: a later die finds the right one."""
    p.line('sub pick($n) { try { return "small" if $n < 3; die "big\\n" if $n > 6; } catch ($e) { return "caught $e" } return "middle" }')
    for n in range(0, 9):
        p.line(f'print pick({n}), "\\n";')
        p.out.append('small\n' if n < 3 else f'caught big\n\n' if n > 6 else 'middle\n')
    p.line('for my $i (1 .. 6) { try { next if $i == 2; last if $i == 5; die "d$i\\n" if $i % 2; say "even $i" } catch ($e) { print "c $e"; next if $i == 3 } say "after $i" }')
    for i in range(1, 7):
        try:
            if i == 2:
                continue
            if i == 5:
                break
            if i % 2:
                raise Died(f'd{i}\n')
            p.say(f'even {i}')
        except Died as e:
            p.out.append(f'c {e.message}')
            if i == 3:
                continue
        p.say(f'after {i}')
    p.line('OUTER: for my $i (1 .. 3) { for my $j (1 .. 3) { try { next OUTER if $j == 2; try { last OUTER if $i == 3 } catch ($f) { } say "$i$j" } catch ($e) { } } }')
    for i in range(1, 4):
        stop = False
        for j in range(1, 4):
            if j == 2:
                break
            if i == 3:
                stop = True
                break
            p.say(f'{i}{j}')
        if stop:
            break
    # After all those ways out, a die must find the try round it, and
    # nothing else.
    line = p.line('try { die "last one" } catch ($e) { print "found: $e" }')
    p.out.append('found: ' + message(p, ['last one'], line))
    p.line('sub count($n) { my $t = 0; for my $i (1 .. $n) { try { $t += $i; die "skip\\n" if $i % 3 == 0; $t += 100 } catch ($e) { next } } return $t }')
    for n in (1, 3, 7):
        p.line(f'say count({n});')
        t = 0
        for i in range(1, n + 1):
            t += i
            if i % 3 == 0:
                continue
            t += 100
        p.say(str(t))


def state(p, rng):
    """What a die leaves, perl's way (T309): nothing of a list assignment,
    a push or a splice whose list died; an element made by an assigning
    operator before its right side died."""
    p.line('sub boom() { die "boom\\n" }')
    p.line('my @a = (1, 2, 3); my %h = (k => "v"); my ($x, $y) = (1, 2);')
    steps = [
        ('push @a, 4, boom();', lambda s: None),
        ('($x, $y) = (8, boom());', lambda s: None),
        ('@a = (9, boom());', lambda s: None),
        ('%h = (z => 1, q => boom());', lambda s: None),
        ('splice(@a, 0, 1, boom());', lambda s: None),
        ('my @b = sort { boom() } @a;', lambda s: None),
        ('@a = sort { boom() } @a;', lambda s: None),
        ('$h{new} .= boom();', lambda s: s['h'].setdefault('new', None)),
        ('$h{or} //= boom();', lambda s: s['h'].setdefault('or', None)),
        ('$a[5] += boom();', lambda s: s['a'].extend([None] * (6 - len(s['a'])))),
        ('$a[1] = boom();', lambda s: None),
        ('$h{k} = "w" . boom();', lambda s: None),
    ]
    st = {'a': [1, 2, 3], 'h': {'k': 'v'}}
    for code, effect in steps:
        p.line(f'try {{ {code} }} catch ($e) {{ print $e }}')
        effect(st)
        p.out.append('boom\n')
    p.line('say scalar(@a), " $x $y ", join(",", sort keys %h), " ", $h{k}, " ", defined $a[5] ? "d" : "u";')
    p.say(f"{len(st['a'])} 1 2 {','.join(sorted(st['h']))} v u")


def messages(p, rng):
    """Every way a message is made, caught and printed (T300, T301)."""
    for perl, values in MESSAGES:
        line = p.line(f'try {{ die {perl} }} catch ($e) {{ print "[", $e, "]\\n" }}' if perl else 'try { die } catch ($e) { print "[", $e, "]\\n" }')
        p.say('[', message(p, values, line), ']')
    p.line('my @e; my @two = ("a", "b"); my $n = 3;')
    for perl, values in [('@e', []), ('@two', ['a', 'b']), ('@two, "\\n"', ['a', 'b', '\n']), ('"n=$n"', ['n=3']),
                         ('"$n\\n"', ['3\n']), ('$n * 2, "x"', ['6', 'x']), ('$n / 2', ['1.5']), ('0.1 + 0.2', ['0.3']),
                         ('-$n', ['-3']), ('"@two"', ['a b']), ('join("-", @two), "!"', ['a-b', '!'])]:
        line = p.line(f'try {{ die {perl} }} catch ($e) {{ print "[", $e, "]\\n" }}')
        p.say('[', message(p, values, line), ']')
    line = p.line('sub where() { ... } try { where() } catch ($e) { print $e }')
    p.out.append(message(p, ['Unimplemented'], line))
    line = p.line('try { die "x" } catch ($e) { my $e = "inner"; print $e, "\\n" }')
    p.say('inner')
    p.line('my $kept = "outer"; try { die "y\\n" } catch ($kept) { $kept = "changed"; print "$kept\\n" } say $kept;')
    p.say('changed')
    p.say('outer')


BUILD = {3010: deep, 3011: loops, 3012: binders, 3013: nested, 3014: flow, 3015: state, 3016: messages}


def main(argv):
    program = argv[0] == '--program'
    n = int(argv[-1])
    p = Program(n)
    BUILD[n](p, random.Random(n))
    sys.stdout.write(p.text() if program else ''.join(p.out))


if __name__ == '__main__':
    main(sys.argv[1:])

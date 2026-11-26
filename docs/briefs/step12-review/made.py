#!/usr/bin/env python3
""""A hash is an array whose indexes are strings": for each place a value
can stand, does perl make an element that is read there, and is the answer
the same for a hash's (`$h{p}`, `@h{"p", "q"}`) as for an array's (`$a[5]`,
`@a[5, 6]`)? Prints every place, and marks those where the two differ.

    python3 docs/briefs/step12-review/made.py
"""
from common import perl

PLACES = {
    'my $v = E': 'my $v = E;',
    'my @l = (E)': 'my @l = (E);',
    'say E': 'my $o = ""; $o .= defined($_) ? 1 : 0 for (1); my @l = (E, 1); ',
    'for (E)': 'for my $v (E) { }',
    'for ((E, 1))': 'for my $v (E, 1) { }',
    'for (reverse E)': 'for my $v (reverse E) { }',
    'for (E x 1) list': 'for my $v ((E) x 1) { }',
    'for $_': '1 for E;',
    'map': 'my @r = map { 1 } E;',
    'grep': 'my @r = grep { 1 } E;',
    'sort block': 'my @r = sort { 0 } E, E2;',
    'sort plain': 'my @r = sort E, E2;',
    'reverse': 'my @r = reverse E, E2;',
    'join': 'my $j = join ",", 1, 2; my @r = (join(",", 1), E // 0);',
    'call arg': 'sub f(@x) { return 1 } f(E);',
    'call arg scalar param': 'sub f($x = 0, $y = 0) { return 1 } f(E);',
    'call in call': 'sub f(@x) { return 1 } sub g(@x) { return 1 } f(g(E));',
    'push': 'my @r; push @r, E;',
    'unshift': 'my @r; unshift @r, E;',
    'splice': 'my @r = (1); splice(@r, 0, 0, E);',
    'return': 'sub f() { return E; } my @r = f();',
    'return list': 'sub f() { return (E, 1); } my @r = f();',
    'last statement': 'sub f() { (E, 1) } my @r = f();',
    'list assign': 'my ($p, $q) = (E, 1);',
    'list slice': 'my @r = (E, 1)[0, 1];',
    'ternary in for': 'for my $v (1 ? E : 0) { }',
    'or in for': 'for my $v (E || 0) { }',
    'dor in for': 'for my $v (E // 0) { }',
    'defined': 'my $d = defined E0;',
    'x': 'my @r = (E) x 2;',
    'string': 'my $s = "S";',
    'exists other': 'my $d = E0 ? 1 : 0;',
    'slice index': 'my @z = (1, 2, 3); my @r = @z[E // 0, 0];',
    'range end in for': 'for my $v (0 .. (E0 // 0)) { }',
    'local-ish +=': 'my $t = 0; $t += E0 // 0;',
    'nested for': 'for my $v (map { $_ } E) { }',
    'grep in for': 'for my $v (grep { 1 } E) { }',
    'sort in for': 'for my $v (sort { 0 } E, E2) { }',
    'say list': 'my @r = (E)[0];',
    'slice-of-slice assign rhs': 'my ($p, $q); ($p, $q) = E;',
    'hash assign rhs': 'my %n = (k => E0);',
    'hash assign rhs slice': 'my %n = (E, 1, 2);',
    'slice key': 'my %n = (0 => 1); my @r = @n{E // 0, 0};',
    'elem key': 'my %n = (0 => 1); my $r = $n{E0 // 0};',
    'delete of other': 'my %n = (0 => 1); delete $n{E0 // 0};',
}
KINDS = {
    'hash element': ('my %h = (a => 1); ', '$h{p}', '$h{p}', '$h{q}', '$h{p}', 'say join ",", sort keys %h;', 'a\n'),
    'array element': ('my @a = (1); ', '$a[5]', '$a[5]', '$a[6]', '$a[5]', 'say scalar(@a);', '1\n'),
    'hash slice': ('my %h = (a => 1); ', '@h{"p", "q"}', None, '@h{"r", "s"}', '@h{"p", "q"}', 'say join ",", sort keys %h;', 'a\n'),
    'array slice': ('my @a = (1); ', '@a[5, 6]', None, '@a[7, 8]', '@a[5, 6]', 'say scalar(@a);', '1\n'),
}


def made(kind, place):
    head, e, e0, e2, s, show, unmade = KINDS[kind]
    text = PLACES[place]
    if 'E0' in text and e0 is None:
        return None
    body = text.replace('E0', e0 or '').replace('E2', e2).replace('E', e).replace('"S"', '"%s"' % s)
    out, err, code = perl('no warnings; ' + head + body + ' ' + show)
    if code != 0:
        return 'stops'
    return 'no' if out == unmade else 'MADE'


def main():
    n = 0
    print('%-28s %-8s %-8s %-8s %-8s' % ('', 'h elem', 'a elem', 'h slice', 'a slice'))
    for place in PLACES:
        r = [made(k, place) for k in KINDS]
        n += sum(x is not None for x in r)
        mark = ''
        if r[0] != r[1] or r[2] != r[3]:
            mark = '   <-- a hash and an array differ'
        print('%-28s %-8s %-8s %-8s %-8s%s' % tuple([place] + [x or '-' for x in r] + [mark]))
    print('%d programs' % n)


main()

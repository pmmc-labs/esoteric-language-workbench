#!/usr/bin/env python3
"""The oracle check's reading rule (`hash_order_shown` in t/checks.py) and
its eight seeds, against programs of step 12's language.

Part 1: programs that show a hash's order and that the reading rule passes.
For each shape, key names are searched for until perl prints one thing under
all eight of the check's seeds: that program passes both halves of the check,
and its "expected output" is an accident of those seeds. A ninth to
fortieth seed then shows the output moving.

Part 2: programs that show no order and that the reading rule rejects (what
the step's own tests will meet first).

    python3 docs/briefs/step12-review/reading.py
"""
import hashlib, importlib.util, itertools, os, sys
from common import perl, ROOT, TMP

spec = importlib.util.spec_from_file_location('checks', os.path.join(ROOT, 't/checks.py'))
checks = importlib.util.module_from_spec(spec)
sys.argv_saved, sys.argv = sys.argv, ['checks.py']
spec.loader.exec_module(checks)
sys.argv = sys.argv_saved
SEEDS = checks.SEEDS
MORE = [hashlib.sha256(str(n).encode()).hexdigest() for n in range(9, 41)]


def reads(body):
    path = os.path.join(TMP, 'reading.pl')
    open(path, 'w').write('use v5.42;\n' + body + '\n')
    return checks.hash_order_shown(path)


# Shapes that print an order. K is replaced by the hash's literal.
SHOWS = {
    'a sort over a slice of a list': 'my %h = (K); say sort { $a cmp $b } (keys %h)[0];',
    'a block of grep under sort says': 'my %h = (K); my @s = sort grep { say $_; 1 } keys %h;',
    'a block of map under sort collects': 'my %h = (K); my @o; my @s = sort map { push @o, $_; $_ } keys %h; say "@o";',
    'a comparator that logs': 'my %h = (K); my @o; my @s = sort { push @o, $a; $a cmp $b } keys %h; say "@o";',
    'a comparator that says': 'my %h = (K); my @s = sort { say "$a $b"; $a cmp $b } keys %h;',
    'sort of values under map, block stores': 'my %h = (K); my $first; my @s = sort map { $first //= $_; $_ } values %h; say $first;',
}
QUIET = {
    'the count: if (%h)': 'my %h = (a => 1); if (%h) { say "some"; }',
    'the count: my $n = %h': 'my %h = (a => 1); my $n = %h; say $n;',
    'the count: %h + 0': 'my %h = (a => 1); say %h + 0;',
    'a copy: my %g = %h': 'my %h = (a => 1, b => 2); my %g = %h; say join ",", map { "$_=$g{$_}" } sort keys %g;',
    'a %opts parameter': 'sub f($x, %o) { return join ",", map { "$_=$o{$_}" } sort keys %o } say f(1, a => 2, b => 3);',
    'a hash handed to a sub that sorts': 'sub f(%o) { return join ",", sort keys %o } my %h = (a => 1, b => 2); say f(%h);',
    'the count of keys, compared': 'my %h = (a => 1, b => 2); say "two" if keys %h == 2;',
    'the count of values in a sum': 'my %h = (a => 1, b => 2); say values(%h) + 0;',
    'a sum over values': 'my %h = (a => 1, b => 2); my $t = 0; for my $v (values %h) { $t += $v; } say $t;',
    'a hash from a map over keys': 'my %h = (a => 1, b => 2); my %g = map { $_ => $h{$_} * 2 } keys %h; say join ",", map { "$_=$g{$_}" } sort keys %g;',
    'delete in a loop over keys': 'my %h = (a => 1, b => 2); for my $k (keys %h) { delete $h{$k}; } say scalar(%h);',
    'scalar(%h)': 'my %h = (a => 1); say scalar(%h);',
    'scalar(keys %h)': 'my %h = (a => 1); say scalar(keys %h);',
    'a slice': 'my %h = (a => 1, b => 2); say join ",", @h{"a", "b"};',
    'exists and delete': 'my %h = (a => 1, b => 2); say exists $h{a} ? 1 : 0; say delete $h{b};',
    'for over sort keys': 'my %h = (a => 1, b => 2); for my $k (sort keys %h) { say "$k=$h{$k}"; }',
    '%h = ()': 'my %h = (a => 1); %h = (); say scalar(%h);',
}
NAMES = ['one', 'two', 'three', 'four', 'five', 'six', 'ant', 'bee', 'cat', 'dog', 'elk', 'fox', 'gnu', 'hen', 'a', 'b', 'c', 'd', 'e', 'x', 'y', 'z', 'k', 'n',
         'name', 'age', 'red', 'blue', 'green', 'apple', 'pear', 'plum', 'fig', 'kiwi', 'lime']


def outputs(body, seeds):
    """perl's (stdout, stderr, exit) under each seed, run as the check runs it: `run_perl`, its
    environment and no more. (With one seed perl's order still moves with the names in the
    environment and with the file's own path, so this is the only fair way to ask.)"""
    path = os.path.join(TMP, 'reading.pl')
    open(path, 'w').write('use v5.42;\n' + body + '\n')
    out = []
    for s in seeds:
        r = checks.run_perl([], path, {}, s, 10)
        out.append((r.stdout.decode(), r.stderr.decode(), r.returncode))
    return out


def passes_check(body):
    """True when `perl_says`, the check's own function, gives an expected output for a `same` test."""
    path = os.path.join(TMP, 'reading.pl')
    open(path, 'w').write('use v5.42;\n' + body + '\n')
    problem, expected = checks.perl_says(path, {}, 'same', 10)
    return problem is None


def main():
    print('Part 1: an order shown, the reading rule satisfied, and the eight seeds agreeing')
    for what, shape in SHOWS.items():
        found = None
        tried = 0
        for a, b in itertools.permutations(NAMES, 2):
            body = shape.replace('K', '%s => 1, %s => 2' % (a, b))
            if reads(body):
                print('  %s: the reading rule rejects it: %s' % (what, reads(body)))
                break
            tried += 1
            if passes_check(body):
                first = outputs(body, SEEDS)
                rest = set(outputs(body, MORE))
                if len(rest) > 1:
                    found = (body, first[0][0], sorted(o[0] for o in rest))
                    break
        if found:
            print('  %s (found at the %dth pair of keys)\n      %s\n      the eight seeds all print %r; seeds 9 to 40 print %r' % (what, tried, found[0], found[1], found[2]))
    print('Part 2: no order shown, and the reading rule rejects')
    for what, body in QUIET.items():
        r = reads(body)
        outs = set(outputs(body, SEEDS))
        print('  %-36s %s%s' % (what, 'rejected: ' + '; '.join(r) if r else 'passes', '' if len(outs) == 1 else '  (and perl\'s output moves!)'))


main()

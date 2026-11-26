#!/usr/bin/env python3
"""D27 against what perl keeps fixed. Each program prints `same` or `differ`
about two orders, never an order itself; perl is run under 40 seeds of 64
hex digits. Where perl says one thing under every seed and D27 (the order
of first storing; a copy keeps it) says the other, the program is fair and
D27 is WRONG for it; where perl's answer moves with the seed it is only
one more program that shows an order.

    python3 docs/briefs/step12-review/order.py
"""
import hashlib
from common import perl

SEEDS = [hashlib.sha256(str(n).encode()).hexdigest() for n in range(1, 41)]
K20 = ', '.join('k%d => %d' % (i, i) for i in range(20))
R20 = ', '.join('k%d => %d' % (i, i) for i in reversed(range(20)))
CMP = ' say join(",", @p) eq join(",", @q) ? "same" : "differ";'
PROGRAMS = {
    # name: (program, what D27 prints)
    'keys twice, nothing between': ('my %h = (K20); my @p = keys %h; my @q = keys %h;' + CMP, 'same'),
    'keys and values pair up': ('my %h = (K20); my @p = map { $h{$_} } keys %h; my @q = values %h;' + CMP, 'same'),
    'a copy keeps the order (my %g = %h)': ('my %h = (K20); my %g = %h; my @p = keys %h; my @q = keys %g;' + CMP, 'same'),
    'a copy of two keys': ('my %h = (a => 1, b => 2); my %g = %h; my @p = keys %h; my @q = keys %g;' + CMP, 'same'),
    'assigned to itself (%h = %h)': ('my %h = (K20); my @p = keys %h; %h = %h; my @q = keys %h;' + CMP, 'same'),
    'the same list twice, two hashes': ('my %h = (K20); my %g = (K20); my @p = keys %h; my @q = keys %g;' + CMP, 'same'),
    'the same keys stored in the other order': ('my %h = (K20); my %g = (R20); my @p = keys %h; my @q = keys %g;' + CMP, 'differ'),
    'two keys, the other order': ('my %h = (a => 1, b => 2); my %g = (b => 2, a => 1); my @p = keys %h; my @q = keys %g;' + CMP, 'differ'),
    'after a delete, the rest': ('my %h = (K20); my @p = grep { $_ ne "k7" } keys %h; delete $h{k7}; my @q = keys %h;' + CMP, 'same'),
    'after a store to an old key': ('my %h = (K20); my @p = keys %h; $h{k7} = 0; my @q = keys %h;' + CMP, 'same'),
    'after one new key, the old ones': ('my %h = (K20); my @p = keys %h; $h{new} = 0; my @q = grep { $_ ne "new" } keys %h;' + CMP, 'same'),
    'after 100 new keys, the old ones': ('my %h = (K20); my @p = keys %h; for my $i (1 .. 100) { $h{"n" . $i} = 0; } my @q = grep { length($_) < 4 && substr($_, 0, 1) eq "k" } keys %h;' + CMP, 'same'),
    'deleted and stored again is last': ('my %h = (K20); delete $h{k7}; $h{k7} = 7; my @q = keys %h; say $q[19] eq "k7" ? "same" : "differ";', 'same'),
    'the first key stored is first': ('my %h = (K20); my @q = keys %h; say $q[0] eq "k0" ? "same" : "differ";', 'same'),
    'a %opts parameter keeps the order': ('sub f(%o) { return join ",", keys %o } my %h = (K20); my @p = (join ",", keys %h); my @q = (f(%h));' + CMP, 'same'),
    'keys after a loop over values': ('my %h = (K20); my @p = keys %h; my $t = 0; for my $v (values %h) { $t += $v; } my @q = keys %h;' + CMP, 'same'),
    'sorted by a tie': ('my %h = (K20); my @p = sort { 0 } keys %h; my @q = keys %h;' + CMP, 'same'),
}


def main():
    for name, (prog, d27) in PROGRAMS.items():
        prog = prog.replace('K20', K20).replace('R20', R20)
        got = [perl(prog, seed=s) for s in SEEDS]
        outs = sorted({g[0].strip() + (' WARNS' if g[1] else '') for g in got})
        tally = {o: sum(1 for g in got if g[0].strip() + (' WARNS' if g[1] else '') == o) for o in outs}
        verdict = 'agree' if outs == [d27] else ('perl moves with the seed' if len(outs) > 1 else 'FAIR, AND D27 DIFFERS')
        print('%-42s perl %-28s D27 %-7s %s' % (name, tally, d27, verdict))


main()

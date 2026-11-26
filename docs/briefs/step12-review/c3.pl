use v5.42;
# C3: a `same` test by the oracle check's rules (every `keys` is under a
# sort, and perl prints one thing under the check's eight seeds) on which
# D27 must differ: the order of first storing says `same` three times,
# and perl says `differ` three times under 40 seeds of 40.
my %h = (k0 => 0, k1 => 1, k2 => 2, k3 => 3, k4 => 4, k5 => 5, k6 => 6, k7 => 7, k8 => 8, k9 => 9,
         k10 => 10, k11 => 11, k12 => 12, k13 => 13, k14 => 14, k15 => 15, k16 => 16, k17 => 17, k18 => 18, k19 => 19);
my @p = sort { 0 } keys %h;
say $p[0] eq "k0" && $p[19] eq "k19" ? "same" : "differ";    # the first stored is first, the last last
for my $i (1 .. 100) {
    $h{"n" . $i} = 0;
}
my @q = grep { substr($_, 0, 1) eq "k" } sort { 0 } keys %h;
say join(",", @p) eq join(",", @q) ? "same" : "differ";      # new keys leave the old ones in their order
delete $h{k7};
$h{k7} = 7;
my @r = sort { 0 } keys %h;
say $r[119] eq "k7" ? "same" : "differ";                     # deleted and stored again is last

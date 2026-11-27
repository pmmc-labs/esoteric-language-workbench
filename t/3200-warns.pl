# kind: warns
# warn, its messages and its value (15b; D148, T314).
use v5.42;
say "start";
warn "plain";
warn "with newline\n";
warn;
warn "";
my @none;
warn @none;
warn "a", 1, 2.5, true;
my $r = warn "valued\n";
say "warn gave $r";
my $n = warn("in a sum\n") + 1;
say $n;
for my $i (1 .. 3) { warn "round $i\n" if $i != 2 }
say "end";

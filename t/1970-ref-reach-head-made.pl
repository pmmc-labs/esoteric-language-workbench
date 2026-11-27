# kind: refused
# perl runs it, and says nothing.
use v5.42;
my $r;
my @l = ($r, ($r->[0] = 1));

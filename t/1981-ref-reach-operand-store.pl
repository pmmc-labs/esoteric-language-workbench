# kind: refused
# perl runs it: '10\n'.
use v5.42;
my $r = [1, 2];
my $s = $r;
say $r->[0] + ($s->[0] = 5);

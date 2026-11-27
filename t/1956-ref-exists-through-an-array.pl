# kind: refused
# perl runs it: '1\n'.
use v5.42;
my $r = [1, 2];
say exists $r->[0] ? 1 : 0;

# kind: refused
# perl runs it: '55\n'.
use v5.42;
my @a = (1, 2, 3);
my $r = \@a;
say $r->[0], ($a[0] = 5);

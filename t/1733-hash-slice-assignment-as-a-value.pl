# kind: refused
# perl gives the count of the right side: 3 (D78).
use v5.42;
my @a = (1, 2, 3);
my $n = (@a[0, 1] = (5, 6, 7));
say $n;

# kind: refused
# perl gives the count of the right side, 3 (T151, D78).
use v5.42;
my @a = (1, 2, 3);
my $n = (my ($p, $q) = @a);
say $n;

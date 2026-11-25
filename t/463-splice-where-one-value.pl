# kind: refused
# perl gives the last element removed, 2 (T151).
use v5.42;
my @a = (1, 2, 3);
my $s = splice(@a, 0, 2);
say $s;

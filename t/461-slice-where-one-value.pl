# kind: refused
# perl gives the last element of the slice, 2 (T151).
use v5.42;
my @a = (1, 2, 3);
my $x = @a[0, 1];
say $x;

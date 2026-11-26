# kind: refused
# perl prints 6 (T213).
use v5.42;
my @a = (1, 2, 3);
my $n = ($a[0] += 1) + ($a[0] += 1);
say $n;

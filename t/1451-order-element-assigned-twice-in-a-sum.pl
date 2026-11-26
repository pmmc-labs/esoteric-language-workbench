# kind: refused
# perl prints 14: each assignment is the element, read when the sum runs (T213).
use v5.42;
my @a = (1);
my $n = ($a[0] = 5) + ($a[0] = 7);
say $n;

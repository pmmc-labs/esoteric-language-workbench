# kind: refused
# perl prints 10: the sub stores 9 before the sum reads the element (T213).
use v5.42;
my @a = (1);
sub nine() { $a[0] = 9; return 1; }
my $n = ($a[0] = 5) + nine();
say $n;

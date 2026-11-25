# kind: refused
# perl prints 2.
use v5.42;
sub f() { return 1; }
my $x = f + 1;
say $x;

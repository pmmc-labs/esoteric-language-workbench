# kind: refused
# perl returns the list to a list, and the count to a scalar (T16): step 10.
use v5.42;
my @a = (1, 2, 3);
sub f() { return @a; }
my $n = f();
say $n;

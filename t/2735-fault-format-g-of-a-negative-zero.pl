# kind: fault
# perl prints -0 here, and 0 when the zero has been an integer (T267).
use v5.42;
my $z = 0.0;
say sprintf("%g", $z);
say sprintf("%g", -$z);

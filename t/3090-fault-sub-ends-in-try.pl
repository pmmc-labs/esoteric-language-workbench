# kind: fault
# A sub that ends in a try has no value (D18, T65): perl gives 42.
use v5.42;
sub f() { try { my $x = 42 } catch ($e) { } }
say "[", f(), "]";

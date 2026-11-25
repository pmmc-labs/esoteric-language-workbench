# kind: refused
# $a and $b are sort's, and perl lets them by without a my (D55, T53).
use v5.42;
my $a = 1;
say $a;

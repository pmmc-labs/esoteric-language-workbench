# kind: refused
# perl assigns to whichever the ? : gives. Values flow, and places
# don't (D17, D56).
use v5.42;
my $x;
my $y;
(1 ? $x : $y) = 8;

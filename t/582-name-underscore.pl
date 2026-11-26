# kind: refused
# $_ is the value a for, a map or a grep gives its block, and no variable
# of the program's (D17, D55).
use v5.42;
my $x = 1;
say $_;

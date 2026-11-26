# kind: refused
# perl does not compile it: %x is not declared (T203).
use v5.42;
my $x = 3;
say "$x{a}";

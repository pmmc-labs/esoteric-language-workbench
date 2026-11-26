# kind: refused
# perl does not compile it: @x is not declared (T201).
use v5.42;
my $x = 3;
say "$x[1]";

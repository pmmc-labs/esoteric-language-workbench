# kind: refused
# perl takes it, and the variable is not seen by the statement before
# the if: it is declared after it.
use v5.42;
my $y = 1;
say $y if my $x = $y;

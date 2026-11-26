# kind: refused
# perl reads `$x`, over the end of the line (T200).
use v5.42;
my $x = 3;
say "$
x";

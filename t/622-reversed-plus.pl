# kind: refused
# perl warns: Reversed += operator (T127).
use v5.42;
my $y = 2;
my $x = 0;
$x =+ $y;
say $x;

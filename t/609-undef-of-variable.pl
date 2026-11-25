# kind: refused
# undef $x makes $x undefined, to perl: undef takes what follows for
# its argument (T105).
use v5.42;
my $x = 1;
my $y = undef $x;

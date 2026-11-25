# kind: refused
# The left of && is tested for truth: perl warns, Found = in
# conditional (T112, D53).
use v5.42;
my $x = 0;
say(($x = 5) && $x);

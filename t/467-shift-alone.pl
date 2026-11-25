# kind: refused
# perl shifts the program's arguments, and gives undef (T152).
use v5.42;
my $x = shift;

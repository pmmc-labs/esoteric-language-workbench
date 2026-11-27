# kind: refused
# perl runs it, and says nothing.
use v5.42;
my @l = map { { n => $_ } } (1, 2);

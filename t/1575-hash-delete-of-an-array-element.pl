# kind: refused
# perl's delete takes it: 1. Not in the language.
use v5.42;
my @a = (1, 2, 3);
say delete $a[0];

# kind: refused
# perl's exists takes it: 1. Not in the language.
use v5.42;
my @a = (1, 2, 3);
say exists $a[0] ? 1 : 0;

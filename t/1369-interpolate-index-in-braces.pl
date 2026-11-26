# kind: refused
# perl warns: Ambiguous use of ${a[...]} resolved to $a[...] (T201).
use v5.42;
my @a = (1, 2, 3);
say "${a[1]}";

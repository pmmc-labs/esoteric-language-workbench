# kind: refused
# perl's own $\, indexed as a hash (T204).
use v5.42;
my $x = 3;
say "$\{x}";

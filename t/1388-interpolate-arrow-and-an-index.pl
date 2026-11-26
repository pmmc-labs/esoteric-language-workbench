# kind: refused
# perl dies: not an ARRAY reference (T203).
use v5.42;
my $x = 3;
say "$x->[0]";

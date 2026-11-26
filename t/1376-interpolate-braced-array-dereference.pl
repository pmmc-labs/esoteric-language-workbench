# kind: refused
# perl dies: not an ARRAY reference.
use v5.42;
my $x = 3;
say "@{$x}";

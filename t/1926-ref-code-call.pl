# kind: refused
# perl dies: Not a CODE reference.
use v5.42;
my $r = [1, 2];
say $r->(1);

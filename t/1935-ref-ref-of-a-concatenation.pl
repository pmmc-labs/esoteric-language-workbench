# kind: refused
# perl runs it: '\n'.
use v5.42;
my $r = [1, 2];
say ref $r . "x";

# kind: refused
# perl runs it: '3\n'.
use v5.42;
my %g = (x => {y => 3});
say $g{x} {y};

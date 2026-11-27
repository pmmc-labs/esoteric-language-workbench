# kind: refused
# perl does not compile it: Multidimensional hash lookup is disabled near '2}'.
use v5.42;
my $h = {};
say $h->{1, 2};

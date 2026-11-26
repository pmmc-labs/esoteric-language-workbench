# kind: refused
# perl takes the count of an empty hash: 0.
use v5.42;
my $n = my %g;
say $n;

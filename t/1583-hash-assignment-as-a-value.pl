# kind: refused
# perl gives the count of the right side: 2 (D78).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $n = (%h = (a => 1));
say $n;

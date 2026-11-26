# kind: refused
# perl gives the last value it deleted: 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $x = delete @h{"a", "b"};
say $x;

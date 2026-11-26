# kind: refused
# perl gives the last: 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $x = @h{"a", "b"};
say $x;

# kind: refused
# perl: 8.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = map { $_ } %h;
say scalar(@l);

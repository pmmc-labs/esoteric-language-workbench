# kind: refused
# perl would read a freed value (D102); only a sub can hold the assignment, which is a statement.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
sub clear() { %h = (); return 1 }
my @l = ($h{a}, clear());
say scalar(@l);

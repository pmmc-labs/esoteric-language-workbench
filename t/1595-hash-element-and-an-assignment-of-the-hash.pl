# kind: refused
# perl: 2. An assignment to the hash is a change for D76 (D102); only a sub can hold one, since it is a statement.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
sub clear() { %h = (); return 1 }
my @l = ($h{a}, clear());
say scalar(@l);

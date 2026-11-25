# kind: refused
# perl gives $r 9: the variable is read when the list is assigned (T157, D76).
use v5.42;
my $x = 1;
sub bump() { $x = 9; return 5; }
my ($r, $s) = ($x, bump());
say $r;

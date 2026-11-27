# kind: refused
# perl warns of a precedence problem.
use v5.42;
my $x = 0;
if ($x) { say 1; } elsif (die "e") { say 2; }

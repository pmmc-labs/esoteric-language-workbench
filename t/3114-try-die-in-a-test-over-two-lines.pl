# kind: refused
# perl: the line of the if; refused all the same.
use v5.42;
my $x;
if ($x
  // die "u") { say 1; }

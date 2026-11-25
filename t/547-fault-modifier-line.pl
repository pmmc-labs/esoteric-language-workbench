# kind: fault
# A fault in the test of a modifier names the line its statement starts
# on, not the line of the if: perl warns of this undef at line 7.
use v5.42;
my $u;
say "before";
say "not reached"
  if
  $u + 1;

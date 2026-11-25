# kind: fault
# A fault in the test of a while modifier names the line its statement
# starts on, not the line of the while: perl dies here at line 8 too.
use v5.42;
my $i = 0;
say "before";

$i++
  while
  10 / (2 - $i) > 0;
say "not reached";

# kind: refused
# perl makes a hash in the element, and a reference to it (step 13).
use v5.42;
my %g;
$g{x}{y} = 1;

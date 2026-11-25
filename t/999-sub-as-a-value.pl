# kind: refused
# perl makes a code reference (step 14).
use v5.42;
my $f = sub ($x) { return $x; };

# kind: fault
# An undef in a die's list is D48's fault: perl warns.
use v5.42;
my $u;
say "before";
try { die "x", $u } catch ($e) { print $e }

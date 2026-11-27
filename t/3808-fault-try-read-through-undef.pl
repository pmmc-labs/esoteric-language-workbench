# kind: fault
# Reading through undef is D107's fault, which a try does not catch: perl makes the hash and runs on.
use v5.42;
my %seen;
try { say "in"; my $n = $seen{a}{b}; } catch ($e) { say "caught"; }

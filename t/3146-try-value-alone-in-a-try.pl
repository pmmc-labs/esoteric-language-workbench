# kind: refused
# perl warns: Useless use of addition in void context.
use v5.42;
my $x = 1;
try { $x + 1; } catch ($e) { say "c"; }

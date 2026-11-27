# kind: refused
# perl does not compile it: syntax error.
use v5.42;
my $x = try { 1 } catch ($e) { 2 };

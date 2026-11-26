use v5.42;
# P2: `%` alone "takes and names nothing", and still dies for an odd count.
sub f($x, %) { return "ok $x" }
say f(1);
say f(1, 2, 3);
say f(1, 2);       # one left over: perl dies here
say "not reached";

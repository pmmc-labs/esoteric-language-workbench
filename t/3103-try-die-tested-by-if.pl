# kind: refused
# perl warns of a precedence problem.
use v5.42;
if (die "u") { say 1; }

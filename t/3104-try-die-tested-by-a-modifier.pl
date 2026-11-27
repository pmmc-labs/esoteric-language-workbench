# kind: refused
# perl warns of a precedence problem.
use v5.42;
say 1 if die "q";

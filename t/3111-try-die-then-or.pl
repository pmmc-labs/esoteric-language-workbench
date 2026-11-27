# kind: refused
# perl warns of a precedence problem, and dies x.
use v5.42;
die "x" or say 1;

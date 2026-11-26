# kind: refused
# perl does not compile it: Global symbol "%nope" requires explicit package name.
use v5.42;
say scalar(%nope);

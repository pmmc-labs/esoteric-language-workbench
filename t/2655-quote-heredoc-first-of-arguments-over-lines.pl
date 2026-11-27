# kind: refused
# perl takes the next line into the body, and does not compile the rest: Global symbol "@a" requires explicit package name (T284).
use v5.42;
my @a = (<<A,
"x");
body
A
say scalar(@a);

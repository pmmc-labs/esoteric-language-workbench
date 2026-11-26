# kind: refused
# perl leaves one out, and warns: Odd number of elements in hash assignment.
use v5.42;
my %g = (a => 1, => 2);

# kind: refused
# perl makes the string: a. One rule for every word (D102).
use v5.42;
my %g = (a # the key
  => 1);
say join(",", sort keys %g);

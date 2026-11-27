# kind: fault
# perl gives the count chomp took: 1. Here chomp is no value, a sub's either (D130).
use v5.42;
sub f($s) { chomp $s }
say "before";
say f("a\n");

# kind: fault
# A list assignment is a statement and has no value (D78): perl gives a sub
# that ends in one the count of its right side (T257).
use v5.42;
my @a;
sub f($n) { my ($p, $q) = (7, 8) }
f(3);
say "void";
my $v = f(3);
say $v;

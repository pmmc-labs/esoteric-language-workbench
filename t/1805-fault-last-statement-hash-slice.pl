# kind: fault
# A list assignment is a statement and has no value (D78): perl gives a sub
# that ends in one the count of its right side (T257).
use v5.42;
my %h;
sub f($n) { @h{"p", "q"} = (1, 2) }
f(3);
say "void";
my $v = f(3);
say $v;

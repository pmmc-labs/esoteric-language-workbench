# kind: refused
# perl gives the last word, and warns: Useless use of a constant ("a") in void context.
use v5.42;
my $x = qw(a b);
say $x;

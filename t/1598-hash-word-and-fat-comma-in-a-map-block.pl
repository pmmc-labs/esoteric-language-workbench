# kind: refused
# perl guesses a hash, and does not compile it: syntax error.
use v5.42;
my @a = (1, 2, 3);
my %g = map { a => $_ } @a;
say join(",", sort keys %g);

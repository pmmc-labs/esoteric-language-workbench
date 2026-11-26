# kind: refused
# perl guesses a block: 1,2,3. Refused for the comma (D102).
use v5.42;
my @a = (1, 2, 3);
my %g = map { $_ => 1 } @a;
say join(",", sort keys %g);

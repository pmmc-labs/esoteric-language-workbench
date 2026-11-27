# kind: refused
# perl gives 1, what printf returns.
use v5.42;
my $r = printf("%s\n", "b");

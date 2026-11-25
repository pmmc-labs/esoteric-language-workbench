# kind: refused
# perl warns: "my" variable $x masks earlier declaration in same scope.
use v5.42;
my $x = 1;
my $x = 2;
say $x;

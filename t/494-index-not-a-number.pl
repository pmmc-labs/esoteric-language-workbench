# kind: refused
# perl warns as it compiles: Argument "x" isn't numeric in array element.
use v5.42;
my @a = (1, 2, 3);
say $a["2"];
say $a["x"];

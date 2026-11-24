# kind: refused
# perl reads `$x` in a double-quoted string as a variable (T34).
use v5.42;
say "cost: $x";

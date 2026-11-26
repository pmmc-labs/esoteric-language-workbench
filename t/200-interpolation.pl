# kind: refused
# perl reads `$x` in a double-quoted string as a variable (T34), and it
# is not declared.
use v5.42;
say "cost: $x";

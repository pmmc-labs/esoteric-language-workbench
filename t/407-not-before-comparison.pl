# kind: refused
# perl 5.42 prints 1, and warns as it compiles: `Possible precedence problem between !
# and numeric eq (==)`. It is `(!undef) == 1` (T115).
use v5.42;
say(!(undef) == 1);

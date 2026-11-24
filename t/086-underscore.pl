# kind: refused
# perl prints 10 and warns of a misplaced underscore (T82).
use v5.42;
say 1__0;

# kind: refused
# perl prints 2, `(not 0) + 1`.
use v5.42;
say(not(0) + 1);

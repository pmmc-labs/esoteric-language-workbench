# kind: refused
# perl prints an empty line, with a warning from say: this is undef of a glob called 2,
# and no multiplication (T105).
use v5.42;
say undef * 2;

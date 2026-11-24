# kind: refused
# perl prints 8: a hex float, which the language may have later.
use v5.42;
say 0x1p3;

# kind: refused
# perl prints 18: the number 0x1, joined to 8 (T78).
use v5.42;
say 0x1.8;

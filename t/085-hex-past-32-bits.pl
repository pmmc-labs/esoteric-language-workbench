# kind: refused
# perl prints 4294967296 and warns that the literal is not portable (D15).
use v5.42;
say 0x100000000;

# kind: refused
# perl prints 1: `\x` with no digit is a NUL, in silence (T86).
use v5.42;
say length "\x";

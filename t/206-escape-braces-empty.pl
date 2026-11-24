# kind: refused
# perl makes `\x{}` a NUL, in silence (T86).
use v5.42;
say "\x{}";

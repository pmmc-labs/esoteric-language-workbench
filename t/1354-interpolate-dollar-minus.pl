# kind: refused
# perl's own $-: a0b, in silence (T204).
use v5.42;
say "a$-b";

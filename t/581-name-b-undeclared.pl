# kind: refused
# perl prints nothing and warns of an uninitialized value: $b needs no
# my, even under strict (D55, T53).
use v5.42;
say $b;

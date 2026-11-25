# kind: refused
# perl prints abcdef: `not` takes the rest of the list, `0, 1`, and what is left is
# substr("abcdef", "") (D51).
use v5.42;
say substr("abcdef", not 0, 1);

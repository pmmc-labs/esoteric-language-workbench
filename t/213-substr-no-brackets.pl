# kind: refused
# perl prints bc: a list operator's arguments without brackets (D41).
use v5.42;
say substr "abc", 1;

# kind: refused
# perl prints 0, and warns of a useless constant: it is `(say 0) or 2` (T106).
use v5.42;
say 0 or 2;

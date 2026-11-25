# kind: refused
# perl prints 1 and says nothing: it is `(say true) and false` (T106).
use v5.42;
say true and false;

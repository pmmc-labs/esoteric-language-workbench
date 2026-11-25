# kind: refused
# perl prints 5, and the sub has @_ (D17).
use v5.42;
sub f { return 5; }
say f();

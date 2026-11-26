# kind: refused
# With no signature a sub's arguments are in @_, to perl, and @_ is not
# in the language (D17, D105): the sub names them in a signature.
use v5.42;
sub add { return $_[0] + $_[1]; }
say add(1, 2);

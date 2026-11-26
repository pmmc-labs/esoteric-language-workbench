# kind: refused
# $_[0] is an element of @_ (T192).
use v5.42;
my @r = map { $_[0] } (1);

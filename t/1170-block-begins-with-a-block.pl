# kind: refused
# perl: an anonymous hash, with a warning (T192).
use v5.42;
my @r = map { { 5 } } (1);

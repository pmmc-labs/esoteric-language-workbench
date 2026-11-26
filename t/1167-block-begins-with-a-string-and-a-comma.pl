# kind: refused
# A hash, to perl's guess, and a syntax error (T175, T54, D21).
use v5.42;
my @r = map { "a", $_ } (1, 2);

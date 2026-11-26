# kind: refused
# perl warns: Useless use.
use v5.42;
my @r = map { $_ + 1; $_ } (1, 2);

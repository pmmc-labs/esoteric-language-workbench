# kind: refused
# perl gives the empty string where the test fails (T176).
use v5.42;
my @r = map { if ($_ > 1) { $_ } } (1, 2, 3);

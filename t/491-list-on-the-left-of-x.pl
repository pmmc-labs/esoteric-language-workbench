# kind: refused
# perl repeats the last value: one string, 22 (T168).
use v5.42;
my $s = (1, 2) x 2;
say $s;

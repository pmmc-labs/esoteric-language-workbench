# kind: fault
# perl compiles it, and dies under strict. Refused until step 13a, and a
# fault since (D107).
use v5.42;
my @a = (1);
say $a[0][0];

# kind: refused
# A loop over $_ again (step 10 will say whether).
use v5.42;
my @a = (1, 2);
say 1 for @a;

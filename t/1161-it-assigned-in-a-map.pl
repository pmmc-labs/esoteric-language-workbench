# kind: refused
# perl: the array is 24 after (T180).
use v5.42;
my @a = (1, 2);
my @r = map { $_ *= 2 } @a;
say @a;

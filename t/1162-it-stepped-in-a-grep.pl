# kind: refused
# perl: 23 (T180).
use v5.42;
my @a = (1, 2);
my @r = grep { $_++ } @a;
say @a;

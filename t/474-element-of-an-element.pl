# kind: refused
# perl compiles it, and dies under strict: an array holds no array until step 13.
use v5.42;
my @a = (1);
say $a[0][0];

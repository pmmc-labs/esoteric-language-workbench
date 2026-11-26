# kind: refused
# perl warns: an element at the smallest integer (T211).
use v5.42;
my @a = (1, 2, 3);
say "$a[9223372036854775808]";

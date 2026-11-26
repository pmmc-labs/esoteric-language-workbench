# kind: refused
# perl prints -1, in silence: the last index of @a:: (T199).
use v5.42;
my @a = (1, 2, 3);
say "$#a::";

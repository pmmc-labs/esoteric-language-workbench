# kind: refused
# perl prints 13: -010 is -8 (T211).
use v5.42;
my @a = (1 .. 20);
say "$a[-010]";

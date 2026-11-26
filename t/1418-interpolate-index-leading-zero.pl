# kind: refused
# perl prints 9: 010 is octal (T211).
use v5.42;
my @a = (1 .. 20);
say "$a[010]";

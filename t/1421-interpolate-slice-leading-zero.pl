# kind: refused
# perl prints 8 9 (T211).
use v5.42;
my @a = (0 .. 20);
say "@a[010, 011]";

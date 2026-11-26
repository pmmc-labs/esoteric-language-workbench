# kind: refused
# perl does not compile it: Illegal octal digit (T211).
use v5.42;
my @a = (1 .. 20);
say "$a[08]";

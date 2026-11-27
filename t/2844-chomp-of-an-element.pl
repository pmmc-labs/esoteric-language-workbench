# kind: refused
# perl chomps the element.
use v5.42;
my @a = ("a\n");
chomp $a[0];

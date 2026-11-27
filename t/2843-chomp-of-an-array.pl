# kind: refused
# perl chomps each element.
use v5.42;
my @a = ("a\n");
chomp(@a);

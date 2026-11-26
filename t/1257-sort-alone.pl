# kind: refused
# perl: Useless use of sort in void context.
use v5.42;
my @a = (3, 1, 2);
sort @a;

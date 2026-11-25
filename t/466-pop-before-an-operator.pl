# kind: refused
# perl does not compile it: pop on scalar is now forbidden (T152).
use v5.42;
my @a = (1, 2, 3);
my $x = pop @a + 1;

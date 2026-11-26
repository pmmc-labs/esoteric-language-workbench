# kind: refused
# perl: 23.
use v5.42;
my @a = (1, 2);
$_++ for @a;
say @a;

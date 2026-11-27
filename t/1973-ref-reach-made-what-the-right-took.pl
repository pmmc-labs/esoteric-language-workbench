# kind: refused
# perl runs it, and says nothing.
use v5.42;
my @a = (undef);
$a[0][0] = $a[0];

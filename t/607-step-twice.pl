# kind: refused
# perl doesn't compile it: Can't modify postincrement in postincrement.
use v5.42;
my $x = 1;
$x++++;

# kind: refused
# perl doesn't compile it either: the blocks of an if are in braces.
use v5.42;
my $x = 1;
if ($x) say 1;

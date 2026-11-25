# kind: refused
# perl doesn't compile it either: the block of a loop is in braces.
use v5.42;
my $i = 0;
while ($i++ < 3) print $i;

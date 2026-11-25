# kind: refused
# perl warns: Found = in conditional, should be == (T112, D53).
use v5.42;
my $i = 0;
$i++ until $i = 3;

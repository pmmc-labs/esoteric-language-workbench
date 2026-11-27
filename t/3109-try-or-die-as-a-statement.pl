# kind: refused
# perl dies zero (D146: die ... unless ...).
use v5.42;
my $x = 0;
$x or die "zero\n";

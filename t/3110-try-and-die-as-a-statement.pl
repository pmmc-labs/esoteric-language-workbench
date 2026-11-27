# kind: refused
# perl dies one.
use v5.42;
my $x = 1;
$x and die "one\n";

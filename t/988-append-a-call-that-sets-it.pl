# kind: refused
# perl prints b3 (D69: the left of .= is the first piece).
use v5.42;
my $x = "a";
sub set() { $x = "b"; return 3; }
$x .= set();
say $x;

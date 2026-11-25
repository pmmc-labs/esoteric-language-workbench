# kind: refused
# perl prints b-1: ping and pong call each other, and pong sets $x (D69).
use v5.42;
my $x = "a";
sub ping($n) { return $n ? pong($n - 1) : 0; }
sub pong($n) { $x = "b"; return $n ? ping($n - 1) : 1; }
say $x . "-" . ping(3);

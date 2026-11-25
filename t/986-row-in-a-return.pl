# kind: refused
# perl returns b-c (D69).
use v5.42;
my $x = "a";
sub ch() { $x = "b"; return "c"; }
sub row() { return $x . "-" . ch(); }
say row();

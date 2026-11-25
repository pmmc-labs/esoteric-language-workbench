# kind: refused
# perl prints b-c: deep calls dflt, whose default calls ch (D69).
use v5.42;
my $x = "a";
sub ch() { $x = "b"; return "c"; }
sub dflt($p = ch()) { return $p; }
sub deep() { return dflt(); }
say $x . "-" . deep();

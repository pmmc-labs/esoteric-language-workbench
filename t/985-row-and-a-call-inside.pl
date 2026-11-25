# kind: refused
# perl prints b-2: the call is inside a builtin, in the later piece (D69).
use v5.42;
my $x = "a";
sub ch() { $x = "b"; return "c"; }
say $x . "-" . (1 + length(ch()));

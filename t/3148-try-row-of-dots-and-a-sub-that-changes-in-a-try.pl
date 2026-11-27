# kind: refused
# perl reads $x after ch has run: bc (D69).
use v5.42;
my $x = "a";
sub ch() { try { $x = "b"; } catch ($e) { } return "c"; }
say $x . ch();

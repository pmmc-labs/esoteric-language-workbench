# kind: refused
# perl prints b-c: the row is one operation, and reads $x after ch has run (T132, D69).
use v5.42;
my $x = "a";
sub ch() { $x = "b"; return "c"; }
say $x . "-" . ch();

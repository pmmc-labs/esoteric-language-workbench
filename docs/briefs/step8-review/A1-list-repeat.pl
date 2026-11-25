use v5.42;
sub g($p = "d") { return "[" . $p . "]" }
sub cnt($p = "-", $q = "-", $r = "-") { return $p . "," . $q . "," . $r }
sub three() { return ("a") x 3 }
sub last2($x) { ($x) x 2 }
my $n = 0;
say g(("a") x $n);
say cnt(("a") x $n, "z");
say cnt(("a") x 2);
say cnt(1 ? ("a") x 2 : "b");
say cnt(0 || ("a") x 2);
say cnt(three());
say cnt(last2("k"));
my $s = three(); say $s;

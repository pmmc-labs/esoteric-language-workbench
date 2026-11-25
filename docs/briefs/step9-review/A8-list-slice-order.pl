use v5.42;
# A list slice works its indexes out before its list.
sub p($v) { print "<", $v, ">"; return $v }
say((p(10), p(20))[p(1)]);
my $i = 0;
say(($i, 5)[$i++]);
my @a = (1, 2, 3);
sub sh() { shift(@a); return 0 }
say((@a)[sh()]);

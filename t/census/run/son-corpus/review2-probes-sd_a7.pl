use v5.42;
sub f { my $n = shift; my $r = "no"; if ($n > 1) { $r = "yes" } return $r } my $r = "keep"; print f(2), $r, f(0), "\n";

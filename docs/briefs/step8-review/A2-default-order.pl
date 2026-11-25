use v5.42;
my $g = 1;
sub bump() { $g = 9; return 5 }
sub f($x //= bump(), $y = 0) { return $x . "," . $y }
say f(undef, $g);
$g = 1;
sub h($x ||= bump(), $y = 0) { return $x . "," . $y }
say h(0, $g);
$g = 1;
say f(undef, $g + 0);

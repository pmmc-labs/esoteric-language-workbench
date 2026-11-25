use v5.42;
sub e($p) { return $p + 10 }
sub id($p) { return $p }
my $r;
$r = - -e(3); say defined($r) ? $r : "u";
$r = !-e(3); say defined($r) ? $r : "u";
$r = (-e(3)); say defined($r) ? $r : "u";
$r = id(-e(3)); say defined($r) ? $r : "u";
$r = -e (3); say defined($r) ? $r : "u";
$r = - e(3); say $r;
$r = -
e(3); say $r;

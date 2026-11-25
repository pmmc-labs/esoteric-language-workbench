use v5.42;
sub t($p) { return $p + 10 }
sub e($p) { return $p + 10 }
my $n = -t(2);
say defined($n) ? "d[" . $n . "]" : "u";
$n = -e(2);
say defined($n) ? "d[" . $n . "]" : "u";

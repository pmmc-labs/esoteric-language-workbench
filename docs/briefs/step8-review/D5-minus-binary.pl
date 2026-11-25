use v5.42;
sub e($p) { return $p + 10 }
sub id($p) { return $p }
my $r = id(26) -e(3);
say $r;

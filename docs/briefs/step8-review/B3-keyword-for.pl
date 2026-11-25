use v5.42;
sub for($p) { return $p + 10 }
my $r = 1 + for(3);
say $r;

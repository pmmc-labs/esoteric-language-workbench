use v5.42;
my $k; sub g { return $k } my $v = g() // "u"; print "$v\n";

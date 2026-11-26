use v5.42;
my $x = 10; sub g { return $x } $x = 20; print g(), "\n";

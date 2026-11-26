use v5.42;
my $x=1; my $n = $x + (sub { $x = 5 })->(); print "$n\n";

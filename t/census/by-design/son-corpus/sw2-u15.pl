use v5.42;
my $x = 5; { local $_ = 3; $x += $_ } print "$x\n";

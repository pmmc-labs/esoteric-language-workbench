use v5.42;
my $x; substr($x = "abc", 0, 1) = "z"; print "$x\n";

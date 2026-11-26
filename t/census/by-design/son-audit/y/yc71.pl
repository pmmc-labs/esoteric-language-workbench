use v5.42;
my $x="a"; sub f { $x="z"; "b" } my $s = $x . f(); print "$s\n";

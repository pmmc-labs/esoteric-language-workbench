use v5.42;
my $x="a"; sub f { $x="z"; "b" } my @l = ($x, f()); print "@l\n";

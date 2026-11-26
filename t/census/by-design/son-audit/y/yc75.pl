use v5.42;
my $x="a"; sub f { $x="z"; "b" } print $x, f(), "\n";

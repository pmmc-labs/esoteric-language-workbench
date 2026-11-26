use v5.42;
my $x=1; sub f { my $v=shift; $x=2; $v } print f($x), $x, "\n";

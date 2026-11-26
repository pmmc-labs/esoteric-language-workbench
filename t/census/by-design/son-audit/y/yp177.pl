use v5.42;
my $x="ab"; sub f { "@_" } print f($x, $x =~ tr/a/z/), "\n";

use v5.42;
sub f { return "[@_]" } my $x = 5; print f($x, $x + 1), "\n";

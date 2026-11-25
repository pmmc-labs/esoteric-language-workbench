use v5.42;
sub v($x) { $x * 2 }
sub w($x) { return $x . "a" }
sub u($x) { "abc" + $x }
my $n;
v($n);
w($n);
u(1);
say "end";

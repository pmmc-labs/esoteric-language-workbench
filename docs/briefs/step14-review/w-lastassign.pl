use v5.42;
sub f($n) { my @x = (1) x $n }
say f(3) ? "true" : "false";
say defined(f(3)) ? "def" : "undef";
my $f = 0;
sub g() { my ($p, $q) = (7, 8) }
say g() ? "yes" : "no";

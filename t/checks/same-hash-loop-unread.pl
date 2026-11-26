# check: ok
# A loop or a map over a hash whose block never reads what it is handed,
# and a hash handed to a sub whose last parameter is a hash: no order
# shows (step 12b).
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my $n = 0;
for my $v (values %h) { $n++; say $h{fig}; last; }
for (%h) { $n++ }
$n++ for values(%h);
$n++ for (%h);
sub told() { return 5 }
sub dflt($x //= told(), %o) { return $x + scalar(keys %o) }
my @ones = map { $h{pear} } values %h;
sub count($x, %o) { return $x . scalar(keys %o) . $o{fig}; }
say $n, scalar(@ones), count(1, %h), count(2, %h, more => 5), dflt(undef, %h);

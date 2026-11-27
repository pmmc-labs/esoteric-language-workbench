# model: t/models/die.py
use v5.42;
sub boom() { die "boom\n" }
my @a = (1, 2, 3); my %h = (k => "v"); my ($x, $y) = (1, 2);
try { push @a, 4, boom(); } catch ($e) { print $e }
try { ($x, $y) = (8, boom()); } catch ($e) { print $e }
try { @a = (9, boom()); } catch ($e) { print $e }
try { %h = (z => 1, q => boom()); } catch ($e) { print $e }
try { splice(@a, 0, 1, boom()); } catch ($e) { print $e }
try { my @b = sort { boom() } @a; } catch ($e) { print $e }
try { @a = sort { boom() } @a; } catch ($e) { print $e }
try { $h{new} .= boom(); } catch ($e) { print $e }
try { $h{or} //= boom(); } catch ($e) { print $e }
try { $a[5] += boom(); } catch ($e) { print $e }
try { $a[1] = boom(); } catch ($e) { print $e }
try { $h{k} = "w" . boom(); } catch ($e) { print $e }
say scalar(@a), " $x $y ", join(",", sort keys %h), " ", $h{k}, " ", defined $a[5] ? "d" : "u";

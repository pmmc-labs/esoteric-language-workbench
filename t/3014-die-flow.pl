# model: t/models/die.py
use v5.42;
sub pick($n) { try { return "small" if $n < 3; die "big\n" if $n > 6; } catch ($e) { return "caught $e" } return "middle" }
print pick(0), "\n";
print pick(1), "\n";
print pick(2), "\n";
print pick(3), "\n";
print pick(4), "\n";
print pick(5), "\n";
print pick(6), "\n";
print pick(7), "\n";
print pick(8), "\n";
for my $i (1 .. 6) { try { next if $i == 2; last if $i == 5; die "d$i\n" if $i % 2; say "even $i" } catch ($e) { print "c $e"; next if $i == 3 } say "after $i" }
OUTER: for my $i (1 .. 3) { for my $j (1 .. 3) { try { next OUTER if $j == 2; try { last OUTER if $i == 3 } catch ($f) { } say "$i$j" } catch ($e) { } } }
try { die "last one" } catch ($e) { print "found: $e" }
sub count($n) { my $t = 0; for my $i (1 .. $n) { try { $t += $i; die "skip\n" if $i % 3 == 0; $t += 100 } catch ($e) { next } } return $t }
say count(1);
say count(3);
say count(7);

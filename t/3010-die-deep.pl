# model: t/models/die.py
use v5.42;
no warnings 'recursion';
sub down($n, $k, $m) { die "at depth $n\n" if $n == $k && $m == 0; die "deep", $n if $n == $k && $m == 1; return down($n + 1, $k, $m) + 1 }
try { my $r = down(0, 0, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 0, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 1, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 1, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 2, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 2, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 5, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 5, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 40, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 40, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 300, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 300, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 3, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 3, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 0, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 0, 1); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 120, 0); say "no die" } catch ($e) { print "caught: ", $e }
try { my $r = down(0, 120, 1); say "no die" } catch ($e) { print "caught: ", $e }
sub up($n) { return $n if $n == 0; return up($n - 1) + 1 }
say "and a call that returns: ", up(50);

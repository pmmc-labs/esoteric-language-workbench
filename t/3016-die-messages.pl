# model: t/models/die.py
use v5.42;
try { die "plain" } catch ($e) { print "[", $e, "]\n" }
try { die "with newline\n" } catch ($e) { print "[", $e, "]\n" }
try { die "two\nlines" } catch ($e) { print "[", $e, "]\n" }
try { die "a", 1, "b", 2.5 } catch ($e) { print "[", $e, "]\n" }
try { die "" } catch ($e) { print "[", $e, "]\n" }
try { die } catch ($e) { print "[", $e, "]\n" }
try { die false } catch ($e) { print "[", $e, "]\n" }
try { die true, "!" } catch ($e) { print "[", $e, "]\n" }
try { die 0 } catch ($e) { print "[", $e, "]\n" }
try { die 1e21 } catch ($e) { print "[", $e, "]\n" }
try { die -7, "\n" } catch ($e) { print "[", $e, "]\n" }
try { die "", "end\n" } catch ($e) { print "[", $e, "]\n" }
my @e; my @two = ("a", "b"); my $n = 3;
try { die @e } catch ($e) { print "[", $e, "]\n" }
try { die @two } catch ($e) { print "[", $e, "]\n" }
try { die @two, "\n" } catch ($e) { print "[", $e, "]\n" }
try { die "n=$n" } catch ($e) { print "[", $e, "]\n" }
try { die "$n\n" } catch ($e) { print "[", $e, "]\n" }
try { die $n * 2, "x" } catch ($e) { print "[", $e, "]\n" }
try { die $n / 2 } catch ($e) { print "[", $e, "]\n" }
try { die 0.1 + 0.2 } catch ($e) { print "[", $e, "]\n" }
try { die -$n } catch ($e) { print "[", $e, "]\n" }
try { die "@two" } catch ($e) { print "[", $e, "]\n" }
try { die join("-", @two), "!" } catch ($e) { print "[", $e, "]\n" }
sub where() { ... } try { where() } catch ($e) { print $e }
try { die "x" } catch ($e) { my $e = "inner"; print $e, "\n" }
my $kept = "outer"; try { die "y\n" } catch ($kept) { $kept = "changed"; print "$kept\n" } say $kept;

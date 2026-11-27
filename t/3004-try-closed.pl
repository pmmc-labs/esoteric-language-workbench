# A try that ends with no die is closed: a later die goes to the try round
# it, or out of the program, and never back into a try that is over. And a
# return in a try is the sub's, a list's too (D141, D18).
use v5.42;
try {
    try { say "inner ran" } catch ($e) { say "not here" }
    for my $i (1 .. 2) { try { say "round $i" } catch ($e) { say "nor here" } }
    die "after\n";
} catch ($e) { print "outer: $e" }
sub fine($n) { try { return "returned $n" if $n; } catch ($e) { } return "fell through" }
say fine(1), " ", fine(0);
try { die "then\n" } catch ($e) { print "caught $e" }
sub pair() { try { return (1, 2); } catch ($e) { } return 3; }
sub count(@l) { return scalar(@l) }
say count(pair(), 8);
my @got = (pair(), 9);
say "@got";
sub none() { try { return; } catch ($e) { } return 1; }
my @n = (none(), none());
say scalar(@n);

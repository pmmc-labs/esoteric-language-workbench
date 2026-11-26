# check: ok
# A hash where only how many keys it has is asked, where it is copied, and
# as a parameter: no order shows (step 12).
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
if (%h) { say "some"; }
unless (!%h) { say "still some"; }
my $n = %h;
my $k = keys %h;
my %g = %h;
say "four" if keys %h == 4;
say $n + $k, scalar(keys %g);
sub count($x, %o) { return $x . scalar(keys %o); }
say count(1, a => 2);

# kind: refused
# perl warns: say (...) interpreted as function. It looks along the
# line of the bracket for what may follow a call, and the if is on the
# next (T128). Found by the review.
use v5.42;
my $x = 1;
say ("a")
if $x;

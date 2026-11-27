# check: fails: line 6: keys without sort
# A quote inside q{}: a reader that paired it would hide the keys after
# it (step 16a).
use v5.42;
my %h = (a => 1); say q{"};
say join ",", keys %h; say "x";

# perl makes a hash in the element, and a reference to it. Refused until
# step 13a, which makes it too (T248).
use v5.42;
my %g;
$g{x}{y} = 1;
say ref($g{x}), $g{x}{y};

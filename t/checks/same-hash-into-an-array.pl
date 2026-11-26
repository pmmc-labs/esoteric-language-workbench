# check: ok
# A hash's values, and the hash itself, copied into an array that is only
# sorted or counted: no order shows (step 12a).
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
my @v = values %h;
my @all = (%h);
say join(",", sort { $a <=> $b } @v), "|", scalar(@v), "|", join(",", (sort @all));

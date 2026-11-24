# check: fails: changes from run to run
# It reads well, and PERL_HASH_SEED=1 to 300 all print the same line: a
# short seed leaves most of perl's seed zero, and these three keys then
# sit in the same buckets every time. Seeds of the full width move them.
use v5.42;
my %h = (pine => 1, yew => 2, nut => 3);
my @k = sort { 0 } keys %h;
say "the middle key is ", $k[1] eq "yew" ? "yew" : "not yew";

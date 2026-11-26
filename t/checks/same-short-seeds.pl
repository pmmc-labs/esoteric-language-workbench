# check: fails: changes from run to run
# It reads well (a sort, whose ties stay as they came), and most short
# seeds, PERL_HASH_SEED=1 to 300, print the same line: a short seed leaves
# most of perl's seed zero. Seeds of the full width move the keys.
use v5.42;
my %h = (pine => 1, yew => 2, nut => 3);
my @k = sort { length($a) <=> length($b) } keys %h;
say "the first key is ", $k[0] eq "yew" ? "yew" : "not yew";

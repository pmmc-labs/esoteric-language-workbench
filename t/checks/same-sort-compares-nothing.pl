# check: fails: without sort
# A sort whose block says every pair is equal gives back the order it was
# handed, which is the hash's (step 12's review).
use v5.42;
my %h = (pear => 3, apple => 1, fig => 2, plum => 4);
say join ",", sort { 0 } keys %h;

# check: fails: line 5: values without sort
# A sort further out, of something else, is not a sort of these.
use v5.42;
my %h = (a => 1);
say join ",", sort(1, 2), values %h;

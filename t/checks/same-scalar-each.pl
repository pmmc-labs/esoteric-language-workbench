# check: fails: line 5: each without sort
# scalar makes a count of keys; of each, it makes the first key.
use v5.42;
my %h = (a => 1);
say scalar(each %h);

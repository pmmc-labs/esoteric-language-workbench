# check: fails: line 5: values without sort
# It sorts one value, and which one is the hash's to say.
use v5.42;
my %h = (a => 1);
say sort((values %h)[0]);

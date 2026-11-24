# check: fails: line 6: keys without sort
# A variable called sort is not sort.
use v5.42;
my %h = (a => 1);
my $sort = sub { @_ };
say join ",", &$sort(keys %h);

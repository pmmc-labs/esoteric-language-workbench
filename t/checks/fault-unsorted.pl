# check: fails: line 5: keys without sort
# kind: fault
use v5.42;
my %h = (a => 1);
say join ",", keys %h;
my $u;
say $u + 1;

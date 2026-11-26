use v5.42;
my %h=(a=>1); my ($k,$v)=%h; delete $h{a}; print "$k$v\n";

use v5.42;
my %h=(a=>1); my $v=delete $h{a}; print "$v ", exists $h{a}?1:0, "\n";

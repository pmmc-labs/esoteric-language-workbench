use v5.42;
my %h=(a=>1,b=>2); my @k = sort keys %h; $h{c}=3; print "@k\n";

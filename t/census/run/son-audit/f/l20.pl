use v5.42;
my %h=(a=>1,b=>2); $_++ for values %h; print "$h{a}$h{b}\n";

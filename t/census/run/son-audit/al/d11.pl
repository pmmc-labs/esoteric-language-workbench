use v5.42;
my %h=(k=>1); ($h{k} += 1) *= 5; print "$h{k}\n";

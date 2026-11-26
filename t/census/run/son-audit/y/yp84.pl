use v5.42;
my %h=(k=>1); sub f { $h{k}=7; 0 } my $n = ($h{k} = 5) + f(); print "$n\n";

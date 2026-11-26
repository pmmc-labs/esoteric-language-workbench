use v5.42;
my %h=(a=>1); sub m2 { $_[0]=9 } m2($h{a}); print "$h{a}\n";

use v5.42;
my %h = (a=>1); sub k { $_[0] = 5 } k($h{a}); print "$h{a}\n";

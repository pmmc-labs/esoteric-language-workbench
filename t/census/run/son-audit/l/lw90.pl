use v5.42;
my %h=(a=>1); for my $v (values %h) { $v .= "x"; last if 1 } print "$h{a}\n";

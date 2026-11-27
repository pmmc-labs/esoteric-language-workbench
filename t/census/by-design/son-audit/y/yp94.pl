use v5.42;
my %h=(a=>1); my $e=\$h{a}; my $n = $h{a} + ($$e = 7); print "$n\n";

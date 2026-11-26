use v5.42;
my $r={a=>1}; my %c=%$r; $c{a}=2; print "$r->{a}\n";

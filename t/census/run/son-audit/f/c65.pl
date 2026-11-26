use v5.42;
my $x=1; my %h=(a=>$x); $x=2; my @l=($x); $x=3; print "$h{a}@l\n";

use v5.42;
my %h=(a=>1); my %c=%h; my $r=\%c; $r->{a}=2; print "$h{a}\n";

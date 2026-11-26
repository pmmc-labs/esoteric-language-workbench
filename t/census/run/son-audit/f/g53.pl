use v5.42;
my %h=(a=>1); my $r=\%h; my %c=%h; $r->{a}=9; print "$c{a}\n";

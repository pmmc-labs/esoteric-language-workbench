use v5.42;
my %h=(a=>1); my $s = join(",", values %h, $h{a}=9); print "$s\n";

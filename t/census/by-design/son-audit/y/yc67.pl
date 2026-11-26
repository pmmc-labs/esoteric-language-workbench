use v5.42;
my %h=(a=>"x"); my $s = $h{a} . ($h{a} = "z"); print "$s\n";

use v5.42;
my $s=join ",", map { ord } split //, "ab"; print "$s\n";

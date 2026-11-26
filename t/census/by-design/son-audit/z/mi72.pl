use v5.42;
my @a=(1,2,3); my $str=join ",", map { $_ % 2 ? "o" : "e" } @a; my %h=map { $_ => 1 } @a; my @k=sort keys %h; print "$str @k\n";

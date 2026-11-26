use v5.42;
my $s="abc"; my $n = () = $s =~ /./g; my @m=$s=~/(a)(b)/; print "$n@m\n";

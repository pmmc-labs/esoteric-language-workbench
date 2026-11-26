use v5.42;
my $s="abc"; ($s .= "d") =~ s/a/X/; print "$s\n";

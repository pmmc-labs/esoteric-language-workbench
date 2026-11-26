use v5.42;
my $s="abc"; my $t=$s; $s =~ s/b/X/; print "$s $t\n";

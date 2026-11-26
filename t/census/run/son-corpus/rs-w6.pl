use v5.42;
my $s = "abc"; $s =~ s/b/$&$&/; print "$s\n";

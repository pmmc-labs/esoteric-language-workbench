use v5.42;
my $s = "abc"; $s =~ s/(z)/[$1]/; print "$s\n";

use v5.42;
my $s = "  a b  "; (my $t = $s) =~ s/^\s+|\s+$//g; (my $u = $s) =~ s/\s+/ /g; my @w = split " ", $s; print "[$t][$u]", scalar(@w), "\n";

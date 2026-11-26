use v5.42;
my $s = "a1b2"; my @m = $s =~ /(\d)/g; $s =~ s/\d//g; print "@m $s\n";

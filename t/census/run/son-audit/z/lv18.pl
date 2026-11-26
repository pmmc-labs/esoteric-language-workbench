use v5.42;
my $y="abc"; (my $x = $y) =~ tr/a-c/A-C/; print "$x$y\n";

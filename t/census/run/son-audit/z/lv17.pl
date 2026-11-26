use v5.42;
my $y="aXa"; (my $x = $y) =~ s/a/b/g; print "$x$y\n";

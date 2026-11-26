use v5.42;
my $s = "x"; $s x= 3; $s .= "y" x 2; my @r = ("a","b") x 2; print "$s @r ", scalar(@r), "\n";

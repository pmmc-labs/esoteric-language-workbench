use v5.42;
my $x="ab"; my $n = ($x =~ tr/a/z/) . $x; print "$n\n";

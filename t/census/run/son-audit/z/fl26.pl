use v5.42;
my $s="ab"; my @b=(length($s), $s.="c", length($s)); print "@b\n";

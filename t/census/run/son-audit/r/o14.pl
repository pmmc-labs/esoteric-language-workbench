use v5.42;
$_="abc"; my $n = tr/a-c//; s/b/X/; print "$n $_\n";

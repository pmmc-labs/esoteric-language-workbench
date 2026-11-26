use v5.42;
$_="t"; eval { my @r=grep { die "x\n" } 1,2 }; print "$_\n";

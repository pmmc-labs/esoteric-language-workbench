use v5.42;
$_="t"; eval { for (1,2) { die "x\n" } }; print "$_\n";

use v5.42;
$_="t"; eval { for (1..3) { die "x\n" if $_==2 } }; print "$_\n";

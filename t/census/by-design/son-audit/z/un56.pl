use v5.42;
$_="t"; eval { local $_="u"; die "x\n" }; print "$_\n";

use v5.42;
my $s = "x"; my @l = ($s, $s .= "y", $s); print "@l\n";

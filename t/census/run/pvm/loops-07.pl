use v5.42;
my @l = ($ENV{A} // "a", "b", "c");
my $s = "";
$s .= $_ foreach @l;
print "$s\n";

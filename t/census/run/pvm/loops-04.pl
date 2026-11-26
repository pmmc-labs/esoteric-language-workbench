use v5.42;
my @l = ($ENV{A} // "a", "b", "c");
foreach my $x (@l) { print $x }
print "\n";

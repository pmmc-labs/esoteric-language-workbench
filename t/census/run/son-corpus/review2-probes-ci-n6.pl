use v5.42;
my $c = 0; my $x = 1;
if ($c) { print "t" } else { if ($x) { print "e" } $x = 3 }
print "$x\n";

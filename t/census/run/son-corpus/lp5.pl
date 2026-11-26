use v5.42;
my $x = 0;
while (1) { last if $x == 3; $x = $x + 1 }
print "e $x\n";

use v5.42;
my $a = $ARGV[0] // 3;
my $b = $ARGV[1] // "3.0";
print "sm [", ($a ~~ $b), "]\n";
print "eq [", ($a eq $b), "]\n";

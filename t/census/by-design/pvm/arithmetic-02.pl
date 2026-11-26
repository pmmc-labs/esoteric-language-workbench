use v5.42;
my $a = $ARGV[0] // "ab";
my $b = $ARGV[1] // "cd";
print "joined: ", $a . $b, "\n";
print "repeat: ", $a x 3, "\n";

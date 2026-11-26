use v5.42;
my $a = $ENV{X} // "hello";
my $b = $ENV{X} // "hello";
substr($a, 0, 1) = "J";
my $old = substr($b, 0, 1, "J");
print "[$a][$b][$old]\n";

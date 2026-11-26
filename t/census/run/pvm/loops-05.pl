use v5.42;
my $i = $ENV{N} // 0;
do { print "once" } while $i > 0;
print "\n";

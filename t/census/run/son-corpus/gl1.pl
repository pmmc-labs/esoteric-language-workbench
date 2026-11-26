use v5.42;
my @none = <*.nonexistent-xyz>;
print "got ", scalar(@none), "\n";

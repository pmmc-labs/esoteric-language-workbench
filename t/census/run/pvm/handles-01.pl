use v5.42;
open(my $fh, "<", \"x\n");
print "opened\n";
close($fh);

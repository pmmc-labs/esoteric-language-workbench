use v5.42;
open(my $fh, "<", \"only\n");
my $l = <$fh>;
print "eof\n" if eof($fh);
close($fh);

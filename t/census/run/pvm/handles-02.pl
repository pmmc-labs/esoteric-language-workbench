use v5.42;
open(my $fh, "<", \"one\ntwo\n");
my $l = <$fh>;
print $l;
close($fh);

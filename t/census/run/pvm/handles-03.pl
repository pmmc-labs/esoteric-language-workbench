use v5.42;
open(my $fh, "<", \"one\ntwo\n");
my @lines = <$fh>;
print scalar(@lines), "\n";
close($fh);

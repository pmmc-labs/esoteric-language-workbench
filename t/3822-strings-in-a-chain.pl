# kind: same
# A string from an element through a reference, chomped, formatted and searched.
use v5.42;
my $r = [" x\n"];
my $s = $r->[0];
chomp($s);
say ucfirst(sprintf("%-4s|", $s)), rindex($r->[0], "x");

# check: fails: perl warned as it ran
# kind: dies
# A dies test in which perl also warns: the hole "The checks themselves" left for step 15.
use v5.42;
my $u;
my $x = "a" . $u;
die "x\n";

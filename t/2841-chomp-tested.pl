# kind: refused
# perl tests the count: y.
use v5.42;
my $s = "a\n";
if (chomp $s) { say "y" }

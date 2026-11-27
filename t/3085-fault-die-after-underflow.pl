# kind: fault
# An uncaught die after a string read as a number underflowed: perl exits 34
# (T319, D151).
use v5.42;
my $s = "1e-310";
my $v = $s + 0;
say "read";
die "x\n";

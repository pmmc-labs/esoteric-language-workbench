# kind: fault
# The same after a ** that underflowed (T319, D151); a die caught between.
use v5.42;
my $n = 10;
my $v = $n ** -400;
try { die "caught\n" } catch ($e) { print $e }
die "x\n";

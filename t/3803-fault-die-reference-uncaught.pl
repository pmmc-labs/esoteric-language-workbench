# kind: fault
# perl writes the reference's address on stderr and exits 255: D112's fault.
use v5.42;
say "before";
my $r = { a => 1 };
die $r;

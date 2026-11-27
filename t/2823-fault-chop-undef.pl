# kind: fault
# perl warns: Use of uninitialized value $s in scalar chop.
use v5.42;
my $s;
chop $s;

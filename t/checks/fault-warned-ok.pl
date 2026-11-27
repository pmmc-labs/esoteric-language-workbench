# check: ok
# kind: fault
# A fault after a warn: the warn is the start of perl's stderr.
use v5.42;
warn "w\n";
my $n = "abc" + 1;

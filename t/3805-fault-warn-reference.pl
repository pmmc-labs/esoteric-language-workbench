# kind: fault
# perl warns with the reference's address: D112's fault.
use v5.42;
say "before";
my $r = [1];
warn $r;

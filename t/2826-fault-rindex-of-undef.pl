# kind: fault
# perl warns: Use of uninitialized value in rindex.
use v5.42;
my $u;
say rindex($u, "a");

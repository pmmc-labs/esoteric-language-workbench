# kind: fault
# perl takes 0 and warns: Use of uninitialized value in sprintf.
use v5.42;
my $u;
say sprintf("%*s", $u, "a");

# kind: fault
# perl prints nothing and warns: Use of uninitialized value in sprintf.
use v5.42;
my $u;
say sprintf("[%s]", $u);

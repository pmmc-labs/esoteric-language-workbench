# kind: refused
# perl warns: Subroutine f redefined, and prints 2.
use v5.42;
sub f() { return 1; }
sub f() { return 2; }
say f();

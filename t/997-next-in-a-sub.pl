# kind: refused
# perl leaves the loop of the caller, with a warning: Exiting subroutine via next (T60).
use v5.42;
sub f() { next; }
my $i = 0;
while ($i++ < 3) {
    f();
    say $i;
}

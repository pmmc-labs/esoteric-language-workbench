# kind: fault
# A fault names the line its statement starts on (D34), and after a call
# has returned that is the caller's statement again: here the sum that
# begins on line 14, though the sub's own last statement was on line 9
# and the undef is on line 16. (perl warns, and names line 16.)
use v5.42;
sub one() {
    say "in";
    return 1;
}
my $u;
my $r = 1 + one();
say $r;
$r = one()
    + one()
    + $u;
say "not reached";

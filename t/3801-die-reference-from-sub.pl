# kind: same
# A reference thrown from a sub, out of a loop and by a last in its catch (D142, D143).
use v5.42;
my @grid = ([1, 2], [3, 4]);
for my $row (@grid) {
    try {
        die { at => $row->[0] } if $row->[1] == 4;
        say $row->[1];
    } catch ($e) {
        say "row ", $e->{at};
        last;
    }
}
my $r = [1];
sub g($t) { die $t; }
try { g($r); } catch ($e) { say scalar(@grid), ref($e), $e == $r ? " same" : " other"; }

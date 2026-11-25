# kind: refused
# The same for a last statement (T143).
use v5.42;
sub last2($x) {
    ($x) x 2;
}
my $s = last2("k");
say $s;

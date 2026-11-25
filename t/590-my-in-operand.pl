# kind: refused
# perl takes it, and the my may never be reached (D21, D56).
use v5.42;
my $y = 0;
if ($y && (my $x = $y)) {
    say 1;
}

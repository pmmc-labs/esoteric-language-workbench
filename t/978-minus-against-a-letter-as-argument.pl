# kind: refused
# perl hands g an undef, in silence (T135).
use v5.42;
sub e($p) { return $p + 10; }
sub g($p) { return defined($p) ? "d" : "u"; }
say g(-e(2));

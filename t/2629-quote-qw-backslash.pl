# kind: refused
# perl keeps it: a\|b.
use v5.42;
say join "|", qw(a\ b);

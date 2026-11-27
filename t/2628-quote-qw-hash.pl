# kind: refused
# perl warns: Possible attempt to put comments in qw() list.
use v5.42;
say join "|", qw(a #b c);

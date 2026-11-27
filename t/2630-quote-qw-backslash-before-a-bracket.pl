# kind: refused
# perl takes it away: a(b|c.
use v5.42;
say join "|", qw(a\(b c);

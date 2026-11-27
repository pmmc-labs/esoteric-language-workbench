# kind: refused
# perl does not compile it: syntax error near '[]'.
use v5.42;
my $r = [1, 2];
say $r->[];

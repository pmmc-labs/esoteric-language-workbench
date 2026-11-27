# kind: refused
# perl does not compile it: syntax error near '}->'.
use v5.42;
my $k = "a";
say({ $k => 1 }->{a});

# kind: refused
# perl runs it: '1\n'.
use v5.42;
my @g = ([1]);
say "$g[0][0]";

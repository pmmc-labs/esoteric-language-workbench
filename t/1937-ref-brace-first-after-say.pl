# kind: refused
# perl runs it: '1\n'.
use v5.42;
say {a => 1}->{a};

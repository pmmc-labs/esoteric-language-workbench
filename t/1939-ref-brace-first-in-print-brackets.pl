# kind: refused
# perl runs it: '1'.
use v5.42;
print({ a => 1 }->{a});

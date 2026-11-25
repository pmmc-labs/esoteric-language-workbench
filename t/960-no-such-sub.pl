# kind: refused
# perl prints before, and dies when it gets to the call.
use v5.42;
say "before";
g(1);
say "after";

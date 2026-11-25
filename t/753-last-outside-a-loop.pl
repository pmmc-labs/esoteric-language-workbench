# kind: refused
# perl prints before, and then dies: Can't "last" outside a loop block.
use v5.42;
say "before";
last;

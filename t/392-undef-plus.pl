# kind: refused
# perl doesn't compile it: `undef` takes `+ 1` for its argument (T105).
use v5.42;
say undef + 1;

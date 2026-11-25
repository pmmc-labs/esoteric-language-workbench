# kind: refused
# perl doesn't compile it: `<=>` and `==` don't associate (T51).
use v5.42;
say 1 <=> 2 == -1;

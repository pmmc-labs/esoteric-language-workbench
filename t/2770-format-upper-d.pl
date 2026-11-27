# kind: refused
# perl takes %D for %ld: 4.
use v5.42;
say sprintf("%D", 4);

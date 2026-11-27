# kind: refused
# perl prints %*3d and warns: Invalid conversion.
use v5.42;
say sprintf("%*3d", 5, 3);

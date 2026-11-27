# kind: refused
# perl prints %5 and warns: Invalid conversion.
use v5.42;
say sprintf("%5");

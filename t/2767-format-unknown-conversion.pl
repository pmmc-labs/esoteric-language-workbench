# kind: refused
# perl prints %y and warns: Invalid conversion (T270).
use v5.42;
say sprintf("%y", 1);

# kind: refused
# perl prints abc% and warns: Invalid conversion in sprintf: end of string (T270).
use v5.42;
say sprintf("abc%");

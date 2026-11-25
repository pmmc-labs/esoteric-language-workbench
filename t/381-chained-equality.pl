# kind: refused
# perl prints an empty line: `(1 != 1) && (1 == 0)`. Read from the left it is 1 (T108).
use v5.42;
say 1 != 1 == 0;

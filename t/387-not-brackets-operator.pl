# kind: refused
# perl prints 1: a bracket after `not` is all it takes, so this is `(not 0) || 1`. Without
# the brackets, `not 0 || 1` is false (T107, D51).
use v5.42;
say(not (0) || 1);

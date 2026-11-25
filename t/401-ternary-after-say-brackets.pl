# kind: refused
# perl prints 1, and warns: the ? : is applied to what say returned (T25).
use v5.42;
say (1) ? 2 : 3;

# kind: refused
# perl prints Inf, in silence (T81). A Num is finite (D37).
use v5.42;
say 1e400;

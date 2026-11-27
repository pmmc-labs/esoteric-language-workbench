# kind: fault
# perl prints -1 (T265).
use v5.42;
say sprintf("%d", 1e30);

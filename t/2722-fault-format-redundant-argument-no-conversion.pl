# kind: fault
# perl prints abc and warns: Redundant argument in sprintf.
use v5.42;
say sprintf("abc", 1);

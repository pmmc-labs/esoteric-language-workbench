# kind: fault
# perl prints -0.000000e+00, and 0.000000e+00 after "-0" + 0 (T282).
use v5.42;
say sprintf("%e", "-0");

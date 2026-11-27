# kind: fault
# perl prints -0.0 (T282).
use v5.42;
say sprintf("%.1f", " -0.0");

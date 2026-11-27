# kind: refused
# perl prints 49.46.50 (T276).
use v5.42;
say sprintf("%vd", "1.2");

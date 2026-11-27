# kind: refused
# perl prints b a (T276).
use v5.42;
say sprintf("%2\$s %1\$s", "a", "b");

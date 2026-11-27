# kind: refused
# perl dies: Modification of a read-only value attempted (T276).
use v5.42;
say sprintf("%n", 1);

# kind: refused
# perl prints garbage for %.2147483648d.
use v5.42;
say sprintf("%.2147483648d", 1);

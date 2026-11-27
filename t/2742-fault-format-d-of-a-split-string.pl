# kind: fault
# perl cuts it to 1 or to 2 by what the string was used as before.
use v5.42;
say sprintf("%d", "1.99999999999999999");

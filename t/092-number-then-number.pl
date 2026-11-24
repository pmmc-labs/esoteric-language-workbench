# kind: refused
# perl prints 1.55: after a number and a blank, a dot joins strings (T78).
use v5.42;
say 1.5 .5;

# kind: fault
# perl makes the surrogate, and warns when it is printed.
use v5.42;
say sprintf("%c", 0xD800);

# kind: fault
# perl dies: Use of code point 0xFFFFFFFFFFFFFFFF is not allowed.
use v5.42;
say sprintf("%c", -1);

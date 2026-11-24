# kind: refused
# perl prints 8: a leading zero makes a literal octal (T24). Octal is step 2.
use v5.42;
say 010;

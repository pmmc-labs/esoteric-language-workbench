# kind: refused
# perl prints 8: a leading zero makes a literal octal (T24, D38).
use v5.42;
say 010;

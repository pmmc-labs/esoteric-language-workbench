# kind: refused
# perl prints 2, the length of -5, and warns that `length` without parentheses is
# ambiguous.
use v5.42;
say length - 5;

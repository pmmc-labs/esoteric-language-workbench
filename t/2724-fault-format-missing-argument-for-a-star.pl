# kind: fault
# perl prints 5 and warns: Missing argument.
use v5.42;
say sprintf("%*d", 5);

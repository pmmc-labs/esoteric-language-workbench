# kind: fault
# perl prints 0 and warns: Argument "abc" isn't numeric in sprintf.
use v5.42;
say sprintf("%d", "abc");

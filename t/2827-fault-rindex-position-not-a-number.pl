# kind: fault
# perl warns: Argument "x" isn't numeric in rindex.
use v5.42;
say rindex("abc", "a", "x");

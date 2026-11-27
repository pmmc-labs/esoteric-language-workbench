# kind: refused
# perl prints a to stdout; a handle is step 21.
use v5.42;
printf STDOUT "%s\n", "a";

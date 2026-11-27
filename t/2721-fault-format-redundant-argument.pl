# kind: fault
# perl prints a and warns: Redundant argument in sprintf (T270).
use v5.42;
say "before";
say sprintf("%s", "a", "b");

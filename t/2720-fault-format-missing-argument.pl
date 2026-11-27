# kind: fault
# perl prints a- and warns: Missing argument in sprintf (T270).
use v5.42;
say "before";
say sprintf("%s-%s", "a");

# kind: fault
# perl prints abc and warns: Redundant argument in printf (T270).
use v5.42;
printf("abc\n", 1);

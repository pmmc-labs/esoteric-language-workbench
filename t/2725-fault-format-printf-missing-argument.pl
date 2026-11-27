# kind: fault
# perl prints | and warns: Missing argument in printf (T270).
use v5.42;
printf("%s|\n");

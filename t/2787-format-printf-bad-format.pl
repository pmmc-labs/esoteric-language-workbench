# kind: refused
# perl prints %y and warns: Invalid conversion in printf.
use v5.42;
printf("%y\n", 1);

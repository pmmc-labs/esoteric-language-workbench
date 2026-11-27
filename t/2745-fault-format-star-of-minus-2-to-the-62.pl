# kind: fault
# perl dies: Integer overflow in format string for sprintf.
use v5.42;
say length sprintf("%*d", -4611686018427387904, 1);

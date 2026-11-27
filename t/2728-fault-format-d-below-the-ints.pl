# kind: fault
# perl prints -9223372036854775808, clamped.
use v5.42;
say sprintf("%d", -9223372036854775808.0);
say sprintf("%d", -9223372036854777856.0);

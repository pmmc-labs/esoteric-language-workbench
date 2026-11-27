# kind: fault
# perl prints 9223372036854775808: -2^63 - 2048 clamped.
use v5.42;
say sprintf("%u", -9223372036854777856.0);

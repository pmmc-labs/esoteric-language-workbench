# kind: fault
# perl prints -9223372036854775808 (T265).
use v5.42;
say sprintf("%d", 9223372036854775807);
say sprintf("%d", 9223372036854775808.0);

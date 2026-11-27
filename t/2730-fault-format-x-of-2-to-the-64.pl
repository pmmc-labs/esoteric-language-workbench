# kind: fault
# perl prints ffffffffffffffff, clamped (T265).
use v5.42;
say sprintf("%x", 18446744073709549568.0);
say sprintf("%x", 18446744073709551616.0);

# kind: fault
# model: t/models/arith.py
use v5.42;
say(1);
say((2 * 3) + (7 % 2));
say((9223372036854775807 * 2) + (7 % 0));
say(2);

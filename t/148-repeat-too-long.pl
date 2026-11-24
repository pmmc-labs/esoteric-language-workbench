# kind: fault
# model: t/models/str.py
use v5.42;
say(1);
say(length('ab' x 1000));
say(length('ab' x 9223372036854775807));
say(2);
